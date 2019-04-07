from flask import Flask, render_template, jsonify
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

@app.route("/get_matches")
def get_matches(location, num_ppl, start_date, duration):
	possible_hosts = db.child("Hosts").get().val()
	matches = []
	for host in possible_hosts:
		# print(host, possible_hosts[host])
		host_features = possible_hosts[host]
		if(host_features.get("location")==location and host_features.get("num_ppl")>=num_ppl and host_features.get("duration")>=duration):
			date = host_features.get("start_date")
			if(date["year"]==start_date["year"] and date["month"]==start_date["month"] and abs(date["day"] -start_date["day"])< 3 ):
				matches.append(host_features)
	print(matches)
	# return jsonify(matches)

# def hi

get_matches("San Francisco",3,{"month": 9, "year":2019, "day":17},6)


@app.route("/")
def main_page():
	return render_template("index.html")


