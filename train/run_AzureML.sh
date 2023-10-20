AZURE_SUBSCRIPTION_ID="9d42c9d4-85ab-429d-afb4-4d77f309078c" #az account list
AZURE_RESOURCE_GROUP_NAME="azure-ml-yola"
AZURE_ML_WORKSPACE_NAME="cats-dogs-yola"
AZURE_LOCATION="northeurope" #az account list-locations -o table

poetry run python azureml_run_pipeline.py \
    --subscription_id $AZURE_SUBSCRIPTION_ID \
    --resource_group_name $AZURE_RESOURCE_GROUP_NAME \
    --workspace_name $AZURE_ML_WORKSPACE_NAME \
    --location $AZURE_LOCATION