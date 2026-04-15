from flask import Flask, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# 🔗 Supabase setup
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

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


# 🔐 LOGIN ROUTE
@app.route('/login', methods=['POST'])
def login():
    data = request.json

    response = supabase.table("Login_Attendance") \
        .select("*") \
        .eq("Enrolment_Number", data["enrolment"]) \
        .eq("Password", data["password"]) \
        .execute()

    if response.data:
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"message": "Invalid credentials"})


if __name__ == '__main__':
    app.run(debug=True)