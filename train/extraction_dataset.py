import asyncio
from dataclasses import dataclass
from pathlib import Path
import azure.ai.ml._artifacts._artifact_utilities as artifact_utils
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.entities import Data
from labelling.create_project import CreateProject, create_ecotag_project
from dataset import download

@dataclass
class RegisterExtractedDataset:
    labelling_api_url = "https://axaguildev-ecotag.azurewebsites.net/api/server"
    oidc_token_endpoint = "https://demo.duendesoftware.com/connect/token"
    oidc_client_id = "m2m"
    oidc_client_secret = "secret"
    subscription_id: str
    resource_group_name: str
    workspace_name: str


def register_extracted_dataset(ml_client,
                               custom_output_path: str,
                               tags: dict,
                               register_extracted_dataset: RegisterExtractedDataset):
    base_path = Path(__file__).resolve().parent

    artifact_utils.download_artifact_from_aml_uri(
        uri=custom_output_path + "extraction_hash",
        destination=str(base_path),
        datastore_operation=ml_client.datastores,
    )

    # lire le fichier hash.txt qui est dans base_path
    with open(str(base_path / "hash.txt"), "r") as file:
        computed_hash = file.read()
    print(f"computed_hash: {computed_hash}")

    extracted_images_dataset_name = "cats-dogs-others-extracted"
    try:
        list_datasets = ml_client.data.list(extracted_images_dataset_name)
        list_list_dataset = list(list_datasets)
        version_dataset_extraction = len(list_list_dataset) + 1
    except:
        list_list_dataset = []
        version_dataset_extraction = 1
        print("No dataset with name cats-dogs-others-extracted")

    hash_tag_already_exists = False
    len_dataset = len(list_list_dataset)
    if len_dataset > 0:
        dataset = list_list_dataset[len_dataset - 1]
        print(f"dataset.tags: {str(dataset.version)}")
        print(dataset.tags)
        if "hash" in dataset.tags:
            extracted_images_dataset_version = dataset.tags["hash"]
            print(f"extracted_images_dataset_version: {extracted_images_dataset_version}")
            print(f"computed_hash: {computed_hash}")
            if extracted_images_dataset_version == computed_hash:
                hash_tag_already_exists = True

    if not hash_tag_already_exists and "git_head_ref" in tags:  # and tags["git_head_ref"] == "main":
        extracted_images_dataset = Data(
            name=extracted_images_dataset_name,
            path=custom_output_path + "extraction_images",
            type=AssetTypes.URI_FOLDER,
            description="Extracted images for cats and dogs and others",
            version=str(version_dataset_extraction),
            tags={"hash": computed_hash, **tags},
        )
        extracted_images_dataset = ml_client.data.create_or_update(extracted_images_dataset)

        async def create_project_async():
            subscription_id = register_extracted_dataset.subscription_id
            resource_group_name = register_extracted_dataset.resource_group_name
            workspace_name = register_extracted_dataset.workspace_name
            dataset_name = extracted_images_dataset.name
            dataset_version = extracted_images_dataset.version

            dataset_path = download(subscription_id, resource_group_name, workspace_name, dataset_name, dataset_version)

            create_project = CreateProject(
                dataset_directory=dataset_path,
                dataset_version=str(version_dataset_extraction),
                api_url=register_extracted_dataset.labelling_api_url,
                token_endpoint=register_extracted_dataset.oidc_token_endpoint,
                client_id=register_extracted_dataset.oidc_client_id,
                client_secret=register_extracted_dataset.oidc_client_secret
            )
            await create_ecotag_project(create_project)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(create_project_async())
        print(
            f"Dataset with name {extracted_images_dataset.name} was registered to workspace, the dataset version is {extracted_images_dataset.version}"
        )
