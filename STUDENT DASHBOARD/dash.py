from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase connection
url = "https://befrnamptjppdadsrrpo.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJlZnJuYW1wdGpwcGRhZHNycnBvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTkwNjE3NywiZXhwIjoyMDkxNDgyMTc3fQ.WMN3xCKnUNDmKYlQksZWcxRb1eHlQ13H4azyDiOi-NE"

supabase: Client = create_client(url, key)


@app.get("/")
def home():
    return {"message": "Backend is running"}


@app.get("/student-dashboard/{enrolment_number}")
def get_dashboard(enrolment_number: str):
    try:
        print("Checking enrolment number:", enrolment_number)

        response = (
            supabase.table("Login_Attendance")
            .select("*")
            .eq("Enrolment_Number", enrolment_number)
            .execute()
        )

        print("Supabase raw response:", response)

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
                "Attendance below 75% in DBMS"
            ]
        }

    except Exception as e:
        return {
            "error_type": type(e).__name__,
            "error_message": str(e)
        }
