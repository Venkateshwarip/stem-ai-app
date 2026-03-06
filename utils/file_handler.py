# utils/file_handler.py
from pathlib import Path
import base64

def save_uploaded_file(upload, dest_folder: Path):
    dest_folder.mkdir(parents=True, exist_ok=True)
    dest = dest_folder / upload.name
    with dest.open("wb") as f:
        f.write(upload.getbuffer())
    return dest

def file_download_link(path: Path, label="Download"):
    b64 = base64.b64encode(path.read_bytes()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{path.name}">{label}</a>'
    return href
