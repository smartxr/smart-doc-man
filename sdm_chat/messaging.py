from datetime import datetime
import json

__all__ = [
    "parse_chat_request",
    "parse_citation",
    "parse_citations",
    "parse_intents",
    "parse_completions_message",
]


def parse_chat_request(json_string: str):
    return (
        json_string.get("user_message", ""),
        json_string.get("search_resource", "none"),
        json_string.get("search_index", "none"),
        json_string.get("chat_seed", ""),
        json_string.get("chat_history", []),
    )


def parse_citation(citation, ref_no):
    return {
        "ref_no": ref_no,
        "id": citation["id"],
        "title": citation["title"],
        "filepath": citation["filepath"],
        "url": citation["url"],
        "chunk_id": citation["chunk_id"],
        # 'content': citation['content'],
    }


def parse_citations(citations):
    result = []
    ref_no = 1
    for citation in citations:
        result.append(parse_citation(citation, ref_no))
        ref_no += 1
    return result


def parse_intents(intents_json: str):
    intents = []
    for intent in json.loads(intents_json):
        intents.append(intent)
    return intents


# Input should be 'system', 'user', 'assistant', 'tool' or 'function'"
def parse_completions_message(completion):
    messages = []
    for choice in completion.choices:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for context_message in choice.message.context["messages"]:
            cm_role = context_message["role"]
            cm_content = json.loads(context_message["content"])
            # Extract citations
            citations = parse_citations(cm_content["citations"])
            # ref_no = 1
            # for citation in cm_content['citations']:
            #     citations.append(parse_citation(citation), ref_no)
            #     ref_no += 1

            # Extract intents
            intents = parse_intents(cm_content["intent"])
            # for intent in json.loads(cm_content['intent']):
            #     intents.append(intent)

        # Package all accumulated components in a message
        messages.append(
            {
                "index": choice.index,  # TODO: Consider removing from chat history
                "timestamp": timestamp,
                "content": choice.message.content,
                "role": choice.message.role,
                "end_turn": choice.message.end_turn,  # TODO: Consider removing from chat history
                "context": {
                    "role": cm_role,
                    "citations": citations,
                    "intents": intents,
                },
            }
        )

    return messages
