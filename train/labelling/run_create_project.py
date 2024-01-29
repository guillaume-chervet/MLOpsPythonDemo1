import argparse
import asyncio
from create_project import CreateProject, create_ecotag_project

parser = argparse.ArgumentParser("labelling")
parser.add_argument("--subscription_id", type=str)
parser.add_argument("--resource_group_name", type=str)
parser.add_argument("--workspace_name", type=str)
parser.add_argument("--dataset_version", type=str)
parser.add_argument("--dataset_name", type=str)
parser.add_argument("--api_url", type=str)
parser.add_argument(
    "--token_endpoint",
    type=str,
    default="https://demo.duendesoftware.com/connect/token",
)
parser.add_argument("--client_id", type=str, default="m2m")
parser.add_argument("--client_secret", type=str, default="secret")

args = parser.parse_args()
subscription_id = args.subscription_id
resource_group_name = args.resource_group_name
workspace_name = args.workspace_name
dataset_version = args.dataset_version
dataset_name = args.dataset_name
api_url = args.api_url
token_endpoint = args.token_endpoint
client_id = args.client_id
client_secret = args.client_secret


async def main():
    create_project = CreateProject(api_url=api_url,
                                   token_endpoint=token_endpoint,
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   subscription_id=subscription_id,
                                   resource_group_name=resource_group_name,
                                   workspace_name=workspace_name,
                                   dataset_name=dataset_name,
                                   dataset_version=dataset_version)
    await create_ecotag_project(create_project)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
