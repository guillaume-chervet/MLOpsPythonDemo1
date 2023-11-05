AZURE_SUBSCRIPTION_ID=$1 #az account list
AZURE_RESOURCE_GROUP_NAME=$2
AZURE_ML_WORKSPACE_NAME=$3
AZURE_LOCATION=$4 #az account list-locations -o table

poetry run python azureml_run_pipeline.py \
    --subscription_id "$AZURE_SUBSCRIPTION_ID" \
    --resource_group_name "$AZURE_RESOURCE_GROUP_NAME" \
    --workspace_name "$AZURE_ML_WORKSPACE_NAME" \
    --location "$AZURE_LOCATION"