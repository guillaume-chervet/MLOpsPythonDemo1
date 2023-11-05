#.\init_repository.sh "MLOpsPythonMyDemo" "RobertCarry22" "MLOpsPython"

# Définir les paramètres avec des valeurs par défaut
repositoryName="${1:-MLOpsPythonMyDemo}"
workspaceName="${2:-RobertCarry22}"
environmentName="${3:-MLOpsPython}"

# Authenticate using Azure CLI (az) and GitHub CLI (gh)
az login
gh auth login

# Fork MLOpsPython repository
gh repo fork https://github.com/guillaume-chervet/MLOpsPythonDemo1 --default-branch-only --fork-name "$repositoryName" --clone

# Retrieve the repository full name (org/repo)
repositoryFullName="$workspaceName/$repositoryName"

# Change directory to the local repository
cd "$repositoryName"

# Remove the upstream remote and set the upstream to the main branch
git remote remove upstream
git push --set-upstream origin main

# Set the default repository
gh repo set-default "https://github.com/${repositoryFullName}"

# Create environment
gh api --method PUT -H "Accept: application/vnd.github+json" "repos/${repositoryFullName}/environments/${environmentName}"

# Retrieve the current subscription and current tenant identifiers using Azure CLI
subscriptionId=$(az account show --query "id" -o tsv)
tenantId=$(az account show --query "tenantId" -o tsv)

# Create an App Registration and its associated service principal using Azure CLI
appId=$(az ad app create --display-name "GitHub Action OIDC for ${repositoryFullName}" --query "appId" -o tsv)
servicePrincipalId=$(az ad sp create --id "$appId" --query "id" -o tsv)

# Assign the contributor role to the service principal on the subscription using Azure CLI
az role assignment create --role contributor --subscription "$subscriptionId" --assignee-object-id "$servicePrincipalId" --assignee-principal-type ServicePrincipal --scope "/subscriptions/$subscriptionId"

# Prepare parameters for federated credentials
parametersJson='{
    "name": "'"$environmentName"'",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:'"$repositoryFullName"':environment:'"$environmentName"'",
    "description": "Development",
    "audiences": [
        "api://AzureADTokenExchange"
    ]
}'

# Create federated credentials using Azure CLI
az ad app federated-credential create --id "$appId" --parameters "$parametersJson"

# Create GitHub secrets needed for the GitHub Actions using GitHub CLI
gh secret set AZURE_TENANT_ID --body "$tenantId" --env "$environmentName"
gh secret set AZURE_SUBSCRIPTION_ID --body "$subscriptionId" --env "$environmentName"
gh secret set AZURE_CLIENT_ID --body "$appId" --env "$environmentName"

# Run the GitHub workflow
gh workflow run main.yml

# Get the run ID
runId=$(gh run list --workflow=main.yml --json databaseId -q ".[0].databaseId")

# Watch the run
gh run watch "$runId"

# Open the repository in the browser
gh repo view -w