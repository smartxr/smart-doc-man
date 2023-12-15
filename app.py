from flask import Flask, render_template, request, jsonify
from openai import AzureOpenAI
import requests
import os
import json
import sdm_chat

app = Flask(__name__)

# Chat seeding system message
chat_seed = "Answer questions in a sarcastic way"


@app.route("/")
def index():
    SEARCH_RESOURCES_LIST = json.loads(os.environ.get("SEARCH_RESOURCES_LIST"))
    SEARCH_RESOURCES_LIST["none"] = "-=None=-"
    return render_template(
        "chat.html", chat_seed=chat_seed, search_resources=SEARCH_RESOURCES_LIST
    )


@app.route("/chat")
def test():
    return render_template("chat.html")


# Configuration function to get options for index name selector
def get_index_options(resource):
    if resource == "none":
        return {"none": "-=None=-"}
    else:
        return json.loads(os.environ.get(f"SEARCH_INDEX_CONFIG_{resource.replace('-', '_').upper()}"))


@app.route("/get_options/<resource>")
def get_options(resource):
    index_list = get_index_options(resource)
    # print(index_list)
    return app.response_class(
        response=json.dumps(index_list), status=200, mimetype="application/json"
    )
    # return jsonify(options)


@app.route("/send_message", methods=["POST"])
def send_message():
    # user_message = request.form['user_message']
    # print(request.form['ref_id'])

    # Get request body
    data = request.get_json()
    # print(data) # TODO: Remove this Debug comment

    # Parse chat request coming from the web-page
    (
        user_message,
        search_resource,
        search_index_name,
        chat_seed,
        chat_history,
    ) = sdm_chat.parse_chat_request(data)

    if user_message == "":
        return jsonify({"status": "error", "message": "Empty message"})

    # Get API response
    # api_response_message = api_response.json().get('message', 'Error in API response')

    # Get OpenAI chat completion response
    completion = sdm_chat.get_chat_complition(
        search_resource, search_index_name, chat_seed, chat_history
    )

    # print(completion.model_dump_json(indent=2)) # TODO: Remove this Debug comment
    # TODO: Find other JSON dump's and convert them into model
    # TODO: What is "end_turn": true in the message

    # TODO : When forming chat history messages put citation in the body of the message for the assistant to see those citations.

    # Parse the structure received from Completions API and convert it into a structure
    messages = sdm_chat.parse_completions_message(completion)

    # Transform representation message into chat_history format
    chat_history.extend(messages)  # TODO: This is where to capture all Tool messages

    return jsonify(
        {"status": "success", "messages": messages, "chathistory": chat_history}
    )


@app.route("/clear_chat", methods=["POST"])
def clear_chat():
    # Clear chat history
    # chat_history.clear()
    return jsonify({"status": "success", "message": "Chat history cleared"})


if __name__ == "__main__":
    app.run(debug=True)
