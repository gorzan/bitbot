from flask import Flask, jsonify, Response, request
import requests
import simplejson
import json

app = Flask(__name__)

@app.route('/price', methods=['POST', 'GET'])
def price():
	#check if ticker is defined
	if 'text' not in request.args:
		return "Ingen ticker definert. Bruk '/price [ticker]'."

	ticker = request.args.get('text').lower()
	coin_uri = 'https://coinmarketcap-nexuist.rhcloud.com/api/' + ticker

	
	#get appropriate json object for ticker and put it in data
	try:
	   uResponse = requests.get(coin_uri)
	except requests.ConnectionError:
		return "Tilkoblingsfeil - klarer ikke hente kurs for " + ticker.upper()
	Jresponse = uResponse.text
	data = json.loads(Jresponse)

	#check ticker existence
	if 'name' not in data:
		return "Ukjent ticker: '" + ticker.upper() + "'"

	#create response dict
	output = {}
	output['response_type'] = 'in_channel'
	output['text'] = 'Siste transaksjonskurs for ' + data['name'] + ': $' + str(data['price']['usd'])

	json_response = json.dumps(output)

	resp = Response(response=json_response, status=200, mimetype="application/json")
	
	return resp

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)