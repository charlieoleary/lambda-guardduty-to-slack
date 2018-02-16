#!/usr/bin/env python3.6
from awacs import aws, sts
from troposphere import GetAtt, Join, Parameter, Ref, Template, awslambda, iam
from troposphere.events import Rule, Target
from troposphere.awslambda import Environment, Function
from troposphere import GetAtt, Join

t = Template()

t.add_version("2010-09-09")
t.add_description("GuardDuty to Slack Lambda bridge - https://github.com/GlorifiedTypist/lambda-guardduty-to-slack")

ParamLambdaS3SrcBucket = t.add_parameter(Parameter(
    "LambdaS3SrcBucket",
    Default="lambda-code",
    Type="String",
    Description="Name of the bucket where lambda function sources is stored"
))

ParamLambdaZipFilename = t.add_parameter(Parameter(
    "LambdaZipFilename",
    Default="cloudwatch-to-slack.zip",
    Type="String",
    Description="Name of the ZIP file with lambda function sources inside S3 bucket"
))

ParamSlackChannel = t.add_parameter(Parameter(
    "ParamSlackChannel",
    Default="lambda",
    Type="String",
    Description="Name of slack channel to send notifications"
))

ParamSlackHookUrl = t.add_parameter(Parameter(
    "ParamSlackHookUrl",
    Default="https://hooks.slack.com/services/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",
    Type="String",
    Description="Slack API hook URL"
))

# Create the Lambda function
GuardDutyToSlackFunction = t.add_resource(Function(
    "GuardDutyToSlackFunction",
    DependsOn='GuardDutyToSlackLambdaRole',
    Code=awslambda.Code(
        S3Bucket=Ref(ParamLambdaS3SrcBucket),
        S3Key=Ref(ParamLambdaZipFilename)
    ),
    Environment=Environment(
        Variables={
            'slackChannel': Ref(ParamSlackChannel),
            'kmsEncryptedHookUrl': Ref(ParamSlackHookUrl),
        }
    ),
    Handler="src.lambda_function.lambda_handler",
    MemorySize=128,
    Role=GetAtt("GuardDutyToSlackLambdaRole", "Arn"),
    Runtime="python3.6",
    Timeout=10
))

# Create lambda function role
GuardDutyToSlackLambdaRole = t.add_resource(iam.Role(
    "GuardDutyToSlackLambdaRole",
    AssumeRolePolicyDocument=aws.Policy(
        Statement=[
            aws.Statement(
                Effect=aws.Allow,
                Action=[sts.AssumeRole],
                Principal=aws.Principal(
                    "Service", ["lambda.amazonaws.com"]
                )
            )
        ]
    ),
    Path= "/service-role/",
    ManagedPolicyArns=[
        'arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess',
        'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole',
        'arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole'
        ],
    Policies=[
        iam.Policy(
            PolicyName="LambdaPolicy",
            PolicyDocument=aws.Policy(
                Statement=[
                    aws.Statement(
                        Effect=aws.Allow,
                        Action=[
                            aws.Action("logs", "CreateLogGroup"),
                            aws.Action("logs", "CreateLogStream"),
                            aws.Action("logs", "PutLogEvents"),
                        ],
                        Resource=["arn:aws:logs:*:*:*"]
                    )
                ]
            )
        )
    ]
))

# Create the Event Target
GuardDutyEventTarget = Target(
    "GuardDutyEventTarget",
    Arn=GetAtt('GuardDutyToSlackFunction', 'Arn'),
    Id="GuardDutyToSlackFunction"
)

# Create the Event Rule
GuardDutyEventRule = t.add_resource(Rule(
    "GuardDutyEventRule",
    EventPattern={
        "source": [
            "aws.guardduty"
        ],
        "detail-type": [
          "GuardDuty Finding"
        ]
    },
    Description="GuardDuty CloudWatch Event Rule",
    State="ENABLED",
    Targets=[GuardDutyEventTarget]
))

# Create invoke Permission
APILambdaPermission = t.add_resource(awslambda.Permission(
    "APILambdaPermission",
    DependsOn="GuardDutyToSlackFunction",
    Action="lambda:InvokeFunction",
    FunctionName=GetAtt('GuardDutyToSlackFunction', 'Arn'),
    Principal="events.amazonaws.com",
    SourceArn=GetAtt('GuardDutyEventRule', 'Arn')
))


print t.to_json()

