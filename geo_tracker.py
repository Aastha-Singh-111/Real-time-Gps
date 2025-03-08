# # gps_fetcher.py - Fetches GPS coordinates and sends to Firestore
# import geocoder
# import time
# import json
# import firebase_admin
# from firebase_admin import credentials, firestore

# # Initialize Firebase
# cred = credentials.Certificate("firebase_credentials.json")  # Add your Firebase credentials
# firebase_admin.initialize_app(cred)
# db = firestore.client()
# # print(f"Cred stored: {cred}")
# # print(f"db stored: {db}")

# def get_location():
#     g = geocoder.ip('me')  # Fetch location from IP
#     if g.latlng:
#         # print(f"Data stored: {location}")
#         return {'latitude': g.latlng[0], 'longitude': g.latlng[1], 'timestamp': time.time()}
#     return None

# def send_to_firestore(location):
#     if location:
#         doc_ref = db.collection("gps_data").add(location)
#         # print(f"doc_Ref: {doc_ref}")
#         # print(f"Data stored: {location}")

# def main():
#     while True:
#         location = get_location()
#         if location:
#             print(json.dumps(location, indent=2))
#             send_to_firestore(location)
#         time.sleep(5) 

# if __name__ == "__main__":
#     main()





# geo_tracker.py - Fetches GPS coordinates and checks for movement alerts
import geocoder
import time
import json
import firebase_admin
from firebase_admin import credentials, firestore
from geopy.distance import geodesic

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_credentials.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

initial_location = None  # Store initial location

def get_location():
    g = geocoder.ip('me')  # Fetch location from IP
    if g.latlng:
        return {'latitude': g.latlng[0], 'longitude': g.latlng[1], 'timestamp': time.time()}
    return None

def send_to_firestore(location):
    if location:
        db.collection("gps_data").add(location)

def store_alert(current_location, distance):
    alert_data = {
        "message": "User moved more than 500 meters!",
        "distance_m": distance,
        "latitude": current_location['latitude'],
        "longitude": current_location['longitude'],
        "timestamp": time.time()
    }
    db.collection("alerts").add(alert_data)
    print("🚨 ALERT STORED IN FIRESTORE!", json.dumps(alert_data, indent=2))

def check_movement(current_location):
    global initial_location
    if initial_location is None:
        initial_location = current_location  # Store first location
        print("[INFO] Initial location set.")
        return
    
    distance = geodesic((initial_location['latitude'], initial_location['longitude']), 
                        (current_location['latitude'], current_location['longitude'])).meters
    print(f"[INFO] Moved: {distance:.2f} meters")
    
    if distance > 500:
        print("🚨 ALERT! User moved more than 500 meters!")
        store_alert(current_location, distance)

def main():
    while True:
        location = get_location()
        if location:
            print(json.dumps(location, indent=2))
            send_to_firestore(location)
            check_movement(location)  # Check if moved >500m
        time.sleep(5)  # Fetch every 60 seconds

if __name__ == "__main__":
    main()


