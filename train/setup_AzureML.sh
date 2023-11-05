AZURE_SUBSCRIPTION_ID=$1 #az account list
AZURE_RESOURCE_GROUP_NAME=$2
AZURE_ML_WORKSPACE_NAME=$3
AZURE_LOCATION=$4 #az account list-locations -o table


# Initialize Azure ML Workspace
az account set --subscription "$AZURE_SUBSCRIPTION_ID"
az group create --name "$AZURE_RESOURCE_GROUP_NAME" --location "$AZURE_LOCATION"
az extension add -n ml
# shellcheck disable=SC2086
az ml workspace create -n "$AZURE_ML_WORKSPACE_NAME" -g $AZURE_RESOURCE_GROUP_NAME

# Initialize Azure ML Pdf Dataset
cwd=$(pwd)
cd ./extraction
chmod +x ./init_dataset.sh
./init_dataset.sh "$AZURE_RESOURCE_GROUP_NAME" "$AZURE_ML_WORKSPACE_NAME"
cd $cwd

#poetry run python azureml_run_pipeline.py --subscription_id $AZURE_SUBSCRIPTION_ID --resource_group_name $AZURE_RESOURCE_GROUP_NAME --workspace_name $AZURE_ML_WORKSPACE_NAME --location $AZURE_LOCATION