from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st
import datetime
import os
import random

uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")

@st.cache_resource
def init_connection():
    return MongoClient(uri, server_api=ServerApi('1'))

def get_db():
    client = init_connection()
    return client.heartguard

def get_users_collection():
    return get_db().users

def get_predictions_collection():
    return get_db().predictions

def save_prediction(user_email, input_data, prediction_proba, prediction_class):
    get_predictions_collection().insert_one({
        "user_email": user_email,
        "timestamp": datetime.datetime.now(),
        "input_data": {k: float(v) if hasattr(v, 'item') else v for k, v in input_data.items()},
        "prediction_proba": float(prediction_proba),
        "prediction_class": int(prediction_class)
    })


def get_user_predictions(user_email):
    return list(get_predictions_collection().find({"user_email": user_email}).sort("timestamp", -1))

# ---- Health Profile ----
def save_health_profile(user_email, profile_data):
    col = get_db().health_profiles
    col.replace_one({"user_email": user_email}, {"user_email": user_email, **profile_data}, upsert=True)

def get_health_profile(user_email):
    return get_db().health_profiles.find_one({"user_email": user_email})

# ---- Doctors ----
MOCK_DOCTORS = [
    {"name": "Dr. Rajesh Khanna", "specialty": "Cardiologist", "hospital": "Apollo Hospital", "city": "Mumbai", "rating": 4.9, "experience": 22, "available": True, "phone": "+91 98200 11234", "fee": "₹800"},
    {"name": "Dr. Priya Sharma", "specialty": "Cardiac Surgeon", "hospital": "Fortis Heart Institute", "city": "Mumbai", "rating": 4.8, "experience": 18, "available": True, "phone": "+91 98200 22345", "fee": "₹1200"},
    {"name": "Dr. Anand Mehta", "specialty": "General Physician", "hospital": "Kokilaben Hospital", "city": "Mumbai", "rating": 4.6, "experience": 14, "available": False, "phone": "+91 98200 33456", "fee": "₹500"},
    {"name": "Dr. Sunita Patel", "specialty": "Cardiologist", "hospital": "Max Super Speciality", "city": "Delhi", "rating": 4.9, "experience": 26, "available": True, "phone": "+91 98110 44567", "fee": "₹1000"},
    {"name": "Dr. Vikram Nair", "specialty": "Cardiologist", "hospital": "AIIMS Delhi", "city": "Delhi", "rating": 4.7, "experience": 20, "available": True, "phone": "+91 98110 55678", "fee": "₹600"},
    {"name": "Dr. Meenakshi Rao", "specialty": "Cardiac Surgeon", "hospital": "Medanta Medicity", "city": "Delhi", "rating": 4.8, "experience": 15, "available": False, "phone": "+91 98110 66789", "fee": "₹1500"},
    {"name": "Dr. Suresh Iyer", "specialty": "Cardiologist", "hospital": "Narayana Health", "city": "Bangalore", "rating": 4.9, "experience": 24, "available": True, "phone": "+91 80123 77890", "fee": "₹900"},
    {"name": "Dr. Deepa Krishnaswamy", "specialty": "General Physician", "hospital": "Manipal Hospital", "city": "Bangalore", "rating": 4.5, "experience": 12, "available": True, "phone": "+91 80123 88901", "fee": "₹450"},
    {"name": "Dr. Arvind Gupta", "specialty": "Cardiac Surgeon", "hospital": "Columbia Asia", "city": "Bangalore", "rating": 4.7, "experience": 17, "available": True, "phone": "+91 80123 99012", "fee": "₹1100"},
    {"name": "Dr. Kavitha Reddy", "specialty": "Cardiologist", "hospital": "KIMS Hospital", "city": "Hyderabad", "rating": 4.8, "experience": 19, "available": True, "phone": "+91 40987 10123", "fee": "₹750"},
    {"name": "Dr. Ravi Shankar", "specialty": "General Physician", "hospital": "Care Hospital", "city": "Hyderabad", "rating": 4.6, "experience": 11, "available": False, "phone": "+91 40987 21234", "fee": "₹400"},
    {"name": "Dr. Padma Venkatesh", "specialty": "Cardiologist", "hospital": "Star Hospital", "city": "Hyderabad", "rating": 4.9, "experience": 28, "available": True, "phone": "+91 40987 32345", "fee": "₹950"},
    {"name": "Dr. Arun Kumar", "specialty": "Cardiologist", "hospital": "MIOT International", "city": "Chennai", "rating": 4.7, "experience": 21, "available": True, "phone": "+91 44876 43456", "fee": "₹850"},
    {"name": "Dr. Lakshmi Narayanan", "specialty": "Cardiac Surgeon", "hospital": "Fortis Malar", "city": "Chennai", "rating": 4.8, "experience": 16, "available": True, "phone": "+91 44876 54567", "fee": "₹1300"},
    {"name": "Dr. Santosh Mishra", "specialty": "Cardiologist", "hospital": "Ruby Hall Clinic", "city": "Pune", "rating": 4.6, "experience": 13, "available": True, "phone": "+91 20765 65678", "fee": "₹700"},
    {"name": "Dr. Neha Joshi", "specialty": "General Physician", "hospital": "Sahyadri Hospital", "city": "Pune", "rating": 4.5, "experience": 9, "available": True, "phone": "+91 20765 76789", "fee": "₹350"},
    {"name": "Dr. Harish Chandra", "specialty": "Cardiologist", "hospital": "PGI Chandigarh", "city": "Chandigarh", "rating": 4.9, "experience": 30, "available": False, "phone": "+91 17254 87890", "fee": "₹600"},
    {"name": "Dr. Pooja Singh", "specialty": "Cardiologist", "hospital": "Medanta Lucknow", "city": "Lucknow", "rating": 4.7, "experience": 15, "available": True, "phone": "+91 52298 98901", "fee": "₹650"},
]

def seed_doctors_if_empty():
    col = get_db().doctors
    if col.count_documents({}) == 0:
        col.insert_many(MOCK_DOCTORS)

def get_doctors(city=None, specialty=None, available_only=False):
    seed_doctors_if_empty()
    query = {}
    if city and city != "All Cities":
        query["city"] = city
    if specialty and specialty != "All Specialties":
        query["specialty"] = specialty
    if available_only:
        query["available"] = True
    return list(get_db().doctors.find(query, {"_id": 0}))

def get_all_cities():
    seed_doctors_if_empty()
    return sorted(get_db().doctors.distinct("city"))

# ---- Appointments ----
DOCTOR_NOTE_TEMPLATES = [
    "Thank you for your visit. Based on your cardiac risk assessment of {risk:.1f}%, I recommend scheduling a follow-up ECG and lipid panel test within the next 2 weeks. Please maintain your prescribed medications and avoid strenuous physical activity for now.",
    "I've reviewed your HeartGuard assessment ({risk:.1f}% risk). I recommend a resting echocardiogram and stress test. Please reduce sodium intake to under 1500mg/day and monitor your blood pressure at home twice daily.",
    "Your cardiac risk profile ({risk:.1f}%) has been reviewed. I'm prescribing a modified DASH diet plan and light walking (20 min/day). Let's also run a complete lipid panel and HbA1c test. Please book the lab tests at the hospital.",
    "Following your risk assessment of {risk:.1f}%, I recommend immediate 24-hour Holter monitoring. Continue your current medications, avoid caffeine, and come in for a proper consultation within 3 days.",
]

def book_appointment(user_email, doctor_name, hospital, specialty, risk_proba):
    db = get_db()
    appt = {
        "user_email": user_email,
        "doctor_name": doctor_name,
        "hospital": hospital,
        "specialty": specialty,
        "timestamp": datetime.datetime.now(),
        "status": "Confirmed",
    }
    db.appointments.insert_one(appt)
    # Auto-generate a doctor note
    note_text = random.choice(DOCTOR_NOTE_TEMPLATES).format(risk=risk_proba)
    db.doctor_notes.insert_one({
        "user_email": user_email,
        "doctor_name": doctor_name,
        "hospital": hospital,
        "timestamp": datetime.datetime.now() + datetime.timedelta(minutes=5),
        "note": note_text,
        "follow_up": "Schedule a lab appointment within 2 weeks",
        "read": False,
    })

def get_user_appointments(user_email):
    return list(get_db().appointments.find({"user_email": user_email}).sort("timestamp", -1))

def get_doctor_notes(user_email):
    return list(get_db().doctor_notes.find({"user_email": user_email}).sort("timestamp", -1))

def mark_note_read(user_email):
    get_db().doctor_notes.update_many({"user_email": user_email}, {"$set": {"read": True}})

def count_unread_notes(user_email):
    return get_db().doctor_notes.count_documents({"user_email": user_email, "read": False})
