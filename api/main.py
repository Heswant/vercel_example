from fastapi import FastAPI, UploadFile, File, HTTPException
from otterai import OtterAI
import os

app = FastAPI()

@app.get("/api/health")
def health():
    return {"status": "Service is live"}

@app.post("/api/upload")
async def process_audio(file: UploadFile = File(...)):
    # Pull credentials from Vercel Environment Variables
    email = os.getenv("OTTER_EMAIL")
    password = os.getenv("OTTER_PASSWORD")
    
    if not email:
        raise HTTPException(status_code=500, detail="Environment Variable OTTER_EMAIL not set")

    try:
        # Initialize Otter
        otter = OtterAI()
        otter.login(email, password)
        
        # Save audio file to Vercel's temporary storage
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())
            
        # Upload to Otter. Otter handles noise reduction and speaker diarization.
        speech_id = otter.upload_speech(temp_path)
        
        return {
            "status": "Processing",
            "speech_id": speech_id,
            "message": "Otter is separating the 3 speakers and cleaning noise."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
