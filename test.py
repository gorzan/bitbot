from flask import Flask, jsonify, Response
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

    output = {}
    output['text'] = 'Siste transaksjonskurs Bitcoin: $' + str(last)
    output['response_type'] = 'in_channel'

    json_response = json.dumps(output)

    resp = Response(response=json_response, status=200, mimetype="application/json")
    
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)