# Lambda/SQS/SNS Example Setup

This document explains how to use the Lambda, SQS, and SNS examples in the Terraform configuration.

## Architecture

```
SNS Topic
    ↓
SNS Subscription (SQS)
    ↓
SQS Queue
    ↓
Lambda Event Source Mapping
    ↓
Lambda Function (Task Processor)
    ↓
CloudWatch Logs
```

## Components

### 1. **SNS Topic** (`aws_sns_topic`)
- Publishes messages to subscribers
- Named: `ec2-instance-notifications`
- Use case: Distribute notifications to multiple services

### 2. **SQS Queue** (`aws_sqs_queue`)
- Stores messages for reliable processing
- Named: `ec2-instance-tasks`
- Features:
  - 4-day message retention
  - 30-second visibility timeout
  - Receives messages from SNS topic

### 3. **SNS to SQS Subscription** (`aws_sns_topic_subscription`)
- Connects SNS topic to SQS queue
- Messages published to SNS are automatically sent to SQS

### 4. **Lambda Function** (`aws_lambda_function`)
- Processes messages from SQS queue
- Runtime: Python 3.11
- Handler: `index.handler`
- Receives batch of messages from SQS

### 5. **Lambda Event Source Mapping** (`aws_lambda_event_source_mapping`)
- Triggers Lambda automatically when messages arrive in SQS
- Batch size: 10 messages per invocation
- Lambda polls SQS queue and processes messages

### 6. **IAM Roles & Policies**
- Lambda role: Allows Lambda to assume role
- Lambda policy: Allows:
  - Reading from SQS queue
  - Deleting processed messages
  - Writing to CloudWatch Logs

### 7. **CloudWatch Logs** (`aws_cloudwatch_log_group`)
- Captures Lambda logs
- Retention: 7 days
- Log group: `/aws/lambda/ec2-instance-task-processor`

## Setup Instructions

### 1. Prepare Lambda Function

The example uses a ZIP file. To create it:

```bash
# On Windows PowerShell
cd c:\alex\work\memo\tterraform

# Create a zip file with the Lambda function
Compress-Archive -Path lambda_function.py -DestinationPath lambda_function.zip -Force
```

On Linux/Mac:
```bash
cd /path/to/tterraform
zip lambda_function.zip lambda_function.py
```

### 2. Initialize and Apply

```bash
terraform init
terraform plan
terraform apply
```

### 3. Test the Setup

Publish a message to SNS (it will automatically go to SQS and trigger Lambda):

```bash
aws sns publish \
  --topic-arn arn:aws:sns:us-east-1:ACCOUNT_ID:ec2-instance-notifications \
  --message '{"task":"process_data","data":"example"}'
```

Or send directly to SQS:

```bash
aws sqs send-message \
  --queue-url https://sqs.us-east-1.amazonaws.com/ACCOUNT_ID/ec2-instance-tasks \
  --message-body '{"task":"process_data","data":"example"}'
```

### 4. Monitor Execution

View Lambda logs:

```bash
aws logs tail /aws/lambda/ec2-instance-task-processor --follow
```

## Key Terraform Concepts Used

### `jsonencode()`
Converts Terraform objects to JSON strings for policies:
```terraform
policy = jsonencode({
  Version = "2012-10-17"
  Statement = [...]
})
```

### `filebase64sha256()`
Computes hash of Lambda ZIP for change detection:
```terraform
source_code_hash = filebase64sha256("lambda_function.zip")
```

### Environment Variables
Pass data to Lambda:
```terraform
environment {
  variables = {
    QUEUE_URL = aws_sqs_queue.tasks.url
  }
}
```

### Event Source Mapping
Connects resources with event triggers:
```terraform
resource "aws_lambda_event_source_mapping" "sqs_lambda" {
  event_source_arn = aws_sqs_queue.tasks.arn
  function_name    = aws_lambda_function.task_processor.function_name
  batch_size       = 10
}
```

## Variables for Customization

Update in `terraform.tfvars`:

```hcl
# Lambda batch processing size
lambda_batch_size = 10

# SQS message visibility timeout
sqs_visibility_timeout = 30

# Lambda function name
lambda_function_name = "task-processor"
```

## Troubleshooting

**Lambda not being triggered:**
- Check SQS queue policy allows SNS to send messages
- Verify Lambda event source mapping is created
- Check Lambda execution role has SQS permissions

**Messages not appearing in SQS:**
- Verify SNS topic subscription exists
- Check SQS queue policy
- Ensure SNS publishing is working

**Lambda execution errors:**
- Check Lambda logs in CloudWatch
- Verify environment variables are set
- Check IAM role permissions

## Extensions

You can extend this by:
- Adding DLQ (Dead Letter Queue) for failed messages
- Multiple Lambda functions for different message types
- SNS to Email subscription for notifications
- S3 triggers for file processing
- API Gateway to publish messages via HTTP
