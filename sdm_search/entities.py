import os
import requests

__all__ = ["get_request_uri", "run_search_request", "get_index_type"]

def get_index_type(search_resource: str, search_index: str):
    resource = search_resource.replace('-', '_').upper()
    index = search_index.replace("-", "_").upper()
    return os.environ.get(f"SEARCH_INDEX_TYPE_{resource}_{index}")

def get_request_uri(search_resource: str, search_index: str, params: dict):
    # url = "https://{}.search.windows.net/indexes/{}/docs".format(
    #     search_resource, search_index
    # )
    # print(url)

    # # Build URL
    # url += "?" + "&".join([f"{key}={value}" for key, value in params.items()])

    return "https://{}.search.windows.net/indexes/{}/docs?{}".format(
        search_resource, search_index, "&".join([f"{key}={value}" for key, value in params.items()])
    )


def run_search_request(request_uri: str, search_resource: str):
    # Add the headers
    resource_key = search_resource.replace('-', '_').upper()
    headers = {
        "api-key": os.environ.get(
            f'SEARCH_API_KEY_{resource_key}'
        )
    }

    # Make the HTTP request
    return requests.get(request_uri, headers=headers)