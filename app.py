from flask import Flask, render_template, render_template_string, request, send_file, session
import pdfkit
from io import BytesIO
import os, platform

app = Flask(__name__)
app.secret_key = "secret_key_for_session"  # required for session storage

# Detect OS and set wkhtmltopdf path
if platform.system() == "Windows":
    WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
else:
    WKHTMLTOPDF_PATH = "/usr/bin/wkhtmltopdf"

config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

# ---------------- PDF/Preview Template ----------------
HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Front Page</title>
  <style>
    @page { size: A4; margin: 0; }
    body {
      font-family: "Times New Roman", serif;
      margin: 0; padding: 0;
      background: #f1f1f1;
    }
    .page {
      width: 90vw;
      min-height: 95vh;
      background: #fff;
      margin: auto;
      padding: 40px;
      box-sizing: border-box;

      border: 6px solid #000;
      outline: 2px solid #000;
      outline-offset: -12px;

      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .header { 
      text-align: center; 
      margin-top: 40px; }
    .subject { 
      font-size: 24pt; 
      font-weight: bold; margin-bottom: 100px; text-transform: uppercase; }
    .title { font-size: 48pt; font-weight: bold; line-height: 1.5; text-transform: uppercase; white-space: pre-line; }
    .footer { display: table; width: 100%; margin-top: 60px; font-size: 18pt; }
    .block { display: table-cell; width: 60%; vertical-align: top; }
    .block b { display: block; margin-bottom: 15px; font-size: 18pt; }
    .value { white-space: pre-line; line-height: 1.5; }
    .block.right { text-align: left; }
  </style>
</head>
<body>
  <div class="page">
    <div class="header">
      <div class="subject">{{ subject }}</div>
      <div class="title">{{ title }}</div>
    </div>
    <div class="footer">
      <div class="block">
        <b>Submitted to</b>
        <div class="value">{{ submitted_to }}</div>
      </div>
      <div class="block right">
        <b>Submitted by</b>
        <div class="value">{{ submitted_by }}</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/preview", methods=["POST"])
def preview():
    session["data"] = {
        "subject": request.form.get("subject", ""),
        "title": request.form.get("title", ""),
        "submitted_to": request.form.get("submitted_to", ""),
        "submitted_by": request.form.get("submitted_by", ""),
    }
    return render_template_string(HTML_TEMPLATE, **session["data"])

@app.route("/generate", methods=["POST"])
def generate():
    data = {
        "subject": request.form.get("subject", ""),
        "title": request.form.get("title", ""),
        "submitted_to": request.form.get("submitted_to", ""),
        "submitted_by": request.form.get("submitted_by", ""),
    }

    rendered = render_template_string(HTML_TEMPLATE, **data)

    options = {
        "page-size": "A4",
        "margin-top": "10mm",
        "margin-bottom": "10mm",
        "margin-left": "10mm",
        "margin-right": "10mm"
    }

    pdf_bytes = pdfkit.from_string(rendered, False, configuration=config, options=options)

    return send_file(
        BytesIO(pdf_bytes),
        as_attachment=True,
        download_name="frontpage.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)
