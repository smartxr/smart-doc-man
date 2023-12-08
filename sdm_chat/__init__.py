from . import messaging, entities
import os

__all__ = ["parse_chat_request"]


def parse_chat_request(json_message):
    return messaging.parse_chat_request(json_message)


### -= Entities =-

def get_chat_complition(search_resource: str, search_index_name: str, chat_seed: str, chat_history: list):
    client = entities.get_azureopenai_client()
    extra_body_value = entities.get_doclib_config(search_resource, search_index_name, chat_seed)
    return  entities.run_chat_complition(client, chat_history, extra_body_value)
