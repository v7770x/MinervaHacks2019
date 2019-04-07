from flask import Flask, render_template, jsonify, request
from flask_cors import CORS


import pyrebase

app = Flask(__name__)
CORS(app)


config = {
  "apiKey": "AIzaSyBep4hN7RY5OSQw7SmxYw1S62CtYUaZtek",
  "authDomain": "minerva-hacks-19.firebaseapp.com",
  "databaseURL": "https://minerva-hacks-19.firebaseio.com/",
  "storageBucket": "minerva-hacks-19.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
print(db.child("Hosts").get().val())

@app.route("/get_matches", methods=["POST", "GET"])
def get_matches():
	search_data = request.get_json(force=True)
	print(search_data)
	possible_hosts = db.child("Hosts").get().val()
	matches = []
	for host in possible_hosts:
		# print(host, possible_hosts[host])
		host_features = possible_hosts[host]
		if(host_features.get("location")==search_data.get("location") and host_features.get("num_ppl")>=search_data.get("num_ppl")
		 and (search_data.get("duration")=="any" or host_features.get("duration")>=search_data.get("duration")) 
		 and host_features.get("type")==search_data.get("type")):
			date = host_features.get("start_date")
			start_date = search_data.get("start_date")
			if(start_date=="any" or date["year"]==start_date["year"] and date["month"]==start_date["month"] and abs(date["day"] -start_date["day"])< 3 ):
				matches.append(host_features)
	print(matches)
	return jsonify(matches)

@app.route("/enter_new_host", methods=["POST", "GET"])
def enter_new_host():
	host_data = request.get_json(force=True)
	# possible_hosts = db.child("Hosts").get().val()
	print(host_data)
	db.child("Hosts").push(host_data)
	
	return "Done"

# def hi


# get_matches("San Francisco",3,{"month": 9, "year":2019, "day":17},6)


@app.route("/")
def main_page():
	return render_template("index.html")


