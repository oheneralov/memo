output "instance_ids" {
  description = "IDs of the created EC2 instances"
  value       = aws_instance.ec2_instances[*].id
}

output "instance_public_ips" {
  description = "Public IP addresses of the created EC2 instances"
  value       = aws_instance.ec2_instances[*].public_ip
}

output "instance_private_ips" {
  description = "Private IP addresses of the created EC2 instances"
  value       = aws_instance.ec2_instances[*].private_ip
}

output "security_group_id" {
  description = "ID of the security group"
  value       = aws_security_group.ec2_sg.id
}

output "ami_id" {
  description = "AMI ID used for instances"
  value       = data.aws_ami.amazon_linux_2.id
}
