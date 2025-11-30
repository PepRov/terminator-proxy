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
        # --- Debug: print exact sequence received ---
        print("✅ Received sequence:", repr(req.sequence))

        # Call the HF Space API endpoint
        result = client.predict(
            sequence=req.sequence,
            api_name="/predict_terminator"  # note the leading slash
        )

        print("✅ Raw result from HF:", result)

        raw_label = result[0]
        #confidence = result[1]
        #confidence = float(result[1]) if isinstance(result[1], (int, float, str)) else 0.0

        # Expecting tuple like ("Promoter", 0.92)
        if isinstance(result, (list, tuple)) and len(result) >= 2:
            label = str(result[0])
            confidence = float(result[1])
        else:
            label = "error"
            confidence = 0.0

        # --- Step 2.4: Prepare payload for Google Sheet ---
        payload = {
            "sequence": req.sequence,
            "secret_token": SECRET_TOKEN_Terminator
        }
        headers = {"Content-Type": "application/json"}

        # --- Step 2.5: POST to Google Sheet ---
        try:
            r = requests.post(SHEET_URL_Terminator, json=payload, headers=headers)
            print("✅ Sheet response:", r.text)
        except Exception as sheet_err:
            print("❌ Failed to save to Google Sheet:", sheet_err)
        # ---------------------------------------------------
        
            
        # Debug logs for Vercel
        print("Sequence  :", req.sequence)
        print("Prediction:", label)
        print("Confidence:", confidence)
        print("-----------------------")

        return {
            "sequence": req.sequence,
            "prediction": label,
            "confidence": float(confidence)
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "sequence": req.sequence,
            "prediction": "error",
            "confidence": 0.0,
            "error": str(e)
        }

