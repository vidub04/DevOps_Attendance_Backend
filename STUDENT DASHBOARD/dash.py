from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from datetime import date
import os

app = Flask(__name__)

CORS(app, resources={
    r"/*": {"origins": "https://devops-attendance-frontend-xi.vercel.app"}
})

# Supabase
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


# ---------------- HOME ----------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend is running"})


# ---------------- MARK ATTENDANCE ----------------
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


# ---------------- STUDENT DASHBOARD ----------------
@app.route("/student-dashboard/<enrolment_number>", methods=["GET"])
def student_dashboard(enrolment_number):
    try:
        student_res = supabase.table("Login_Attendance") \
            .select("*") \
            .eq("Enrolment_Number", enrolment_number) \
            .execute()

        attendance_res = supabase.table("attendance") \
            .select("*") \
            .eq("enrolment_number", enrolment_number) \
            .execute()

        if not student_res.data:
            return jsonify({"error": "Student not found"}), 404

        student = student_res.data[0]

        total_classes = 40
        attended_classes = len(attendance_res.data)
        missed_classes = total_classes - attended_classes
        percentage = (attended_classes / total_classes) * 100

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
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
