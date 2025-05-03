from aws_cdk import CfnOutput, Duration, Stack
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as subs
from aws_cdk import aws_sqs as sqs
from cdk_dynamo_table_view import TableViewer
from constructs import Construct

from cdk_workshop.hitcounter import HitCounter


class CdkWorkshopStack(Stack):

    @property
    def hc_endpoint(self):
        return self._hc_endpoint

    @property
    def hc_viewer_url(self):
        return self._hc_viewer_url

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_lambda = _lambda.Function(
            self,
            "HelloHandler",
            runtime=_lambda.Runtime.PYTHON_3_13,
            code=_lambda.Code.from_asset("lambda"),
            handler="hello.handler",
        )

        hello_with_counter = HitCounter(self, "HelloHitCounter", downstream=my_lambda)

        gateway = apigw.LambdaRestApi(
            self, "gwHello", handler=hello_with_counter.handler
        )

        tv = TableViewer(
            self, "ViewHitCounter", title="Hello Hits", table=hello_with_counter.table
        )

        self._hc_endpoint = CfnOutput(self, "GatewayUrl", value=gateway.url)

        self._hc_viewer_url = CfnOutput(self, "TableViewerUrl", value=tv.endpoint)
