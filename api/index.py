import os
import requests
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.get("/api/health")
def health():
    return {"status": "Live", "message": "No extra libraries needed!"}

@app.post("/api/upload")
async def upload_to_otter(file: UploadFile = File(...)):
    # 1. Get credentials from Vercel settings
    email = os.getenv("OTTER_EMAIL")
    password = os.getenv("OTTER_PASSWORD")
    
    if not email or not password:
        return {"error": "Missing OTTER_EMAIL or OTTER_PASSWORD in Vercel"}

    # 2. Start a session to talk to Otter.ai
    with requests.Session() as s:
        # Login
        login_res = s.post("https://otter.ai/api/v1/login", json={
            "username": email, "password": password
        })
        
        if login_res.status_code != 200:
            return {"error": "Otter Login Failed", "details": login_res.text}

        # 3. Forward the audio file
        audio_content = await file.read()
        upload_res = s.post(
            "https://otter.ai/api/v1/speeches", 
            files={'file': (file.filename, audio_content)}
        )
        
        return {
            "info": "File sent to Otter successfully",
            "otter_response": upload_res.json()
        }
