import os
from openai import AzureOpenAI

__all__ = ["get_azureopenai_client", "get_doclib_config", "run_chat_complition"]


def get_azureopenai_client():
    return AzureOpenAI(
        # https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#rest-api-versioning
        api_version=os.environ.get("OPENAI_API_VERSION"),
        # https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource
        base_url=f"{os.environ.get('OPENAI_API_ENDPOINT')}/openai/deployments/{os.environ.get('OPENAI_DEPLOYMENT_ID')}/extensions",
        api_key=os.environ.get("OPENAI_API_KEY"),
    )


def get_doclib_config(search_resource: str, search_index_name: str, chat_seed: str):
    if search_resource == "none":
        return None
    else:
        return {
            "dataSources": [
                {
                    "type": "AzureCognitiveSearch",
                    "parameters": {
                        "endpoint": f"https://{search_resource.lower()}.search.windows.net",
                        "key": os.environ.get(
                            f'SEARCH_API_KEY_{search_resource.replace("-", "_").upper()}'
                        ),
                        "indexName": search_index_name,
                        "queryType": "semantic",
                        "semanticConfiguration": "default",
                        "topNDocuments": 10,  # Retrieved documents. Default - 5, maximum - 20
                        "roleInformation": chat_seed,
                        # "roleInformation": 'You are an AI assistant that helps people find information.',
                        "strictness": 1,  # default - 3, highest - 5, lowest - 1
                    },
                }
            ]
        }


def run_chat_complition(
    client: AzureOpenAI, chat_history: list, extra_body_value: dict
):
    return client.chat.completions.create(
        model=os.environ.get(
            "OPENAI_DEPLOYMENT_ID"
        ),  # e.g. gpt-35-instant TODO: Remove it as redundant
        messages=chat_history,
        extra_body=extra_body_value,
    )
