from flask import Flask, render_template_string, request, send_file
import pdfkit
from io import BytesIO
import os
import platform

app = Flask(__name__)

# Detect OS and set wkhtmltopdf path
if platform.system() == "Windows":
    WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
else:
    WKHTMLTOPDF_PATH = "/usr/bin/wkhtmltopdf"

config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

# HTML template inside Python
HTML_TEMPLATE = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Front Page</title>
    <style>
      body { font-family: "Times New Roman", serif; margin: 0; padding: 0; }
      .border-box { border: 3px solid black; margin: 40px; padding: 60px; min-height: 1000px;
        display: flex; flex-direction: column; justify-content: space-between; }
      .header { text-align: center; margin-top: 40px; }
      .subject { font-size: 20px; font-weight: bold; margin-bottom: 60px; }
      .title { font-size: 32px; font-weight: bold; line-height: 1.5; text-transform: uppercase; }
      .topic { font-size: 22px; font-weight: bold; margin-top: 20px; text-transform: uppercase; }
      .footer-section { display: flex; justify-content: space-between; margin-top: 120px; font-size: 16px; }
      .footer-section .block { width: 45%; }
      .footer-section b { display: block; margin-bottom: 8px; font-size: 18px; }
      .value { white-space: pre-line; line-height: 1.5; }
    </style>
  </head>
  <body>
    <div class="border-box">
      <div class="header">
        <div class="subject">SUB – {{ subject }}</div>
        <div class="title">{{ title }}</div>
        {% if topic %}
        <div class="topic">ON<br>{{ topic }}</div>
        {% endif %}
      </div>
      <div class="footer-section">
        <div class="block">
          <b>Submitted to</b>
          <div class="value">{{ submitted_to }}</div>
        </div>
        <div class="block">
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
    return """
    <h2>Front Page Maker</h2>
    <form method="post" action="/generate">
      Subject: <input type="text" name="subject"><br><br>
      Title: <input type="text" name="title"><br><br>
      Topic: <input type="text" name="topic"><br><br>
      Submitted to:<br>
      <textarea name="submitted_to" rows="4" cols="40"></textarea><br><br>
      Submitted by:<br>
      <textarea name="submitted_by" rows="4" cols="40"></textarea><br><br>
      <button type="submit">Generate PDF</button>
    </form>
    """

@app.route("/generate", methods=["POST"])
def generate():
    data = {
        "subject": request.form.get("subject", ""),
        "title": request.form.get("title", ""),
        "topic": request.form.get("topic", ""),
        "submitted_to": request.form.get("submitted_to", ""),
        "submitted_by": request.form.get("submitted_by", ""),
    }

    rendered = render_template_string(HTML_TEMPLATE, **data)
    pdf_bytes = pdfkit.from_string(rendered, False, configuration=config)

    return send_file(
        BytesIO(pdf_bytes),
        as_attachment=True,
        download_name="frontpage.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
