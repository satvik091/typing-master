from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os


API_KEY = os.getenv("AIzaSyBPDNB9oDlVpJlTdEkEnc7vWv_CsAZiVQ0")  # Make sure your API key is set in the environment variables
genai.configure(api_key=API_KEY)

app = Flask(__name__)

def generate_paragraph(length):
    """Generate a paragraph with the specified length using Google Gemini API."""
    try:
        # Corrected way of setting up the model based on available API (assuming `genai.GenerativeModel` or equivalent)
        model = genai.Model("gemini-pro")  # Adjust this based on the actual gemini API you're using

        # Define prompts based on length
        prompts = {
            "short": "Write a short paragraph (2-3 sentences) for a typing speed test.",
            "medium": "Write a medium-length paragraph (4-6 sentences) for a typing speed test.",
            "long": "Write a long paragraph (7-10 sentences) for a typing speed test."
        }
        
        prompt = prompts.get(length, prompts["medium"])  # Default to medium if invalid input
        
        # Generate content
        response = model.generate(prompt)

        # Ensure response is valid
        if response and hasattr(response, "text"):
            return response.text.strip()
        else:
            return "Failed to generate a paragraph."

    except Exception as e:
        return f"API Error: {str(e)}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["GET"])
def get_paragraph():
    length = request.args.get("length", "medium")  # Get 'length' parameter (default to medium)
    paragraph = generate_paragraph(length)
    return jsonify({"paragraph": paragraph})

if __name__ == "__main__":
    app.run(debug=True)
