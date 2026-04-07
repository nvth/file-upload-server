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

- Drag-and-drop upload interface at `/`
- Lists files from the server's current working directory
- Lets you download files from the current working directory
- Accepts files via `POST /upload`
- Saves uploaded files to the `uploads/` directory
- Automatically renames files when a name conflict occurs
- Shows recent uploaded files with download links

## Configuration

- `HOST`: bind address, default `0.0.0.0`
- `PORT`: server port, default `8000`
