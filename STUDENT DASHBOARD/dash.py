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



# ---------------- STUDENT DASHBOARD ----------------


if __name__ == "__main__":
    app.run(debug=True)
