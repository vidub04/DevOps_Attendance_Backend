from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

# 📦 Data to insert
data = {
    "Enrolment_Number": "07801192024",
    "Name_of_Student": "Vidushi bhardwaj",
    "Branch": "AIML",
    "College_Email": "def@igdtuw.com",
    "Semester":"4",
    "Password":"goooodoo"
}

# 🚀 Insert into table
response = supabase.table("Login_Attendance").insert(data).execute()

print(response)