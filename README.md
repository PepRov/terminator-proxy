# terminator-proxy

# Terminator Proxy API for Transcription Termination Prediction

A lightweight Vercel serverless API that relays DNA sequences from an iOS app to a Hugging Face transcription terminator model and returns predictions in real-time. No tokens or permanent storage required.

## Architecture Overview

**The workflow is simple:**

1. The iOS App sends a DNA sequence to the Vercel API via HTTPS.  
2. Vercel receives the sequence and forwards it to the Hugging Face model endpoint.  
3. The Hugging Face Hub runs the transcription termination prediction model and returns a prediction.  
4. Vercel relays the prediction back to the iOS App, which displays the result to the user.

## Roles in Brief

- **iOS App:** input and display  
- **Vercel:** secure middleware and request relay  
- **Hugging Face Hub:** model computation and prediction  

## Features

- Accepts DNA sequences via HTTP POST  
- Returns predictions in JSON format, e.g., `{"label":"terminator","score":0.87}`  
- Fully serverless and tokenless  
- Minimal setup and fast response

## Quick Start

1. Deploy the terminator-proxy API to Vercel (free account works fine).  
2. In your iOS app, send a POST request to the Vercel endpoint with the DNA sequence in JSON, e.g.:

```json
{
    "sequence": "ATGCGTACGTTAGC..."
}
{
    "label": "terminator",
    "score": 0.87
}
