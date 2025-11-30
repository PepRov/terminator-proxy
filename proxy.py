import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from gradio_client import Client
import requests

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Step 0.2: Load environment variables ---
SHEET_URL_Terminator = os.getenv("SHEET_URL_Terminator")
SECRET_TOKEN_Terminator = os.getenv("SECRET_TOKEN_Terminator")

# 🔍 Optional: warn in logs if env vars were not found
if SHEET_URL_Terminator is None:
    print("⚠️ WARNING: SHEET_URL_Terminator is NOT set in environment variables.")

if SECRET_TOKEN_Terminator is None:
    print("⚠️ WARNING: SECRET_TOKEN_Terminator is NOT set in environment variables.")

# Connect to your Hugging Face Space
client = Client("Ym420/terminator-classification-space")  # public space, no token needed

class SequenceRequest(BaseModel):
    sequence: str

@app.get("/")
def root():
    return {"message": "Proxy server running"}

@app.post("/predict")
def predict(req: SequenceRequest):
    try:
        # Debug: print exact sequence received
        print("✅ Received sequence:", repr(req.sequence))

        # Call the HF Space API endpoint
        result = client.predict(
            sequence=req.sequence,
            api_name="/predict_terminator"
        )

        print("✅ Raw result from HF:", result)

        # Parse HF result safely
        if isinstance(result, (list, tuple)) and len(result) >= 2:
            label = str(result[0])
            confidence = float(result[1])
        else:
            label = "error"
            confidence = 0.0

        # Step 2.4: Prepare payload for Google Sheet
        payload = {
            "sequence": req.sequence,
            "secret_token": SECRET_TOKEN_Terminator
        }

        headers = {"Content-Type": "application/json"}

        # Step 2.5: POST to Google Sheet
        try:
            if SHEET_URL_Terminator:
                r = requests.post(SHEET_URL_Terminator, json=payload, headers=headers)
                print("✅ Sheet response:", r.text)
            else:
                print("❌ SHEET_URL_Terminator missing — skipping POST")
        except Exception as sheet_err:
            print("❌ Failed to save to Google Sheet:", sheet_err)

        # Debug logs for Vercel
        print("Sequence  :", req.sequence)
        print("Prediction:", label)
        print("Confidence:", confidence)
        print("-----------------------")

        return {
            "sequence": req.sequence,
            "prediction": label,
            "confidence": confidence
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "sequence": req.sequence,
            "prediction": "error",
            "confidence": 0.0,
            "error": str(e)
        }


