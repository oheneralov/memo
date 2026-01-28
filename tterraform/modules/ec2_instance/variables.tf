variable "instance_name" {
  description = "Name of the EC2 instance"
  type        = string
  default     = "web-server-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.small"
}

variable "ami_id" {
  description = "AMI ID for the instance"
  type        = string
  default     = "" # Will be set from data source in main.tf of module
}

variable "security_group_ids" {
  description = "List of security group IDs"
  type        = list(string)
  default     = [] # Will be set from resource in main.tf of module
}

variable "tags" {
  description = "Tags to apply to the instance"
  type        = map(string)
  default = {
    Role = "webserver"
  }
}

