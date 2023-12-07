from flask import Flask, render_template, request, jsonify
from openai import AzureOpenAI
from datetime import datetime
import requests
import os
import json

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
    # user_message = 'user_message'
    
    # chat_history = []

    # Add user message to chat history
    # chat_history.append({'timestamp': timestamp, 'name': 'User', 'content': user_message})

    # Send full chat history to API
    # api_response = requests.post(api_endpoint, json={'chat_history': chat_history})

    data = request.get_json()
    print(data)
    user_message = data.get('user_message', '')
    chat_history = data.get('chat_history', [])
    search_resource = data.get('search_resource', 'none')
    search_index_name = data.get('search_index', 'none')

    if user_message == '':
        return jsonify({'status': 'error', 'message': 'Empty message'})

    # Get API response
    # api_response_message = api_response.json().get('message', 'Error in API response')


    client = AzureOpenAI(
        # https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#rest-api-versioning
        api_version=os.environ.get('OPENAI_API_VERSION'),
        # https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource
        base_url=f"{os.environ.get('OPENAI_API_ENDPOINT')}/openai/deployments/{os.environ.get('OPENAI_DEPLOYMENT_ID')}/extensions",
        api_key=os.environ.get('OPENAI_API_KEY'),
    )

    if search_resource == 'none':
        extra_body_value = None
    else:    
        extra_body_value = {
            "dataSources": [
                {
                    "type": "AzureCognitiveSearch",
                    "parameters": {
                        "endpoint": f"https://{search_resource}.search.windows.net",
                        "key": os.environ.get(f'SEARCH_API_KEY_{search_resource.upper()}'),
                        "indexName": search_index_name,
                        "queryType": "semantic",
                        "semanticConfiguration": "default",
                        "topNDocuments": 10, #Retrieved documents. Default - 5, maximum - 20
                        "roleInformation": 'You are an AI assistant that helps people find information.',
                        "strictness": 1, # default - 3, highest - 5, lowest - 1
                    }
                }
            ]
        }

    completion = client.chat.completions.create(
        model=os.environ.get('OPENAI_DEPLOYMENT_ID'),  # e.g. gpt-35-instant TODO: Remove it as redundant
        messages=chat_history,
        extra_body=extra_body_value,
    )

    print(completion.model_dump_json(indent=2))

    # Add API response to chat history
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    api_response_message = {'timestamp': timestamp, 'role': completion.choices[0].message.role, 'content': completion.choices[0].message.content}

    chat_history.append(api_response_message)


    # chat_history.append(api_response_message)

    return jsonify({'status': 'success', 'message': api_response_message, 'chathistory': chat_history})
    # return jsonify({'status': 'success', 'message': api_response_message, 'chathistory': chat_history})

@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    # Clear chat history
    # chat_history.clear()
    return jsonify({'status': 'success', 'message': 'Chat history cleared'})

if __name__ == '__main__':
    app.run(debug=True)
