# lambda-guardduty-to-slack

### [AWS GuardDuty][guardduty_link]

Flagship threat detection service for the cloud which continuously monitors and protects AWS accounts, along with the applications and services running within them.

 - Detects known and unknown threats (Zero-Days)
 - Makes use of artificial intelligence and machine learning from a large sample base
 - Integrated threat intelligence
 - Fire and forget

### [Troposphere][troposphere_link] & [CloudFormation][cloudformation_link]

 - True IaC, preview changes, rollback triggers
 - Portable, flexible and repeatable
 - Native CI/CD integration

### Prerequisites

**Python 3.6**

Python Dependencies:

 - virtualenv
 - awacs
 - troposphere
 - requests
 - boto3

### Infrastructure Resource Overview

#### Not covered in the stack scripts and must be provided for a successful deployment:

* **S3 Bucket** with appropriate permissions, if not IAM permissions assigned CF will assume the logged in deployment users IAM users permissions
* **Slack Incoming Webhook** has been setup and assigned to a channel. Further info and a setup guide can be found [here][slack_webhook_link]

#### The stack scripts brings the following resources up during deployment:

* **GuardDutyToSlackFunction** (``AWS::Lambda::Function``): approx 10Mb zip of code and dependancies.
* **GuardDutyToSlackLambaRole** (``AWS::IAM::Role``): minimal access to required permissions:
 - (``AWSXrayWriteOnlyAccess``): gathers meta-data of various requests between compute resources in the application flow
 - (``AWSLambdaBasicExecutionRole``): grants permission to Lambda to run as well as calls from CloudWatch
 - (``AWSLambdaVPCAccessExecutionRole``): allows Lambda to write to CloudWatch logs
* **GuardDutyEventRule** (``AWS::Events::Rule``): routes Guardduty specific event to the Lambda function for processing
* **APILambdaPermission** (``AWS::Lambda::Permission``): allows versioning of code updates and abstracting updates from testing environments into production

### Deployment Guide



[troposphere_link]: https://github.com/cloudtools/troposphere
[cloudformation_link]: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html
[guardduty_link]: https://aws.amazon.com/guardduty/
[slack_webhook_link]: https://my.slack.com/services/new/incoming-webhook/
[lambda_perms_link]: https://docs.aws.amazon.com/lambda/latest/dg/intro-permission-model.html

