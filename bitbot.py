from flask import Flask, jsonify, Response, request
import requests
import simplejson
import json

app = Flask(__name__)

@app.route('/price', methods=['POST', 'GET'])
def price():
	#define uri for various tickers
	api_uri = {}
	api_uri['btc'] = 'https://api.bitcoinaverage.com/ticker/USD/'
	api_uri['eth'] = 'https://coinmarketcap-nexuist.rhcloud.com/api/eth'

	#check if ticker is defined
	if 'text' not in request.args:
		return "Ingen ticker definert. Bruk '/price [ticker]'."

	ticker = request.args.get('text').lower()

	#check if valid ticker
	if ticker not in api_uri.keys():
		return "Ukjent ticker '" + ticker.upper() +"'"
	
	#get appropriate json object for ticker and put it in data
	try:
	   uResponse = requests.get(api_uri[ticker])
	except requests.ConnectionError:
		return "Tilkoblingsfeil - klarer ikke hente kurs for " + ticker.upper()
	Jresponse = uResponse.text
	data = json.loads(Jresponse)

	#create response dict
	output = {}
	output['response_type'] = 'in_channel'

	#fetch relevant object from json and build responsetext
	if ticker == 'btc':
		output['text'] = 'Siste transaksjonskurs for Bitcoin: $' + str(round(data['last'],2))
	elif ticker == 'eth':
		output['text'] = 'Siste transaksjonskurs for Etherium: $' + str(round(data['price']['usd'],2))
	else:
		return "Ukjent ticker '" + ticker.upper() +"'"

	json_response = json.dumps(output)

	resp = Response(response=json_response, status=200, mimetype="application/json")
	
	return resp

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)