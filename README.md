# sls-guardduty-slack-notifications

Based on the work by [GlorifiedTypist](https://github.com/GlorifiedTypist/lambda-guardduty-to-slack), but deployed with the Serverless Framework.

## [AWS GuardDuty](https://aws.amazon.com/guardduty)

Flagship threat detection service for the cloud which continuously monitors and protects AWS accounts, along with the applications and services running within them.

- Detects known and unknown threats (Zero-Days)
- Makes use of artificial intelligence and machine learning from a large sample base
- Integrated threat intelligence
- Fire and forget

## [Serverless Framework](https://serverless.com)

- Simplifed framework on top of CloudFormation
- Enabls versioned deployments, managed secrets, etc.

## Deployment Guide

### Configuration

Refer to the `serverless.yml` file for all configuration options.

You will need to create a Slack webhook and an appropriate SSM path for it. The following parameters
are expected:

`/serverless/guardDutyNotifications/SLACK_WEBHOOK` - The webhook that will receive the POST.
`/serverless/guardDutyNotifications/SLACK_CHANNEL` - The channel the message will be sent to.

The `stage` and `region` parameters can be customized based on your use case.

### Deploying the Stack

- Install the Serverless Framework.
- Run `npm install` to install the `serverless-python-requirements` plugin.
- Run `sls deploy` to deploy your function.

### Resources

### License

GNU GENERAL PUBLIC LICENSE - Version 3, 29 June 2007

Huge thanks to [GlorifiedTypist](https://github.com/GlorifiedTypist/lambda-guardduty-to-slack) who
created the original script. Almost no modifications were made to the handler, and that it is
completely thanks to them that this exists.
