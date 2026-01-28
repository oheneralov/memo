# Terraform AWS EC2 Configuration

This repository contains Terraform configuration examples for creating EC2 instances on AWS, demonstrating different approaches and best practices.

## Overview

The configuration includes:
- **Data sources** to fetch AWS resources
- **Resources** to create EC2 instances and security groups
- **Variables** to parameterize the configuration
- **Outputs** to expose created resource information
- **Modules** for reusable infrastructure patterns
- **Multiple examples** showing count, for_each, and module usage

---

## Terraform Blocks & Fields Explained

### 1. **terraform Block**
```terraform
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.0"
}
```
- **Declares Terraform settings** and requirements
- **`required_providers`** - Lists required providers (AWS) with their source and version
- **`required_version`** - Specifies minimum Terraform version needed

### 2. **provider Block**
```terraform
provider "aws" {
  region = var.aws_region
}
```
- **Configures the AWS provider** with credentials and settings
- **`region`** - AWS region where resources will be created

### 3. **data Block** (Data Source)
```terraform
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}
```
- **Fetches existing AWS resources** without creating them
- **`most_recent`** - Returns the latest matching AMI
- **`owners`** - Filter by owner (amazon = AWS official)
- **`filter`** - Search criteria (filters available AMIs by name)
- **Usage:** Reference with `data.aws_ami.amazon_linux_2.id`

### 4. **resource Block**
```terraform
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
```
- **Creates or manages AWS resources**
- **`resource "aws_instance" "ec2_instances"`** - Type is `aws_instance`, name is `ec2_instances`
- **Common fields:**
  - **`ami`** - Amazon Machine Image ID (OS)
  - **`instance_type`** - EC2 instance size (t2.small, t2.medium, etc.)
  - **`vpc_security_group_ids`** - Security group(s) for network rules
  - **`tags`** - Metadata tags for organizing resources

### 5. **count Meta-argument** (Example 1)
```terraform
resource "aws_instance" "ec2_instances" {
  count = var.instance_count
  # ... other config
}
```
- **Creates multiple similar resources** based on a number
- **`count.index`** - Zero-based index (0, 1, 2, ...)
- **`count.value`** - The count value
- **Reference:** `aws_instance.ec2_instances[0].id` or `aws_instance.ec2_instances[*].id`
- **Use when:** Simple number-based repetition

### 6. **for_each Meta-argument** (Examples 2 & 3)
```terraform
resource "aws_instance" "ec2_instances_foreach" {
  for_each = var.instances_config  # Map or set

  instance_type = each.value.instance_type
  # ... other config
}
```
- **Creates multiple resources** from a map or set
- **`each.key`** - Current key (e.g., "web-server-1")
- **`each.value`** - Current value (e.g., {instance_type: "t2.small"})
- **Reference:** `aws_instance.ec2_instances_foreach["web-server-1"].id`
- **Use when:** Different configurations per instance or meaningful identifiers

### 7. **variable Block**
```terraform
variable "instance_count" {
  description = "Number of EC2 instances to create"
  type        = number
  default     = 1
}
```
- **Defines input variables** for the configuration
- **`description`** - Explains the variable's purpose
- **`type`** - Data type (string, number, list, map, object, etc.)
- **`default`** - Default value if not provided
- **Usage:** Reference with `var.instance_count`

### 8. **output Block**
```terraform
output "instance_ids" {
  description = "IDs of the created EC2 instances"
  value       = aws_instance.ec2_instances[*].id
}
```
- **Exposes values** from the configuration
- **`value`** - What to output (can be resource attributes)
- **`[*]` operator** - Splat syntax to get all instances' attributes
- **Usage:** Displayed after `terraform apply` and accessible via `terraform output`

### 9. **module Block**
```terraform
module "web_server" {
  source = "./modules/ec2_instance"

  instance_name      = "web-server-1"
  instance_type      = "t2.small"
  ami_id             = data.aws_ami.amazon_linux_2.id
  security_group_ids = [aws_security_group.ec2_sg.id]
}
```
- **Calls a reusable module** (defined in a subdirectory)
- **`source`** - Path to the module
- **Named arguments** - Variables passed to the module
- **Reference outputs:** `module.web_server.instance_id`
- **Use when:** Reusing infrastructure patterns

---

## File Structure

```
tterraform/
├── provider.tf              # AWS provider configuration
├── variables.tf             # Input variables
├── main.tf                  # Resources and data sources
├── outputs.tf               # Output values
├── terraform.tfvars.example # Example variable values
├── .gitignore               # Git ignore patterns
└── modules/
    └── ec2_instance/        # Reusable EC2 module
        ├── variables.tf
        ├── main.tf
        └── outputs.tf
```

---

## Key Functions & Operators

### **merge()**
```terraform
tags = merge(var.tags, {Name = "my-instance"})
```
- Combines multiple maps/objects into one
- Later values override earlier ones

### **toset()**
```terraform
for_each = toset(var.instance_names)
```
- Converts a list to a set (required for `for_each` with lists)

### **Splat Operator `[*]`**
```terraform
value = aws_instance.ec2_instances[*].id
```
- Extracts attribute from all instances
- Returns a list of values

### **String Interpolation `${}`**
```terraform
Name = "${var.instance_name_prefix}-${count.index + 1}"
```
- Embeds variables/expressions within strings

---

## Usage

### 1. Initialize Terraform
```bash
terraform init
```

### 2. Create terraform.tfvars
```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your desired values
```

### 3. Plan the deployment
```bash
terraform plan
```

### 4. Apply the configuration
```bash
terraform apply
```

### 5. View outputs
```bash
terraform output
```

### 6. Destroy resources
```bash
terraform destroy
```

---

## Examples Overview

### Example 1: count
- Creates N instances based on `instance_count` variable
- All instances have identical configuration
- Simple but less flexible for mixed configurations

### Example 2: for_each with map
- Creates instances with different types and tags
- Uses `var.instances_config` (web-server, db-server, etc.)
- Each instance has its own configuration

### Example 3: for_each with list
- Creates instances from a list of names
- All instances have same type (uses `var.instance_names`)
- Simpler than Example 2 when uniform configuration needed

### Example 4: module
- Reusable EC2 instance module
- Demonstrates single module call and module with `for_each`
- Promotes code reusability

---

## Security Considerations

⚠️ **Current Security Group:** Allows SSH (port 22) from anywhere (`0.0.0.0/0`)
- Use in development/learning only
- Restrict to specific IPs in production: `cidr_blocks = ["YOUR_IP/32"]`

---

## Resources

- [Terraform AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Language Reference](https://www.terraform.io/language)
- [EC2 Instance Resource](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance)
