from supabase import create_client, Client

# 🔑 Supabase credentials
url = "https://befrnamptjppdadsrrpo.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJlZnJuYW1wdGpwcGRhZHNycnBvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTkwNjE3NywiZXhwIjoyMDkxNDgyMTc3fQ.WMN3xCKnUNDmKYlQksZWcxRb1eHlQ13H4azyDiOi-NE"

supabase: Client = create_client(url, key)

# 📦 Data to insert
data = {
    "Enrolment_Number": "07701192024",
    "Name_of_Student": "Vanshika Yadav",
    "Branch": "AIML",
    "College_Email": "abc@igdtuw.com",
    "Semester":"4"
}

# 🚀 Insert into table
response = supabase.table("Login_Attendance").insert(data).execute()

print(response)