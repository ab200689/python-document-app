
import os
from flask import Flask, request, render_template_string
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

FULL_NAME = "Aysel Baghirova"
GROUP = "Computer Engineering - 4th Year"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Aysel's Python Application</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #eef3ff;
            margin: 0;
            padding: 50px 20px;
            color: #222;
        }
        main {
            background: white;
            max-width: 520px;
            margin: auto;
            padding: 35px;
            border-radius: 16px;
            box-shadow: 0 8px 25px #0001;
            text-align: center;
        }
        h1 { color: #1759c7; }
        .info {
            background: #f1f5ff;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
        }
        input { max-width: 100%; }
        button {
            background: #1759c7;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
        }
        .message { margin-top: 20px; overflow-wrap: anywhere; }
    </style>
</head>
<body>
    <main>
        <h1>My Python Application</h1>
        <div class="info">
            <h2>{{ name }}</h2>
            <p>{{ group }}</p>
        </div>
        <h3>Upload a Document</h3>
        <p>Select a PDF, DOC, DOCX or TXT file (maximum 10 MB).</p>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="document"
                   accept=".pdf,.doc,.docx,.txt" required>
            <p><button type="submit">Upload Document</button></p>
        </form>
        <div class="message">{{ message }}</div>
    </main>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        file = request.files.get("document")

        if not file or not file.filename:
            message = "Please select a document."
        else:
            filename = secure_filename(file.filename)
            allowed = {"pdf", "doc", "docx", "txt"}

            if not filename or "." not in filename:
                message = "Invalid filename."
            elif filename.rsplit(".", 1)[1].lower() not in allowed:
                message = "Unsupported file type."
            else:
                message = f"Document received: {filename}"

    return render_template_string(
        HTML,
        name=FULL_NAME,
        group=GROUP,
        message=message
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
