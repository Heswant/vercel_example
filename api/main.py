from fastapi import FastAPI, UploadFile, File, HTTPException
from otterai import OtterAI
import os

# --- THIS IS STEP 3: DEFINING 'app' ---
app = FastAPI() 

@app.get("/api/health")
def health_check():
    """This helps you test if the deployment is live"""
    return {"status": "success", "message": "Python backend is active"}

@app.post("/api/upload")
async def handle_audio_upload(file: UploadFile = File(...)):
    """This handles your 3-speaker noisy audio"""
    email = os.getenv("OTTER_EMAIL")
    password = os.getenv("OTTER_PASSWORD")
    
    if not email or not password:
        return {"error": "Otter credentials missing in Vercel settings"}

    try:
        otter = OtterAI()
        otter.login(email, password)
        
        # Temporary storage on Vercel
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())
            
        # Upload to Otter
        speech_id = otter.upload_speech(temp_path)
        return {"status": "processing", "speech_id": speech_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
