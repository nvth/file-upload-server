# Simple File Upload Server

## Run the server

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

The server runs at `http://127.0.0.1:8000` by default.

## Features

- Simple upload form at `/`
- Accepts files via `POST /upload`
- Saves uploaded files to the `uploads/` directory
- Automatically renames files when a name conflict occurs

## Configuration

- `HOST`: bind address, default `0.0.0.0`
- `PORT`: server port, default `8000`
- `MAX_CONTENT_LENGTH_MB`: maximum upload size in MB, default `100`
