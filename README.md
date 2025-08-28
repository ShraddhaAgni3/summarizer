# Document Summarizer & Improvement Analyzer  

This project is a **Flask-based web application** that allows users to upload PDF or image files. It extracts text using **PyPDF2** (for PDFs) or **Tesseract OCR** (for images), sends the extracted text to **Google Gemini API**, and generates:  

- 📝 A **summary** of the document  
- 🎯 **Areas of improvement** based on the content  

---

# Features
- 📂 Upload **PDFs** and **images** (`.jpg`, `.jpeg`, `.png`)  
- 📝 Extract text using **PyPDF2** (text PDFs) and **Tesseract OCR** (scanned images)  
- 🤖 Uses **Gemini API** (`gemini-1.5-flash`) for summarization and improvements  
- 🎯 Choose summary length: **short**, **medium**, **long**  
- 🌐 Simple web interface built with **Flask + HTML (Jinja2 templates)**  

---

# Tech Stack
- **Backend:** Python, Flask  
- **Text Extraction:** PyPDF2, pytesseract, Pillow  
- **AI Model:** Google Gemini API  
- **Frontend:** HTML, Jinja2  

---

# Clone the Repository
```bash
git clone https://github.com/ShraddhaAgni3/summarizer
cd summarizer
