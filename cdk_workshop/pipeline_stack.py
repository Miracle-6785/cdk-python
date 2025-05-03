from aws_cdk import Stack
from aws_cdk import pipelines as pipelines
from constructs import Construct

# arn:aws:codeconnections:ap-southeast-1:637423223528:connection/2d86ea02-e6cf-4f33-893a-714c7818686c


class WorkshopPipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.connection(
                    repo_string="Miracle-6785/cdk-python",
                    branch="main",
                    connection_arn="arn:aws:codeconnections:ap-southeast-1:637423223528:connection/2d86ea02-e6cf-4f33-893a-714c7818686c",
                ),
                commands=[
                    "npm install -g aws-cdk",  # Installs the cdk cli on Codebuild
                    "pip install uv",
                    "uv sync",
                    "pwd",
                    "ls -la",
                    # "bash -c 'source .venv/bin/activate && cdk synth'",
                ],
            ),
        )
