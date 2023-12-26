# Smart Document Management - Search

from . import messaging, entities
import os

__all__ = ["parse_search_request", "get_search_results", "parse_search_results"]


### -= Messaging =-


def parse_search_request(json_message: str):
    return messaging.parse_search_request(json_message)



### -= Search =-


def get_search_results(search_query: str, search_resource: str, search_index: str):
    # Get data from the form
    index_type = entities.get_index_type(search_resource, search_index)

    # Add parameters to the URL
    params = messaging.get_params(
        index_type, 
        search_query=search_query
    )
    
    request_uri = entities.get_request_uri(search_resource, search_index, params)

    # Make the HTTP request
    return entities.run_search_request(request_uri, search_resource)


def parse_search_results(payload: dict):
    return messaging.parse_search_results(payload)