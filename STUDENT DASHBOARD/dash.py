from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from datetime import date
import os

app = Flask(__name__)

# ✅ CORS
CORS(
    app,
    resources={r"/*": {"origins": "https://devops-attendance-frontend-xi.vercel.app"}},
    supports_credentials=True
)

# ✅ Supabase connection
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


# ---------------- HOME ----------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend is running"})


# ---------------- DASHBOARD ----------------
@app.route("/student-dashboard/<enrolment_number>", methods=["GET"])
def get_dashboard(enrolment_number):
    try:
        response = (
            supabase.table("Login_Attendance")
            .select("*")
            .eq("Enrolment_Number", enrolment_number)
            .execute()
        )

        data = response.data

        if not data:
            return jsonify({"error": "Student not found"}), 404

        student = data[0]

        total_classes = 40
        attended_classes = 32
        missed_classes = total_classes - attended_classes
        percentage = (attended_classes / total_classes) * 100

        return jsonify({
            "student": {
                "name": student.get("Name_of_Student", ""),
                "branch": student.get("Branch", ""),
                "semester": student.get("Semester", ""),
                "email": student.get("College_Email", "")
            },
            "overview": {
                "total_classes": total_classes,
                "attended_classes": attended_classes,
                "missed_classes": missed_classes,
                "attendance_percentage": round(percentage, 2)
            },
            "alerts": [
                "Attendance below 75%"
            ]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500




# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)