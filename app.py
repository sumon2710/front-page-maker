from flask import Flask, render_template, request, send_file
import pdfkit
from io import BytesIO
from datetime import datetime
import os

app = Flask(__name__)

# Path to wkhtmltopdf executable (update if installed elsewhere)
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    form = request.form
    data = {
        "subject": form.get("subject", ""),
        "title": form.get("title", ""),
        "submitted_to": form.get("submitted_to", ""),
        "submitted_by": form.get("submitted_by", ""),
        "footer": form.get("footer", ""),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Render HTML with user data
    rendered = render_template("preview.html", **data)

    # Convert HTML → PDF using pdfkit with configuration
    pdf_bytes = pdfkit.from_string(rendered, False, configuration=config)

    return send_file(
        BytesIO(pdf_bytes),
        as_attachment=True,
        download_name="frontpage.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)
