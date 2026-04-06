import os
from pathlib import Path
from uuid import uuid4

from flask import Flask, redirect, render_template_string, request, url_for
from werkzeug.utils import secure_filename


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = int(
    os.getenv("MAX_CONTENT_LENGTH_MB", "100")
) * 1024 * 1024


HTML_PAGE = """
<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>File Upload Server</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      max-width: 680px;
      margin: 48px auto;
      padding: 0 16px;
      line-height: 1.5;
    }
    .box {
      border: 1px solid #d0d7de;
      border-radius: 12px;
      padding: 24px;
      background: #f6f8fa;
    }
    .message {
      margin-bottom: 16px;
      padding: 12px 16px;
      border-radius: 8px;
      background: #e7f5ff;
    }
    button {
      padding: 10px 16px;
      border: 0;
      border-radius: 8px;
      cursor: pointer;
      background: #0969da;
      color: white;
    }
  </style>
</head>
<body>
  <h1>Upload tệp tin</h1>
  {% if message %}
    <div class="message">{{ message }}</div>
  {% endif %}
  <div class="box">
    <form action="{{ url_for('upload_file') }}" method="post" enctype="multipart/form-data">
      <p>
        <input type="file" name="file" required>
      </p>
      <button type="submit">Tải lên</button>
    </form>
    <p>Tệp sẽ được lưu vào thư mục <code>uploads/</code>.</p>
  </div>
</body>
</html>
"""


def build_unique_path(filename: str) -> Path:
    safe_name = secure_filename(filename) or f"upload-{uuid4().hex}"
    target = UPLOAD_DIR / safe_name

    if not target.exists():
        return target

    stem = target.stem
    suffix = target.suffix
    return UPLOAD_DIR / f"{stem}-{uuid4().hex[:8]}{suffix}"


@app.get("/")
def index():
    return render_template_string(HTML_PAGE, message=request.args.get("message"))


@app.post("/upload")
def upload_file():
    uploaded_file = request.files.get("file")
    if uploaded_file is None:
        return redirect(url_for("index", message="Khong tim thay tep trong request."))

    if uploaded_file.filename == "":
        return redirect(url_for("index", message="Ban chua chon tep de tai len."))

    save_path = build_unique_path(uploaded_file.filename)
    uploaded_file.save(save_path)

    message = f"Upload thanh cong: {save_path.name}"
    return redirect(url_for("index", message=message))


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    app.run(host=host, port=port, debug=True)
