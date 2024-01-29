import argparse
import asyncio
from dataclasses import dataclass

from ecotag_sdk.ecotag import get_access_token, ApiInformation, create_dataset, Dataset, Project, create_project, Label

from dataset import download


@dataclass
class DownloadAndCreateLabellingProject:
    labelling_api_url = "https://axaguildev-ecotag.azurewebsites.net/api/server"
    oidc_token_endpoint = "https://demo.duendesoftware.com/connect/token"
    oidc_client_id = "m2m"
    oidc_client_secret = "secret"
    subscription_id: str
    resource_group_name: str
    workspace_name: str


def download_and_create_labelling_project(
        dataset_version: str,
        dataset_name: str,
        download_and_create_labelling_project: DownloadAndCreateLabellingProject):
    async def create_project_async():
        subscription_id = download_and_create_labelling_project.subscription_id
        resource_group_name = download_and_create_labelling_project.resource_group_name
        workspace_name = download_and_create_labelling_project.workspace_name
        labelling_api_url = download_and_create_labelling_project.labelling_api_url
        oidc_token_endpoint = download_and_create_labelling_project.oidc_token_endpoint
        oidc_client_id = download_and_create_labelling_project.oidc_client_id
        oidc_client_secret = download_and_create_labelling_project.oidc_client_secret
        dataset_path = download(subscription_id, resource_group_name, workspace_name, dataset_name, dataset_version)

        create_project = CreateProject(
            dataset_directory=dataset_path,
            dataset_version=dataset_version,
            api_url=labelling_api_url,
            token_endpoint=oidc_token_endpoint,
            client_id=oidc_client_id,
            client_secret=oidc_client_secret
        )
        await create_labelling_project(create_project)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_project_async())

@dataclass
class CreateProject:
    api_url: str
    access_token=""
    token_endpoint: str
    client_id: str
    client_secret: str
    dataset_version: str
    dataset_directory: str


async def create_labelling_project(create_ecotag_project: CreateProject):
    dataset_version = create_ecotag_project.dataset_version
    api_url = create_ecotag_project.api_url
    token_endpoint = create_ecotag_project.token_endpoint
    client_id = create_ecotag_project.client_id
    client_secret = create_ecotag_project.client_secret
    access_token = create_ecotag_project.access_token
    dataset_directory = create_ecotag_project.dataset_directory

    if access_token == "":
        access_token = get_access_token(token_endpoint, client_id, client_secret)

    api_information = ApiInformation(api_url=api_url, access_token=access_token)

    dataset = Dataset(dataset_name='cats_dogs_others_v ' + dataset_version,
                      dataset_type='Image',
                      team_name='cats_dogs_others',
                      directory=dataset_directory,
                      classification='Public')
    await create_dataset(dataset, api_information)

    project = Project(project_name='cats_dogs_others_v ' + dataset_version,
                      dataset_name=dataset.dataset_name,
                      team_name='cats_dogs_others',
                      annotationType='ImageClassifier',
                      labels=[Label(name='cat', color='#FF0000', id="0"), Label(name='dog', color='#00FF00', id="1"),
                              Label(name='other', color='#0000FF', id="2")])

    await create_project(project, api_information)


if __name__ == "__main__":
    async def main():
        parser = argparse.ArgumentParser("labelling")
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
        dataset_version = args.dataset_version
        dataset_name = args.dataset_name
        api_url = args.api_url
        token_endpoint = args.token_endpoint
        client_id = args.client_id
        client_secret = args.client_secret

        create_project = CreateProject(api_url=api_url,
                                       token_endpoint=token_endpoint,
                                       client_id=client_id,
                                       dataset_version=dataset_version,
                                       client_secret=client_secret,
                                       dataset_directory=dataset_name)
        await create_labelling_project(create_project)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())