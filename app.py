# app.py - Flask Server to Fetch GPS Data from Firestore

from flask import Flask, jsonify, render_template
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
 
@app.route("/get_location", methods=["GET"])
def get_location():
    docs = db.collection("gps_data").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(1).stream()
    print(f"docs got: {docs}")
    location = None
    for doc in docs:
        location = doc.to_dict()
        print(f"location got: {location}")
    return jsonify(location) if location else jsonify({"error": "No data found"})

@app.route("/")
def index():
    return render_template("index.html")  # Frontend dashboard

if __name__ == "__main__":
    app.run(debug=True)
