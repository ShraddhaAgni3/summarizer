from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"

# ---- Simple text processor ----
def process_text(text, instruction):
    # Return the full text with the instruction prepended
    return f"Instruction: {instruction}\n\n{text}"

# ---- Main Page ----
@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    if request.method == "POST":
        action = request.form.get("action")   # either "file" or "custom"
        instruction = request.form.get("instruction", "Summarize")

        if action == "file":
            file = request.files["file"]
            if file:
                transcript = file.read().decode("utf-8", errors="ignore")
                summary = process_text(transcript, instruction)
        elif action == "custom":
            custom_text = request.form.get("custom_text")
            if custom_text.strip():
                summary = process_text(custom_text, instruction)

    return render_template("index.html", summary=summary)

# ---- Email Sending ----
@app.route("/send_email", methods=["POST"])
def send_email():
    edited_summary = request.form["edited_summary"]
    recipient = request.form["recipient"]

    # ✅ Now sender email & password will come from the UI
    sender_email = request.form["sender_email"]
    sender_password = request.form["sender_password"]
    subject = "Shared Summary"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(edited_summary, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.quit()
        flash("✅ Email sent successfully!", "success")
    except Exception as e:
        flash(f"❌ Failed to send email: {str(e)}", "error")

    return redirect(url_for("index"))

# ---- Run Server ----
if __name__ == "__main__":
    app.run(debug=True)
