# Smart Document Management - Search

from . import messaging, entities
# import os

__all__ = ["parse_search_request", "get_search_results", "parse_search_results"]


### -= Messaging =-


def parse_search_request(parameters: dict):
    return messaging.parse_search_request(parameters)


### -= Search =-


def get_search_results(search_query: str, search_resource: str, search_index: str, search_page: int):
    # Get data from the form
    index_type = entities.get_index_type(search_resource, search_index)
    page_size=entities.get_search_page_size()

    # Add parameters to the URL
    params = messaging.get_params(
        index_type=index_type, 
        search_query=search_query,
        search_page=search_page,
        page_size=page_size
    )
    
    request_uri = entities.get_request_uri(search_resource, search_index, params)

    # Make the HTTP request
    return entities.run_search_request(request_uri, search_resource)


def parse_search_results(payload: dict, search_page: int):
    page_size=entities.get_search_page_size()
    return messaging.parse_search_results(payload, search_page, page_size)