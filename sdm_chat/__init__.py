from . import messaging, searching, entities
import os

__all__ = ["parse_chat_request", "parse_completions_message", "get_chat_complition"]

### -= Messaging =-


def parse_chat_request(json_message: str):
    return messaging.parse_chat_request(json_message)


def parse_completions_message(completion):
    return messaging.parse_completions_message(completion)


### -= Entities =-


def get_chat_complition(
    search_resource: str, search_index_name: str, chat_seed: str, chat_history: list
):
    client = entities.get_azureopenai_client()
    extra_body_value = entities.get_doclib_config(
        search_resource, search_index_name, chat_seed
    )
    return entities.run_chat_complition(client, chat_history, extra_body_value)


### -= Search =-

def get_search_data(search_resource: str, search_index: str, search_query: str):
    # Get data from the form
    url = "https://{}.search.windows.net/indexes/{}/docs".format(
        search_resource, search_index
    )
    print(url)
    
    # Add parameters to the URL
    params = searching.get_params(
        search_resource=search_resource, 
        search_index=search_index, 
        search_query=search_query
    )
    
    # Build URL
    url += "?" + "&".join([f"{key}={value}" for key, value in params.items()])

    # Add the headers
    resource_key = search_resource.replace('-', '_').upper()
    headers = {
        "api-key": os.environ.get(
            f'SEARCH_API_KEY_{resource_key}'
        )
    }

    # Make the HTTP request
    response = requests.get(url, headers=headers)

    return entities.get_azureopenai_client()