from flask import Flask, render_template, request, jsonify
from openai import AzureOpenAI
from datetime import datetime
import requests
import os
import json
import sdm_chat

app = Flask(__name__)

# Chat history
# chat_seed = [{'role': 'System', 'content': 'Answer to questions in sarcastic way'}]
chat_seed = 'Answer questions in a sarcastic way'

# API endpoint (replace with your actual API endpoint)
api_endpoint = "https://your-api-endpoint.com"

@app.route('/')
def index():
    # chat_history = [] Initialize with System Message
    # return render_template('search.html')
    # return render_template('search.html', chat_seed=chat_seed)
    SEARCH_RESOURCES_LIST = json.loads(os.environ.get('SEARCH_RESOURCES_LIST'))
    SEARCH_RESOURCES_LIST['none'] = '-=None=-'
    return render_template('chat.html', chat_seed=chat_seed, search_resources=SEARCH_RESOURCES_LIST)

@app.route('/chat')
def test():
    return render_template('chat.html')

# Configuration function to get options for selector 2
def get_index_options(resource):
    if resource == 'none':
        return {'none': '-=None=-'}
    else:
        return json.loads(os.environ.get(f'SEARCH_INDEX_CONFIG_{resource.upper()}'))

@app.route('/get_options/<resource>')
def get_options(resource):
    index_list = get_index_options(resource)
    # print(index_list)
    return app.response_class(response=json.dumps(index_list), status=200, mimetype='application/json')
    # return jsonify(options)

@app.route('/send_message', methods=['POST'])
def send_message():
    # user_message = request.form['user_message']
    # print(request.form['ref_id'])
    
    # Get request body
    data = request.get_json()
    # print(data) # TODO: Remove this Debug comment

    # Parse chat request coming from the web-page
    user_message, search_resource, search_index_name, chat_seed, chat_history = sdm_chat.parse_chat_request(data)

    if user_message == '':
        return jsonify({'status': 'error', 'message': 'Empty message'})

    # Get API response
    # api_response_message = api_response.json().get('message', 'Error in API response')

    # Get OpenAI chat complition response
    completion = sdm_chat.get_chat_complition(search_resource, search_index_name, chat_seed, chat_history)

    # print(completion.model_dump_json(indent=2)) # TODO: Remove this Debug comment
    # TODO: Find other JSON dump's and convert them into model

    # Deserialize citation information from Tool message
    # TODO: What is "end_turn": true in the message
    messages = []
    for choice in completion.choices:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for context_message in choice.message.context['messages']:
            cm_role = context_message['role']
            cm_content = json.loads(context_message['content'])
            citations = []
            ref_no = 1
            for citation in cm_content['citations']:
                citations.append({
                    'ref_no': ref_no,
                    'id': citation['id'],
                    'title': citation['title'],
                    'filepath': citation['filepath'],
                    'url': citation['url'],
                    'chunk_id': citation['chunk_id'],
                    # 'content': citation['content'],
                })
                ref_no += 1
            
            intents = []
            for intent in json.loads(cm_content['intent']):
                intents.append(intent)

        # Package all accumulated components in a message
        messages.append({
            'index': choice.index, # TODO: Consider removing from chat history
            'timestamp': timestamp,
            'content': choice.message.content,
            'role': choice.message.role,
            'end_turn': choice.message.end_turn, # TODO: Consider removing from chat history
            'context': {
                'role': cm_role,
                'citations': citations,
                'intents': intents,
            }
        })


    # Add API response to chat history
    # api_response_messages = [{'timestamp': timestamp, 'role': completion.choices[0].message.role, 'content': completion.choices[0].message.content}]
    # TODO: Accomodate multiple choices and Tool messages

# TODO : When forming chat history messages put citation in the body of the message for the assistant to see those citations.

    # chat_history.append(api_response_message) # TODO: This is where to capture all Tool messages
    chat_history.extend(messages) # TODO: This is where to capture all Tool messages

    # print(sdm_chat.convert_message(messages))

    # chat_history.append(api_response_message)

    # Input should be 'system', 'user', 'assistant', 'tool' or 'function'"

    return jsonify({'status': 'success', 'messages': messages, 'chathistory': chat_history})
    # return jsonify({'status': 'success', 'message': api_response_message, 'chathistory': chat_history})

@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    # Clear chat history
    # chat_history.clear()
    return jsonify({'status': 'success', 'message': 'Chat history cleared'})

if __name__ == '__main__':
    app.run(debug=True)
