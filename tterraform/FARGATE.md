# AWS Fargate Example

This document explains the Fargate (serverless container) example in the Terraform configuration.

## What is Fargate?

**Fargate** is AWS's serverless container platform:
- No EC2 instance management needed
- Pay only for compute resources used
- Automatic scaling
- High availability built-in

## Architecture

```
ECS Cluster
    ↓
ECS Service (desired_count=1)
    ↓
ECS Task Definition (Container spec)
    ↓
Fargate Launch Type (no EC2 needed)
    ↓
Docker Container (runs in VPC)
    ↓
CloudWatch Logs (captures output)
```

## Components

### 1. **ECS Cluster** (`aws_ecs_cluster`)
- Container orchestration cluster
- Container Insights enabled for monitoring
- Named: `ec2-instance-cluster`

### 2. **ECS Task Definition** (`aws_ecs_task_definition`)
Specifies container configuration:
- **Image**: Docker image to run (default: nginx:latest)
- **CPU**: CPU units (256, 512, 1024, etc.)
- **Memory**: RAM in MB (512, 1024, 2048, etc.)
- **Port**: Container port (default: 80)
- **Logging**: CloudWatch logs configuration
- **Environment variables**: Passed to container

### 3. **ECS Service** (`aws_ecs_service`)
- Launches and manages tasks
- Desired count: number of running tasks
- Launch type: Fargate (serverless)
- Network: Runs in default VPC with public IP
- Auto-restart if task fails

### 4. **IAM Roles**
- **Execution Role**: Allows ECS to pull images and write logs
- **Task Role**: Allows container app to access AWS resources (S3, DynamoDB, etc.)

### 5. **Auto-Scaling**
- **CPU Policy**: Scales when average CPU > 70%
- **Memory Policy**: Scales when average memory > 80%
- **Min capacity**: ecs_desired_count (default: 1)
- **Max capacity**: ecs_max_capacity (default: 4)

### 6. **CloudWatch Logs** (`aws_cloudwatch_log_group`)
- Captures container output
- Retention: 7 days
- Log group: `/ecs/ec2-instance`

### 7. **Security Group**
- Allows traffic on container port
- Allows all outbound traffic

## Setup Instructions

### 1. Deploy Fargate Service

```bash
cd c:\alex\work\memo\tterraform

# Create terraform.tfvars with Fargate settings
cat > terraform.tfvars << EOF
container_image = "nginx:latest"
container_port  = 80
fargate_cpu     = 256
fargate_memory  = 512
ecs_desired_count = 2
ecs_max_capacity  = 4
environment = "dev"
EOF

terraform init
terraform plan
terraform apply
```

### 2. Get Task IP and Test

```bash
# Get task IP from AWS console or CLI
aws ecs describe-services \
  --cluster ec2-instance-cluster \
  --services ec2-instance-service \
  --query 'services[0].runningCount'

# Get task details
aws ecs list-tasks --cluster ec2-instance-cluster
aws ecs describe-tasks --cluster ec2-instance-cluster --tasks <task-arn>
```

### 3. View Container Logs

```bash
# Stream logs
aws logs tail /ecs/ec2-instance --follow

# Or in Terraform
terraform output
```

## Variables for Customization

Edit `terraform.tfvars`:

```hcl
# Docker image to run
container_image = "nginx:latest"
# Example custom image:
# container_image = "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:v1"

# Container port
container_port = 80

# Fargate CPU units: 256, 512, 1024, 2048, 4096
fargate_cpu = 256

# Memory in MB: 512, 1024, 2048, 3072, 4096, etc.
# Must be compatible with CPU choice
fargate_memory = 512

# Initial number of tasks
ecs_desired_count = 1

# Maximum tasks for auto-scaling
ecs_max_capacity = 4

# Environment name
environment = "dev"
```

## CPU/Memory Combinations

Valid combinations for Fargate:

| CPU     | Memory Options |
|---------|----------------|
| 256     | 512, 1024, 2048 |
| 512     | 1024-4096 (1GB increments) |
| 1024    | 2048-8192 (1GB increments) |
| 2048    | 4096-16384 (1GB increments) |
| 4096    | 8192-30720 (1GB increments) |

## Using Private Docker Images

If using ECR (Elastic Container Registry):

```hcl
container_image = "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest"
```

Ensure task execution role has ECR permissions:
```terraform
resource "aws_iam_role_policy" "ecr_access" {
  role = aws_iam_role.ecs_task_execution_role.id
  
  policy = jsonencode({
    Statement = [{
      Effect = "Allow"
      Action = [
        "ecr:GetAuthorizationToken",
        "ecr:BatchGetImage",
        "ecr:GetDownloadUrlForLayer"
      ]
      Resource = "*"
    }]
  })
}
```

## Auto-Scaling Details

### CPU Scaling
- Scales UP when average CPU > 70%
- Scales DOWN when average CPU < 70%
- Metric: ECSServiceAverageCPUUtilization

### Memory Scaling
- Scales UP when average memory > 80%
- Scales DOWN when average memory < 80%
- Metric: ECSServiceAverageMemoryUtilization

### Example:
With `desired_count=1` and `max_capacity=4`:
- Starts with 1 task
- If CPU > 70%, may scale to 2, 3, or 4 tasks
- If CPU drops, scales back down

## Adding Load Balancer

To add an Application Load Balancer:

```terraform
resource "aws_lb" "main" {
  name               = "${var.instance_name_prefix}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = data.aws_subnets.default.ids
}

resource "aws_lb_target_group" "app" {
  name        = "${var.instance_name_prefix}-tg"
  port        = var.container_port
  protocol    = "HTTP"
  vpc_id      = data.aws_vpc.default.id
  target_type = "ip"
}

resource "aws_ecs_service" "app" {
  # ... existing config ...
  
  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = var.instance_name_prefix
    container_port   = var.container_port
  }
}
```

## Monitoring

View metrics in CloudWatch:

```bash
# CPU utilization
aws cloudwatch get-metric-statistics \
  --namespace AWS/ECS \
  --metric-name CPUUtilization \
  --dimensions Name=ServiceName,Value=ec2-instance-service Name=ClusterName,Value=ec2-instance-cluster \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 300 \
  --statistics Average
```

## Cleanup

```bash
terraform destroy
```

## Troubleshooting

**Tasks not starting:**
- Check task definition is valid
- Verify IAM execution role permissions
- Check Docker image is accessible
- Review CloudWatch logs

**Service unhealthy:**
- Check security group allows inbound traffic
- Verify container port matches task definition
- Check application logs in CloudWatch

**Auto-scaling not working:**
- Verify target and scaling policies are created
- Check CloudWatch metrics show CPU/memory data
- Review auto-scaling activity history
