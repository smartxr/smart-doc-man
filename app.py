from flask import Flask, render_template, request, jsonify
# from openai import AzureOpenAI
# import requests
import os
import json
import sdm_chat, sdm_search

app = Flask(__name__)

# Chat seeding system message
chat_seed = "You are a helpful assistant who helps with searching through the library and finding answers in relevant documents."


@app.route("/")
def index():
    SEARCH_RESOURCES_LIST = json.loads(os.environ.get("SEARCH_RESOURCES_LIST"))
    # SEARCH_RESOURCES_LIST["none"] = "-=None=-"
    return render_template(
        "blocks.html", chat_seed=chat_seed, search_resources=SEARCH_RESOURCES_LIST
        # "index.html", chat_seed=chat_seed, search_resources=SEARCH_RESOURCES_LIST
    )


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


@app.route("/run_search", methods=["GET"])
def run_search():
    # user_message = request.form['user_message']
    # print(request.form['ref_id'])

    # Get request body
    data = request.args.to_dict()
    # print(data)

    # Parse chat request coming from the web-page
    (
        search_query,
        search_resource,
        search_index_name,
        search_page,
    ) = sdm_search.parse_search_request(data)

    # Check is Search Query was provided
    if search_query == "":
        return jsonify({"status": "error", "message": "Empty search query"})
    
    # Check is Search Resource was provided
    if search_resource == "":
        return jsonify({"status": "error", "message": "Empty search resource"})
    
    # Check is Search Index was provided
    if search_index_name == "":
        return jsonify({"status": "error", "message": "Empty search index"})


    # Get data from Search API
    response = sdm_search.get_search_results(
        search_query, search_resource, search_index_name, search_page,
    )

    if response.status_code != 200:
        return jsonify({"status": "error", "message": response.text})
        # return jsonify({"status": "error", "message": "Error in Search API response"})
    
    payload = response.json()

    # Save payload into a sample file
    # with open("sample_search_payload.json", "w") as file:
    #     json.dump(payload, file)


    # Load sample_search_payload into payload variable
    # with open("sample_search_payload.json", "r") as file:
    #     payload = json.load(file)

    result = sdm_search.parse_search_results(payload, search_page)
    # print(result)

    return jsonify(
        {"status": "success", "result": result}
    )    


@app.route("/clear_chat", methods=["POST"])
def clear_chat():
    # Clear chat history
    # chat_history.clear()
    return jsonify({"status": "success", "message": "Chat history cleared"})


if __name__ == "__main__":
    app.run(debug=True)
