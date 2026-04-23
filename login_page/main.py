from flask import Flask, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
from flask_cors import CORS
from datetime import date
import os

load_dotenv()

app = Flask(__name__)


CORS(app, origins=["https://devops-attendance-frontend-xi.vercel.app"])



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

    response = supabase.table("Login").insert(db_data).execute()

    return jsonify({"message": "Signup successful!"})


@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({"message": "OK"}), 200

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    response = supabase.table("Login") \
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
    


# ---------------- STUDENT DASHBOARD ----------------
@app.route("/student-dashboard/<enrolment_number>", methods=["GET"])
def student_dashboard(enrolment_number):
    try:
        # ✅ Student info
        student_res = supabase.table("Login") \
            .select("*") \
            .eq("Enrolment_Number", enrolment_number) \
            .execute()

        if not student_res.data:
            return jsonify({"error": "Student not found"}), 404

        student = student_res.data[0]

        # ✅ FIXED: attendance column name
        attendance_res = supabase.table("attendance") \
            .select("*") \
            .eq("Enrolment_Number", enrolment_number) \
            .execute()

        attendance_data = attendance_res.data or []

        total_classes = 40
        attended_classes = len(attendance_data)
        missed_classes = total_classes - attended_classes

        percentage = (attended_classes / total_classes) * 100 if total_classes else 0

        return jsonify({
            "student": {
                "name": student.get("Name_of_Student", "")
            },
            "overview": {
                "total_classes": total_classes,
                "attended_classes": attended_classes,
                "missed_classes": missed_classes,
                "attendance_percentage": round(percentage, 2)
            }
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": "Internal server error"}), 500


@app.route("/mark-attendance", methods=["POST"])
def mark_attendance():
    try:
        data = request.get_json()

        enrolment_number = data.get("enrolment_number")  # ⚠️ FIXED NAME
        name = data.get("name")
        today = str(date.today())

        existing = supabase.table("attendance") \
            .select("*") \
            .eq("enrolment_number", enrolment_number) \
            .eq("date", today) \
            .execute()

        if existing.data:
            return jsonify({"message": "Already marked today"})

        supabase.table("attendance").insert({
            "enrolment_number": enrolment_number,
            "name": name,
            "date": today,
            "status": "Attended"
        }).execute()

        return jsonify({"message": "Attendance marked successfully"})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
