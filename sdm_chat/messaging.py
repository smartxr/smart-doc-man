__all__ = ["parse_chat_request"]


def parse_chat_request(json_string):
    return (
        json_string.get("user_message", ""),
        json_string.get("search_resource", "none"),
        json_string.get("search_index", "none"),
        json_string.get("chat_seed", ""),
        json_string.get("chat_history", []),
    )
