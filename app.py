from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request
import PyPDF2
from PIL import Image
import pytesseract
import requests
import base64
import os

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set in environment variables")

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\shrad\OneDrive\Desktop\tesseract.exe"

def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

def prepare_image_for_gemini(file):
    img_bytes = file.read()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")
    return {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}

def get_summary(text=None, image_part=None, length="medium"):
    headers = {"Content-Type": "application/json"}
    prompt = f"Summarize the following content in a {length} length without Markdown symbols (*, **, -)."
    parts = [{"text": prompt}]
    if text:
        parts.append({"text": text})
    if image_part:
        parts.append(image_part)
    data = {"contents": [{"parts": parts}]}

    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return "No summary returned"
    else:
        return f"Error: {response.status_code} - {response.text}"

def get_areas_of_improvement(text=None, image_part=None):
    headers = {"Content-Type": "application/json"}
    prompt = (
        "Based on the following content, provide 'Areas of Improvement'. "
        "List them as simple bullet points without Markdown symbols (*, **, -)."
    )
    parts = [{"text": prompt}]
    if text:
        parts.append({"text": text})
    if image_part:
        parts.append(image_part)
    data = {"contents": [{"parts": parts}]}

    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        try:
            raw_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            cleaned = []
            seen = set()
            for line in raw_text.splitlines():
                line = line.strip()
                if not line:
                    continue
                line = line.lstrip("*").lstrip("-").lstrip().replace("**", "").strip()
                if line.lower() not in seen:
                    cleaned.append("• " + line)
                    seen.add(line.lower())
            return "\n".join(cleaned)
        except (KeyError, IndexError):
            return "No areas of improvement returned"
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route("/", methods=["GET", "POST"])
def index():
    summary, improvements = "", ""
    if request.method == "POST":
        file = request.files.get("file")
        summary_length = request.form.get("summary_length", "medium")
        if file:
            filename = file.filename.lower()
            if filename.endswith(".pdf"):
                text = extract_text_from_pdf(file)
                if text.strip():
                    summary = get_summary(text=text, length=summary_length)
                    improvements = get_areas_of_improvement(text=text)
                else:
                    summary = "No text found in PDF."
            elif filename.endswith((".png", ".jpg", ".jpeg")):
                image_part = prepare_image_for_gemini(file)
                summary = get_summary(image_part=image_part, length=summary_length)
                improvements = get_areas_of_improvement(image_part=image_part)
            else:
                summary = "Unsupported file format."
    return render_template("index.html", summary=summary, improvements=improvements)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
