from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace these with the actual API URL and the necessary credentials
API_BASE_URL = "http://example.com/api"
API_KEY = 'your_api_key'

@app.route('/')
def index():
    return render_template('chat.html')
    # return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
       