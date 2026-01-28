variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "instance_count" {
  description = "Number of EC2 instances to create"
  type        = number
  default     = 1
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.small"
}

variable "ami_id" {
  description = "AMI ID to use for EC2 instances (defaults to Amazon Linux 2)"
  type        = string
  default     = "" # Will be populated by data source in main.tf
}

variable "instance_name_prefix" {
  description = "Prefix for instance names"
  type        = string
  default     = "ec2-instance"
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default = {
    Environment = "dev"
    ManagedBy   = "terraform"
  }
}

# ============================================================================
# Variables for for_each examples
# ============================================================================

variable "instances_config" {
  description = "Configuration for each EC2 instance using for_each with map"
  type        = map(object({
    instance_type = string
    tags          = optional(map(string))
  }))
  default = {
    "web-server-1" = {
      instance_type = "t2.small"
      tags = {
        Role = "webserver"
      }
    }
    "web-server-2" = {
      instance_type = "t2.small"
      tags = {
        Role = "webserver"
      }
    }
    "db-server-1" = {
      instance_type = "t2.medium"
      tags = {
        Role = "database"
      }
    }
  }
}

variable "instance_names" {
  description = "Names of EC2 instances to create using for_each with list"
  type        = list(string)
  default     = ["app-server-1", "app-server-2", "app-server-3"]
}

# ============================================================================
# Variables for conditional examples
# ============================================================================

variable "enable_monitoring" {
  description = "Enable CloudWatch monitoring for instances"
  type        = bool
  default     = true
}

variable "enable_ebs_optimization" {
  description = "Enable EBS optimization for instances"
  type        = bool
  default     = false
}

variable "environment" {
  description = "Environment type (dev, staging, prod)"
  type        = string
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "create_web_server" {
  description = "Whether to create the web server module"
  type        = bool
  default     = true
}

# ============================================================================
# Variables for Lambda/SQS/SNS examples
# ============================================================================

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "task-processor"
}

variable "sqs_visibility_timeout" {
  description = "SQS message visibility timeout in seconds"
  type        = number
  default     = 30
  
  validation {
    condition     = var.sqs_visibility_timeout >= 0 && var.sqs_visibility_timeout <= 43200
    error_message = "Visibility timeout must be between 0 and 43200 seconds."
  }
}

variable "lambda_batch_size" {
  description = "Batch size for Lambda processing SQS messages"
  type        = number
  default     = 10
  
  validation {
    condition     = var.lambda_batch_size >= 1 && var.lambda_batch_size <= 10
    error_message = "Batch size must be between 1 and 10."
  }
}

# ============================================================================
# Variables for Fargate examples
# ============================================================================

variable "container_image" {
  description = "Docker image URI for ECS task"
  type        = string
  default     = "nginx:latest"
  # Example: "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest"
}

variable "container_port" {
  description = "Port exposed by container"
  type        = number
  default     = 80
}

variable "fargate_cpu" {
  description = "Fargate CPU units (256, 512, 1024, 2048, 4096)"
  type        = number
  default     = 256
  
  validation {
    condition     = contains([256, 512, 1024, 2048, 4096], var.fargate_cpu)
    error_message = "CPU must be one of: 256, 512, 1024, 2048, 4096."
  }
}

variable "fargate_memory" {
  description = "Fargate memory in MB (512, 1024, 2048, 3072, 4096, etc.)"
  type        = number
  default     = 512
  
  validation {
    condition     = var.fargate_memory >= 512 && var.fargate_memory <= 30720
    error_message = "Memory must be between 512 and 30720 MB."
  }
}

variable "ecs_desired_count" {
  description = "Desired number of ECS tasks"
  type        = number
  default     = 1
}

variable "ecs_max_capacity" {
  description = "Maximum number of ECS tasks for auto-scaling"
  type        = number
  default     = 4
}
