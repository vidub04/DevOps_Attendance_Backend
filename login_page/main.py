from flask import Flask, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

app = Flask(__name__)


CORS(app, resources={
    r"/*": {
        "origins": "https://frontenddevop-eight.vercel.app"
    }
})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'https://frontenddevop-eight.vercel.app')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response




# 🔗 Supabase setup
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.route('/')
def home():
    return "Backend is running!"

# 📝 SIGNUP ROUTE
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json

    db_data = {
        "Enrolment_Number": data["enrolment"],
        "Name_of_Student": data["name"],
        "Branch": data["branch"],
        "College_Email": data["email"],
        "Semester": data["semester"],
        "Password": data["password"]
    }

    response = supabase.table("Login_Attendance").insert(db_data).execute()

    return jsonify({"message": "Signup successful!"})


@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({"message": "OK"}), 200

    data = request.json

    response = supabase.table("Login_Attendance") \
        .select("*") \
        .eq("Enrolment_Number", data["enrolment"]) \
        .execute()

    if not response.data:
        return jsonify({"message": "User not found ❌"})

    user = response.data[0]

    if user["Password"] == data["password"]:
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"message": "Wrong password ❌"})
    



if __name__ == '__main__':
    app.run(debug=True)