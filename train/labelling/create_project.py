from dataclasses import dataclass

from ecotag_sdk.ecotag import get_access_token, ApiInformation, create_dataset, Dataset, Project, create_project, Label


@dataclass
class CreateProject:
    api_url: str
    access_token=""
    token_endpoint: str
    client_id: str
    client_secret: str
    dataset_version: str
    dataset_directory: str


async def create_ecotag_project(create_ecotag_project: CreateProject):
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
