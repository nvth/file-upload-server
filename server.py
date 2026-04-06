import os
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from flask import (
    Flask,
    redirect,
    render_template_string,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


app = Flask(__name__)


HTML_PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Upload Hub</title>
  <style>
    :root {
      --bg: #f4efe7;
      --panel: rgba(255, 252, 247, 0.9);
      --panel-strong: #fffaf2;
      --text: #1f2933;
      --muted: #52606d;
      --line: rgba(31, 41, 51, 0.12);
      --accent: #c05621;
      --accent-dark: #9c4221;
      --accent-soft: rgba(192, 86, 33, 0.12);
      --success-bg: #e6fffa;
      --success-text: #234e52;
      --shadow: 0 18px 50px rgba(120, 82, 56, 0.14);
    }
    body {
      margin: 0;
      min-height: 100vh;
      padding: 32px 18px;
      font-family: "Trebuchet MS", "Segoe UI", sans-serif;
      line-height: 1.5;
      color: var(--text);
      background:
        radial-gradient(circle at top left, rgba(255, 214, 165, 0.8), transparent 34%),
        radial-gradient(circle at bottom right, rgba(196, 181, 253, 0.35), transparent 28%),
        linear-gradient(135deg, #f6f0e8 0%, #efe7dc 100%);
    }
    .shell {
      max-width: 1080px;
      margin: 0 auto;
    }
    .hero {
      display: grid;
      gap: 20px;
      grid-template-columns: 1.3fr 0.9fr;
      align-items: start;
    }
    .hero-card,
    .stats-card,
    .uploads-card {
      background: var(--panel);
      backdrop-filter: blur(12px);
      border: 1px solid var(--line);
      border-radius: 28px;
      box-shadow: var(--shadow);
    }
    .hero-card {
      padding: 32px;
    }
    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 999px;
      color: var(--accent-dark);
      background: var(--accent-soft);
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-weight: 700;
    }
    h1 {
      margin: 18px 0 10px;
      font-family: Georgia, "Times New Roman", serif;
      font-size: clamp(2.4rem, 6vw, 4.6rem);
      line-height: 0.98;
      letter-spacing: -0.03em;
    }
    .lead {
      margin: 0 0 24px;
      max-width: 600px;
      color: var(--muted);
      font-size: 1.04rem;
    }
    .message {
      margin-bottom: 20px;
      padding: 14px 16px;
      border-radius: 16px;
      background: var(--success-bg);
      color: var(--success-text);
      border: 1px solid rgba(35, 78, 82, 0.14);
      font-weight: 600;
    }
    .dropzone {
      position: relative;
      display: grid;
      gap: 14px;
      padding: 26px;
      border: 2px dashed rgba(192, 86, 33, 0.35);
      border-radius: 24px;
      background:
        linear-gradient(180deg, rgba(255, 255, 255, 0.78), rgba(255, 247, 237, 0.92));
      transition: transform 0.18s ease, border-color 0.18s ease, background 0.18s ease;
    }
    .dropzone.dragover {
      transform: translateY(-2px);
      border-color: var(--accent);
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(255, 237, 213, 0.94));
    }
    .dropzone h2 {
      margin: 0;
      font-size: 1.35rem;
    }
    .dropzone p {
      margin: 0;
      color: var(--muted);
    }
    .file-input {
      display: none;
    }
    .actions {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
    }
    .button,
    button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      padding: 12px 18px;
      border: 0;
      border-radius: 14px;
      cursor: pointer;
      text-decoration: none;
      font-weight: 700;
      transition: transform 0.18s ease, opacity 0.18s ease;
    }
    .button:hover,
    button:hover {
      transform: translateY(-1px);
    }
    .button-primary {
      background: var(--accent);
      color: white;
    }
    .button-secondary {
      background: rgba(31, 41, 51, 0.06);
      color: var(--text);
    }
    .file-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
      color: var(--muted);
      font-size: 0.95rem;
    }
    .stats-card {
      padding: 24px;
      display: grid;
      gap: 18px;
    }
    .stats-card h3,
    .uploads-card h3 {
      margin: 0;
      font-size: 1rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
    }
    .stat-grid {
      display: grid;
      gap: 14px;
    }
    .stat {
      padding: 18px;
      border-radius: 20px;
      background: var(--panel-strong);
      border: 1px solid var(--line);
    }
    .stat strong {
      display: block;
      margin-bottom: 6px;
      font-size: 2rem;
      line-height: 1;
      font-family: Georgia, "Times New Roman", serif;
    }
    .stat span {
      color: var(--muted);
    }
    .uploads-card {
      margin-top: 24px;
      padding: 24px;
    }
    .uploads-header {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      margin-bottom: 16px;
    }
    .uploads-list {
      display: grid;
      gap: 12px;
    }
    .upload-item {
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: center;
      padding: 16px 18px;
      border-radius: 18px;
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.72);
    }
    .upload-item strong {
      display: block;
      margin-bottom: 4px;
      word-break: break-word;
    }
    .upload-item span {
      color: var(--muted);
      font-size: 0.92rem;
    }
    .empty {
      padding: 18px;
      border-radius: 18px;
      border: 1px dashed var(--line);
      color: var(--muted);
      background: rgba(255, 255, 255, 0.55);
    }
    code {
      padding: 2px 7px;
      border-radius: 999px;
      background: rgba(31, 41, 51, 0.08);
    }
    @media (max-width: 860px) {
      .hero {
        grid-template-columns: 1fr;
      }
      .hero-card,
      .stats-card,
      .uploads-card {
        border-radius: 22px;
      }
    }
    @media (max-width: 560px) {
      body {
        padding: 18px 12px;
      }
      .hero-card,
      .stats-card,
      .uploads-card {
        padding: 18px;
      }
      .actions,
      .upload-item {
        flex-direction: column;
        align-items: stretch;
      }
    }
  </style>
</head>
<body>
  <div class="shell">
    <section class="hero">
      <div class="hero-card">
        <div class="eyebrow">Simple Python Upload Server</div>
        <h1>Drop a file and ship it.</h1>
        <p class="lead">
          A compact upload dashboard built on Flask. Files are stored in
          <code>uploads/</code>, duplicate names are handled automatically, and
          recent uploads stay visible on the page.
        </p>
        {% if message %}
          <div class="message">{{ message }}</div>
        {% endif %}
        <form action="{{ url_for('upload_file') }}" method="post" enctype="multipart/form-data" id="upload-form">
          <input class="file-input" id="file-input" type="file" name="file" required>
          <div class="dropzone" id="dropzone">
            <h2>Choose a file or drag it here</h2>
            <p>Single file upload, fast path, no extra dependencies beyond Flask.</p>
            <div class="file-meta">
              <span id="file-name">No file selected</span>
              <span id="file-size"></span>
            </div>
            <div class="actions">
              <button class="button button-secondary" id="browse-trigger" type="button">Browse files</button>
              <button class="button-primary" type="submit">Upload now</button>
            </div>
          </div>
        </form>
      </div>

      <aside class="stats-card">
        <h3>Overview</h3>
        <div class="stat-grid">
          <div class="stat">
            <strong>{{ upload_count }}</strong>
            <span>files stored in the uploads directory</span>
          </div>
          <div class="stat">
            <strong>No limit</strong>
            <span>upload size is not restricted by the app</span>
          </div>
          <div class="stat">
            <strong>POST /upload</strong>
            <span>endpoint for multipart form uploads</span>
          </div>
        </div>
      </aside>
    </section>

    <section class="uploads-card">
      <div class="uploads-header">
        <h3>Recent Uploads</h3>
        <span>{{ uploads|length }} shown</span>
      </div>
      {% if uploads %}
        <div class="uploads-list">
          {% for item in uploads %}
            <div class="upload-item">
              <div>
                <strong>{{ item.name }}</strong>
                <span>{{ item.size_label }} - {{ item.modified_label }}</span>
              </div>
              <a class="button button-secondary" href="{{ url_for('download_file', filename=item.name) }}">Download</a>
            </div>
          {% endfor %}
        </div>
      {% else %}
        <div class="empty">No uploaded files yet. The first file you upload will appear here.</div>
      {% endif %}
    </section>
  </div>
  <script>
    const input = document.getElementById("file-input");
    const dropzone = document.getElementById("dropzone");
    const browseTrigger = document.getElementById("browse-trigger");
    const fileName = document.getElementById("file-name");
    const fileSize = document.getElementById("file-size");

    function formatFileSize(bytes) {
      if (!bytes) {
        return "";
      }
      const units = ["B", "KB", "MB", "GB"];
      let value = bytes;
      let index = 0;
      while (value >= 1024 && index < units.length - 1) {
        value /= 1024;
        index += 1;
      }
      return `${value.toFixed(value >= 10 || index === 0 ? 0 : 1)} ${units[index]}`;
    }

    function updateSelectedFile() {
      const file = input.files[0];
      if (!file) {
        fileName.textContent = "No file selected";
        fileSize.textContent = "";
        return;
      }
      fileName.textContent = file.name;
      fileSize.textContent = formatFileSize(file.size);
    }

    input.addEventListener("change", updateSelectedFile);
    browseTrigger.addEventListener("click", () => input.click());
    dropzone.addEventListener("click", (event) => {
      if (event.target.closest("button")) {
        return;
      }
      input.click();
    });

    ["dragenter", "dragover"].forEach((eventName) => {
      dropzone.addEventListener(eventName, (event) => {
        event.preventDefault();
        dropzone.classList.add("dragover");
      });
    });

    ["dragleave", "drop"].forEach((eventName) => {
      dropzone.addEventListener(eventName, (event) => {
        event.preventDefault();
        dropzone.classList.remove("dragover");
      });
    });

    dropzone.addEventListener("drop", (event) => {
      const files = event.dataTransfer.files;
      if (!files.length) {
        return;
      }
      input.files = files;
      updateSelectedFile();
    });
  </script>
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


def format_size(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(num_bytes)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(size)} {unit}"
            return f"{size:.1f} {unit}"
        size /= 1024

    return f"{int(num_bytes)} B"


def list_uploads(limit: int = 10):
    files = []
    for path in UPLOAD_DIR.iterdir():
        if not path.is_file():
            continue
        stat = path.stat()
        files.append(
            {
                "name": path.name,
                "size_label": format_size(stat.st_size),
                "modified_label": stat.st_mtime_ns,
            }
        )

    files.sort(key=lambda item: item["modified_label"], reverse=True)
    recent_files = files[:limit]
    for item in recent_files:
        timestamp = item["modified_label"] / 1_000_000_000
        item["modified_label"] = datetime.fromtimestamp(timestamp).strftime(
            "%Y-%m-%d %H:%M"
        )
    return recent_files, len(files)


@app.get("/")
def index():
    uploads, upload_count = list_uploads()
    return render_template_string(
        HTML_PAGE,
        message=request.args.get("message"),
        uploads=uploads,
        upload_count=upload_count,
    )


@app.post("/upload")
def upload_file():
    uploaded_file = request.files.get("file")
    if uploaded_file is None:
        return redirect(url_for("index", message="No file was found in the request."))

    if uploaded_file.filename == "":
        return redirect(url_for("index", message="Please choose a file to upload."))

    save_path = build_unique_path(uploaded_file.filename)
    uploaded_file.save(save_path)

    message = f"Upload complete: {save_path.name}"
    return redirect(url_for("index", message=message))


@app.get("/files/<path:filename>")
def download_file(filename: str):
    return send_from_directory(UPLOAD_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    app.run(host=host, port=port, debug=True)
