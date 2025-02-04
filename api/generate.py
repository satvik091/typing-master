import google.generativeai as genai
import os
from flask import Flask, jsonify, request

# Configure API key securely (Set it in environment variables)
API_KEY =("AIzaSyBPDNB9oDlVpJlTdEkEnc7vWv_CsAZiVQ0")  # Use the environment variable
genai.configure(api_key=API_KEY)

def generate_paragraph(length):
    """Generate a paragraph with the specified length using Google Gemini API."""
    try:
        model = genai.GenerativeModel("gemini-pro")

        prompts = {
            "short": "Write a short paragraph (2-3 sentences) for a typing speed test.",
            "medium": "Write a medium-length paragraph (4-6 sentences) for a typing speed test.",
            "long": "Write a long paragraph (7-10 sentences) for a typing speed test."
        }

        prompt = prompts.get(length, prompts["medium"])

        response = model.generate_content(prompt)

        if response and hasattr(response, "text"):
            return response.text.strip()
        else:
            return "Failed to generate a paragraph."

    except Exception as e:
        return f"API Error: {str(e)}"

# Serverless function that will handle the requests
def handler(event, context):
    length = event.get("queryStringParameters", {}).get("length", "medium")  # Get 'length' parameter
    paragraph = generate_paragraph(length)

    return {
        "statusCode": 200,
        "body": jsonify({"paragraph": paragraph}),
        "headers": {
            "Content-Type": "application/json",
        }
    }
