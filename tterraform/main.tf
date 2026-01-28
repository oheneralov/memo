# Data source to get the latest Amazon Linux 2 AMI
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Create EC2 security group
resource "aws_security_group" "ec2_sg" {
  name        = "${var.instance_name_prefix}-sg"
  description = "Security group for EC2 instances"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.instance_name_prefix}-sg"
    }
  )
}

# ============================================================================
# EXAMPLE 1: Create EC2 instances using count
# ============================================================================
# Use this when you have a simple number-based repetition
resource "aws_instance" "ec2_instances" {
  count                = var.instance_count
  ami                  = data.aws_ami.amazon_linux_2.id
  instance_type        = var.instance_type
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  tags = merge(
    var.tags,
    {
      Name = "${var.instance_name_prefix}-${count.index + 1}"
    }
  )
}

# ============================================================================
# EXAMPLE 2: Create EC2 instances using for_each with a map
# ============================================================================
# for_each is better when you have different configurations per instance
resource "aws_instance" "ec2_instances_foreach" {
  for_each           = var.instances_config
  ami                = data.aws_ami.amazon_linux_2.id
  instance_type      = each.value.instance_type
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  tags = merge(
    var.tags,
    each.value.tags,
    {
      Name = each.key
    }
  )
}

# ============================================================================
# EXAMPLE 3: Create EC2 instances using for_each with a list (requires toset)
# ============================================================================
# When using a list converted to a set
resource "aws_instance" "ec2_instances_list" {
  for_each           = toset(var.instance_names)
  ami                = data.aws_ami.amazon_linux_2.id
  instance_type      = var.instance_type
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  tags = merge(
    var.tags,
    {
      Name = each.value
    }
  )
}

# ============================================================================
# EXAMPLE 4: Create EC2 instances using a module
# ============================================================================
# Modules promote code reusability and maintainability
# See modules/ec2_instance/ for the module definition

# Single instance using module (completely self-contained with defaults)
module "web_server" {
  source = "./modules/ec2_instance"
}

# Multiple instances using module with for_each
module "app_servers" {
  for_each = var.instances_config

  source = "./modules/ec2_instance"

  instance_name      = each.key
  instance_type      = each.value.instance_type
  ami_id             = data.aws_ami.amazon_linux_2.id
  security_group_ids = [aws_security_group.ec2_sg.id]
  tags = merge(
    var.tags,
    each.value.tags
  )
}

# ============================================================================
# EXAMPLE 5: Conditional resource creation and configuration
# ============================================================================
# Use conditions to conditionally create resources or set attributes

# Conditionally create an instance based on a flag
resource "aws_instance" "conditional_instance" {
  count              = var.create_web_server ? 1 : 0
  ami                = data.aws_ami.amazon_linux_2.id
  instance_type      = var.instance_type
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
  monitoring         = var.enable_monitoring # Enable/disable based on variable
  ebs_optimized      = var.enable_ebs_optimization

  tags = merge(
    var.tags,
    {
      Name        = "${var.instance_name_prefix}-conditional"
      Environment = var.environment
    }
  )
}

# Conditional attribute with ternary operator
resource "aws_instance" "conditional_type" {
  count = 1
  ami   = data.aws_ami.amazon_linux_2.id
  
  # Use large instance for prod, small for others
  instance_type      = var.environment == "prod" ? "t2.large" : "t2.small"
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  tags = merge(
    var.tags,
    {
      Name        = "${var.instance_name_prefix}-typed"
      Environment = var.environment
    }
  )
}

# Conditional with nested conditions
resource "aws_instance" "advanced_conditional" {
  count = (var.create_web_server && var.environment != "dev") ? 1 : 0
  ami   = data.aws_ami.amazon_linux_2.id
  
  # Conditions: prod=large, staging=medium, otherwise small
  instance_type = (
    var.environment == "prod" ? "t2.large" :
    var.environment == "staging" ? "t2.medium" :
    "t2.small"
  )
  
  monitoring        = var.environment != "dev" # Enable monitoring for non-dev
  ebs_optimized     = var.environment == "prod" # Only optimize for prod
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  tags = merge(
    var.tags,
    {
      Name        = "${var.instance_name_prefix}-advanced"
      Environment = var.environment
    }
  )
}

# ============================================================================
# EXAMPLE 6: AWS Lambda, SQS, and SNS Integration
# ============================================================================
# Demonstrates serverless architecture with event-driven messaging

# Create SNS topic for notifications
resource "aws_sns_topic" "notifications" {
  name = "${var.instance_name_prefix}-notifications"

  tags = merge(
    var.tags,
    {
      Name = "${var.instance_name_prefix}-sns-topic"
    }
  )
}

# Create SQS queue for message processing
resource "aws_sqs_queue" "tasks" {
  name                      = "${var.instance_name_prefix}-tasks"
  delay_seconds             = 0
  message_retention_seconds = 345600 # 4 days
  visibility_timeout_seconds = 30

  tags = merge(
    var.tags,
    {
      Name = "${var.instance_name_prefix}-sqs-queue"
    }
  )
}

# Subscribe SQS queue to SNS topic
resource "aws_sns_topic_subscription" "tasks_subscription" {
  topic_arn = aws_sns_topic.notifications.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.tasks.arn
}

# SQS queue policy to allow SNS to send messages
resource "aws_sqs_queue_policy" "tasks_policy" {
  queue_url = aws_sqs_queue.tasks.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "sns.amazonaws.com"
        }
        Action   = "sqs:SendMessage"
        Resource = aws_sqs_queue.tasks.arn
        Condition = {
          ArnEquals = {
            "aws:SourceArn" = aws_sns_topic.notifications.arn
          }
        }
      }
    ]
  })
}

# IAM role for Lambda function
resource "aws_iam_role" "lambda_role" {
  name = "${var.instance_name_prefix}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = var.tags
}

# IAM policy for Lambda to read from SQS
resource "aws_iam_role_policy" "lambda_sqs_policy" {
  name = "${var.instance_name_prefix}-lambda-sqs-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ]
        Resource = aws_sqs_queue.tasks.arn
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# Lambda function (using inline code for simplicity)
resource "aws_lambda_function" "task_processor" {
  filename         = "lambda_function.zip"
  function_name    = "${var.instance_name_prefix}-task-processor"
  role             = aws_iam_role.lambda_role.arn
  handler          = "index.handler"
  runtime          = "python3.11"
  source_code_hash = filebase64sha256("lambda_function.zip")

  environment {
    variables = {
      QUEUE_URL = aws_sqs_queue.tasks.url
    }
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.instance_name_prefix}-lambda"
    }
  )
}

# Event source mapping: Lambda triggered by SQS
resource "aws_lambda_event_source_mapping" "sqs_lambda" {
  event_source_arn = aws_sqs_queue.tasks.arn
  function_name    = aws_lambda_function.task_processor.function_name
  batch_size       = 10 # maximum number of messages Lambda retrieves from the SQS queue per invocation.
}

# CloudWatch Log Group for Lambda
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.task_processor.function_name}"
  retention_in_days = 7

  tags = var.tags
}

# ============================================================================
# Example SNS/SQS usage patterns
# ============================================================================

# Publish message to SNS topic
resource "aws_sns_topic_policy" "notifications_policy" {
  arn = aws_sns_topic.notifications.arn

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = "*"
        }
        Action   = "SNS:Publish"
        Resource = aws_sns_topic.notifications.arn
      }
    ]
  })
}

# ============================================================================
# EXAMPLE 7: AWS Fargate - Serverless Container Orchestration
# ============================================================================
# Demonstrates containerized app deployment on Fargate (no EC2 management)

# ECS Cluster for Fargate
resource "aws_ecs_cluster" "main" {
  name = "${var.instance_name_prefix}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.instance_name_prefix}-cluster"
    }
  )
}

# CloudWatch Log Group for ECS tasks
resource "aws_cloudwatch_log_group" "ecs_logs" {
  name              = "/ecs/${var.instance_name_prefix}"
  retention_in_days = 7

  tags = var.tags
}

# IAM role for ECS task execution
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "${var.instance_name_prefix}-ecs-task-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })

  tags = var.tags
}

# Attach execution role policy
resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# IAM role for ECS task (application)
resource "aws_iam_role" "ecs_task_role" {
  name = "${var.instance_name_prefix}-ecs-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })

  tags = var.tags
}

# Task role policy (example: S3 access)
resource "aws_iam_role_policy" "ecs_task_policy" {
  name = "${var.instance_name_prefix}-ecs-task-policy"
  role = aws_iam_role.ecs_task_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# ECS Task Definition for Fargate
resource "aws_ecs_task_definition" "app" {
  family                   = var.instance_name_prefix
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn      = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = var.instance_name_prefix
      image     = var.container_image
      cpu       = var.fargate_cpu
      memory    = var.fargate_memory
      essential = true

      portMappings = [
        {
          containerPort = var.container_port
          hostPort      = var.container_port
          protocol      = "tcp"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs_logs.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }

      environment = [
        {
          name  = "ENVIRONMENT"
          value = var.environment
        },
        {
          name  = "LOG_LEVEL"
          value = "INFO"
        }
      ]
    }
  ])

  tags = merge(
    var.tags,
    {
      Name = "${var.instance_name_prefix}-task"
    }
  )
}

# Security group for Fargate tasks
resource "aws_security_group" "fargate_sg" {
  name        = "${var.instance_name_prefix}-fargate-sg"
  description = "Security group for Fargate tasks"

  ingress {
    from_port   = var.container_port
    to_port     = var.container_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.instance_name_prefix}-fargate-sg"
    }
  )
}

# Get default VPC and subnets (for quick setup)
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Get available AZs in the region for replica distribution
data "aws_availability_zones" "available" {
  state = "available"
}

# ECS Service (Fargate launch type)
resource "aws_ecs_service" "app" {
  name            = "${var.instance_name_prefix}-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.ecs_desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = data.aws_subnets.default.ids
    security_groups  = [aws_security_group.fargate_sg.id]
    assign_public_ip = true
  }

  depends_on = [
    aws_iam_role_policy.ecs_task_policy
  ]

  tags = merge(
    var.tags,
    {
      Name = "${var.instance_name_prefix}-service"
    }
  )
}

# Auto-scaling target for ECS service
resource "aws_appautoscaling_target" "ecs_target" {
  max_capacity       = var.ecs_max_capacity
  min_capacity       = var.ecs_desired_count
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.app.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

# CPU scaling policy
resource "aws_appautoscaling_policy" "ecs_policy_cpu" {
  name               = "${var.instance_name_prefix}-cpu-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs_target.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value = 70.0
  }
}

# Memory scaling policy
resource "aws_appautoscaling_policy" "ecs_policy_memory" {
  name               = "${var.instance_name_prefix}-memory-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs_target.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageMemoryUtilization"
    }
    target_value = 80.0
  }
}

# ============================================================================
# EXAMPLE 8: AWS RDS MySQL with Read Replicas (2 replicas)
# ============================================================================
# Demonstrates multi-AZ RDS MySQL deployment with read replicas for high availability

# DB subnet group for RDS
resource "aws_db_subnet_group" "mysql" {
  name       = "${var.instance_name_prefix}-mysql-subnet-group"
  subnet_ids = data.aws_subnets.default.ids

  tags = merge(
    var.tags,
    {
      Name = "${var.instance_name_prefix}-mysql-subnet-group"
    }
  )
}

# Security group for RDS MySQL
resource "aws_security_group" "rds_mysql_sg" {
  name        = "${var.instance_name_prefix}-rds-mysql-sg"
  description = "Security group for RDS MySQL"

  # Allow MySQL/Aurora from within VPC
  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # In production, restrict to your VPC CIDR
  }

  # Allow MySQL/Aurora from EC2 security group
  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.ec2_sg.id, aws_security_group.fargate_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.instance_name_prefix}-rds-mysql-sg"
    }
  )
}

# Primary RDS MySQL instance
resource "aws_db_instance" "mysql_primary" {
  identifier              = "${var.instance_name_prefix}-mysql-primary"
  engine                  = "mysql"
  engine_version          = "8.0"
  instance_class          = "db.t3.micro"
  allocated_storage       = 20
  storage_type            = "gp2"
  storage_encrypted       = true
  
  # Credentials (use AWS Secrets Manager in production)
  db_name  = "appdb"
  username = "admin"
  password = "YourSecurePassword123!" # Change this to a strong password
  
  # Backup configuration
  backup_retention_period = 7
  backup_window           = "03:00-04:00"
  maintenance_window      = "mon:04:00-mon:05:00"
  copy_tags_to_snapshot   = true
  
  # Multi-AZ for high availability
  multi_az = true
  
  # Database settings
  db_subnet_group_name            = aws_db_subnet_group.mysql.name
  vpc_security_group_ids          = [aws_security_group.rds_mysql_sg.id]
  publicly_accessible             = false
  skip_final_snapshot             = false
  final_snapshot_identifier       = "${var.instance_name_prefix}-mysql-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"
  
  # Performance insights (optional, available on t3 and larger)
  performance_insights_enabled    = true
  performance_insights_retention_period = 7
  
  # Enable CloudWatch logs exports
  enabled_cloudwatch_logs_exports = ["audit", "error", "general", "slowquery"]
  
  # Deletion protection
  deletion_protection = false # Set to true in production
  
  # Parameter group
  parameter_group_name = aws_db_parameter_group.mysql.name

  tags = merge(
    var.tags,
    {
      Name = "${var.instance_name_prefix}-mysql-primary"
      Role = "Primary"
    }
  )

  depends_on = [aws_db_subnet_group.mysql]
}

# DB Parameter Group for MySQL
resource "aws_db_parameter_group" "mysql" {
  name   = "${var.instance_name_prefix}-mysql-params"
  family = "mysql8.0"

  # Custom parameters for replication
  parameter {
    name  = "binlog_format"
    value = "ROW"
    apply_method = "immediate"
  }

  parameter {
    name  = "max_allowed_packet"
    value = "16777216"
    apply_method = "immediate"
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.instance_name_prefix}-mysql-params"
    }
  )
}

# Read Replica 1 (same AZ as primary)
resource "aws_db_instance" "mysql_replica_1" {
  identifier             = "${var.instance_name_prefix}-mysql-replica-1"
  replicate_source_db    = aws_db_instance.mysql_primary.identifier
  instance_class         = "db.t3.micro"
  availability_zone      = data.aws_availability_zones.available.names[0]
  
  # Replica-specific settings
  publicly_accessible = false
  storage_encrypted   = true
  
  # Auto-minor version upgrade
  auto_minor_version_upgrade = true
  
  # Skip final snapshot for replicas (optional)
  skip_final_snapshot = true

  tags = merge(
    var.tags,
    {
      Name = "${var.instance_name_prefix}-mysql-replica-1"
      Role = "Replica"
    }
  )

  depends_on = [aws_db_instance.mysql_primary]
}

# Read Replica 2 (different AZ for geographic redundancy)
resource "aws_db_instance" "mysql_replica_2" {
  identifier             = "${var.instance_name_prefix}-mysql-replica-2"
  replicate_source_db    = aws_db_instance.mysql_primary.identifier
  instance_class         = "db.t3.micro"
  availability_zone      = data.aws_availability_zones.available.names[1]
  
  # Replica-specific settings
  publicly_accessible  = false
  storage_encrypted    = true
  
  # Auto-minor version upgrade
  auto_minor_version_upgrade = true
  
  # Skip final snapshot for replicas (optional)
  skip_final_snapshot = true

  tags = merge(
    var.tags,
    {
      Name = "${var.instance_name_prefix}-mysql-replica-2"
      Role = "Replica"
    }
  )

  depends_on = [aws_db_instance.mysql_primary]
}

# Optional: Create an RDS Proxy for connection pooling and failover
resource "aws_db_proxy" "mysql_proxy" {
  name                   = "${var.instance_name_prefix}-mysql-proxy"
  engine_family          = "MYSQL"
  auth {
    auth_scheme = "SECRETS"
    secret_arn  = aws_secretsmanager_secret.rds_secret.arn
  }
  role_arn               = aws_iam_role.rds_proxy_role.arn
  vpc_subnet_ids         = data.aws_subnets.default.ids
  vpc_security_group_ids = [aws_security_group.rds_mysql_sg.id]
  
  # Connection settings
  max_connections              = 100
  max_idle_connections         = 50
  connection_borrow_timeout    = 120
  session_pinning_filters      = ["EXCLUDE_VARIABLE_SETS"]
  init_query                   = ""
  
  # Logging
  enable_iam_auth           = true
  debug_logging             = false
  require_tls               = false

  tags = merge(
    var.tags,
    {
      Name = "${var.instance_name_prefix}-mysql-proxy"
    }
  )

  depends_on = [aws_iam_role_policy.rds_proxy_policy]
}

# RDS Proxy target group for primary instance
resource "aws_db_proxy_target_group" "mysql_tg" {
  name          = "${var.instance_name_prefix}-mysql-tg"
  db_proxy_name = aws_db_proxy.mysql_proxy.name
  target_arn    = aws_db_instance.mysql_primary.arn

  connection_pool_config {
    max_connections              = 100
    max_idle_connections         = 50
    connection_borrow_timeout    = 120
    session_pinning_filters      = ["EXCLUDE_VARIABLE_SETS"]
  }
}

# Secrets Manager for RDS credentials
resource "aws_secretsmanager_secret" "rds_secret" {
  name                    = "${var.instance_name_prefix}/rds/mysql/admin"
  description             = "RDS MySQL admin credentials"
  recovery_window_in_days = 7

  tags = var.tags
}

resource "aws_secretsmanager_secret_version" "rds_secret_version" {
  secret_id = aws_secretsmanager_secret.rds_secret.id
  secret_string = jsonencode({
    username = aws_db_instance.mysql_primary.username
    password = aws_db_instance.mysql_primary.password
  })
}

# IAM role for RDS Proxy
resource "aws_iam_role" "rds_proxy_role" {
  name = "${var.instance_name_prefix}-rds-proxy-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "rds.amazonaws.com"
        }
      }
    ]
  })

  tags = var.tags
}

# IAM policy for RDS Proxy to access Secrets Manager
resource "aws_iam_role_policy" "rds_proxy_policy" {
  name = "${var.instance_name_prefix}-rds-proxy-policy"
  role = aws_iam_role.rds_proxy_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = aws_secretsmanager_secret.rds_secret.arn
      },
      {
        Effect = "Allow"
        Action = [
          "kms:Decrypt"
        ]
        Resource = "*"
        Condition = {
          StringEquals = {
            "kms:ViaService" = "secretsmanager.${var.aws_region}.amazonaws.com"
          }
        }
      }
    ]
  })
}
