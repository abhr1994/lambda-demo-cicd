from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_lambda,
    aws_lambda_event_sources as lambda_event_sources
)


class LambdaDemoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a Queue
        queue = sqs.Queue(
            self, "LambdaDemoQueue",
            visibility_timeout=Duration.seconds(300),
        )

        # topic = sns.Topic(
        #     self, "LambdaDemoTopic"
        # )
        # topic.add_subscription(subs.SqsSubscription(queue))

        # Create a lambda function
        lambda_function = aws_lambda.Function(self, "SQSLambda", handler='lambda_handler.handler',
                                              runtime=aws_lambda.Runtime.PYTHON_3_10,
                                              code=aws_lambda.Code.from_asset('lambda_code'))

        # Create event source
        sqs_event_source = lambda_event_sources.SqsEventSource(queue)

        # Add event source to lambda
        lambda_function.add_event_source(sqs_event_source)

