Terminator Proxy

Terminator Proxy API for Protein Termination Prediction

A lightweight Vercel serverless API that relays amino acid sequences from an iOS app to a Hugging Face termination model and returns predictions in real-time. No tokens or permanent storage required.

Architecture Overview

The workflow is simple:

The iOS App sends an amino acid sequence to the Vercel API via HTTPS.

Vercel receives the sequence and forwards it to the Hugging Face model endpoint.

The Hugging Face Hub runs the termination prediction model and returns a prediction.

Vercel relays the prediction back to the iOS App, which displays the result to the user.

Roles in Brief

iOS App: input and display

Vercel: secure middleware and request relay

Hugging Face Hub: model computation and prediction

Features

Accepts amino acid sequences via HTTP POST

Returns predictions in JSON format, e.g., {"label":"terminator","score":0.87}

Fully serverless and tokenless

Minimal setup and fast response
