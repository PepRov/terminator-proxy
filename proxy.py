from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from gradio_client import Client

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to your Hugging Face Space
# Ensure this matches exactly the Space URL
client = Client("Ym420/terminator-classification-space")  # public space

class SequenceRequest(BaseModel):
    sequence: str

@app.get("/")
def root():
    return {"message": "Proxy server running"}

@app.post("/predict")
def predict(req: SequenceRequest):
    try:
        # --- Debug: print exact sequence received ---
        print("✅ Received sequence from client:", repr(req.sequence))

        # --- Call the HF Space API endpoint ---
        # The api_name must match the gr.api() name in app.py exactly
        result = client.predict(
            sequence=req.sequence,
            api_name="predict_terminator"  # remove leading slash
        )

        print("✅ Raw result from HF client:", result)

        # --- Handle list-wrapped tuple from Gradio ---
        if isinstance(result, list) and len(result) == 1:
            result = result[0]

        # --- Extract label and confidence safely ---
        if isinstance(result, (list, tuple)) and len(result) == 2:
            label = str(result[0])
            confidence = float(result[1])
        else:
            label = "error"
            confidence = 0.0

        # --- Debug logs for Vercel ---
        print("Sequence  :", req.sequence)
        print("Prediction:", label)
        print("Confidence:", confidence)
        print("-----------------------")

        # --- Return JSON to iOS client ---
        return {
            "sequence": req.sequence,
            "prediction": label,
            "confidence": round(confidence, 4)
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "sequence": req.sequence,
            "prediction": "error",
            "confidence": 0.0,
            "error": str(e)
        }
