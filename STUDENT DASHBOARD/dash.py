from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://devops-attendance-frontend-xi.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Supabase connection
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


@app.get("/")
def home():
    return {"message": "Backend is running"}


@app.get("/student-dashboard/{enrolment_number}")
def get_dashboard(enrolment_number: str):
    try:
        response = (
            supabase.table("Login_Attendance")
            .select("*")
            .eq("Enrolment_Number", enrolment_number)
            .execute()
        )

        data = response.data

        if not data:
            return {"error": "Student not found"}

        student = data[0]

        total_classes = 40
        attended_classes = 32
        missed_classes = total_classes - attended_classes
        percentage = (attended_classes / total_classes) * 100

        return {
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
        }

    except Exception as e:
        return {
            "error": str(e)
        }
        from datetime import date

@app.post("/mark-attendance")
def mark_attendance(data: dict):
    try:
        enrolment_number = data["enrollment_number"]
        name = data["name"]
        today = str(date.today())

        # prevent duplicate marking
        existing = supabase.table("attendance") \
            .select("*") \
            .eq("enrollment_number", enrolment_number) \
            .eq("date", today) \
            .execute()

        if existing.data:
            return {"message": "Already marked today"}

        supabase.table("attendance").insert({
            "enrollment_number": enrolment_number,
            "name": name,
            "date": today,
            "status": "Attended"
        }).execute()

        return {"message": "Attendance marked successfully"}

    except Exception as e:
        return {"error": str(e)}
        @app.options("/{full_path:path}")
def preflight(full_path: str):
    return {"message": "OK"}
