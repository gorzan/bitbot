from flask import Flask, jsonify
import requests
import simplejson
import json

app = Flask(__name__)

@app.route('/')
def home():
    uri = 'https://api.bitcoinaverage.com/ticker/USD/'
    try:
       uResponse = requests.get(uri)
    except requests.ConnectionError:
       return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)

    last = data['last']

    result = 'Siste transaksjonskurs Bitcoin: $' + str(last)

    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)