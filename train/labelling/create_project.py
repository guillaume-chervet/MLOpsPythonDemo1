from dataclasses import dataclass

from ecotag import get_access_token, ApiInformation, create_dataset, Dataset, Project, create_project, Label
from dataset import download


@dataclass
class CreateProject:
    api_url: str
    access_token=""
    token_endpoint: str
    client_id: str
    client_secret: str
    dataset_version: str
    subscription_id: str
    resource_group_name: str
    workspace_name: str
    dataset_name: str


async def create_ecotag_project(create_ecotag_project: CreateProject):
    subscription_id = create_ecotag_project.subscription_id
    resource_group_name = create_ecotag_project.resource_group_name
    workspace_name = create_ecotag_project.workspace_name
    dataset_name = create_ecotag_project.dataset_name
    dataset_version = create_ecotag_project.dataset_version
    api_url = create_ecotag_project.api_url
    token_endpoint = create_ecotag_project.token_endpoint
    client_id = create_ecotag_project.client_id
    client_secret = create_ecotag_project.client_secret
    access_token = create_ecotag_project.access_token

    if access_token == "":
        access_token = get_access_token(token_endpoint, client_id, client_secret)

    dataset_path = download(subscription_id, resource_group_name, workspace_name, dataset_name, dataset_version)

    api_information = ApiInformation(api_url=api_url, access_token=access_token)

    dataset = Dataset(dataset_name='cats_dogs_others_v ' + dataset_version,
                      dataset_type='Image',
                      team_name='cats_dogs_others',
                      directory=dataset_path,
                      classification='Public')
    await create_dataset(dataset, api_information)

    project = Project(project_name='cats_dogs_others_v ' + dataset_version,
                      dataset_name=dataset.dataset_name,
                      team_name='cats_dogs_others',
                      annotationType='ImageClassifier',
                      labels=[Label(name='cat', color='#FF0000', id="0"), Label(name='dog', color='#00FF00', id="1"),
                              Label(name='other', color='#0000FF', id="2")])

    await create_project(project, api_information)
