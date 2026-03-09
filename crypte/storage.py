import json
import os
from cryptography.fernet import Fernet

SALT_SIZE = 16

def get_or_create_salt(file_path: str) -> bytes:
    if os.path.exists(file_path) and os.path.getsize(file_path) >= SALT_SIZE:
        with open(file_path, "rb") as f:
            return f.read(SALT_SIZE)
    return os.urandom(SALT_SIZE)

def load_encrypted_entries(file_path: str, key_obj) -> list[dict]:
    entries = []
    if not os.path.exists(file_path):
        return entries

    with open(file_path, "rb") as f:
        f.seek(SALT_SIZE)
        for line in f:
            try:
                data = json.loads(key_obj.decrypt(line.strip()).decode())
                entries.append(data)
            except Exception:
                continue
    return entries

def save_all_entries(file_path: str, key_obj, entries: list[dict], salt: bytes) -> None:
    with open(file_path, "wb") as f:
        f.write(salt)
        for data in entries:
            f.write(key_obj.encrypt(json.dumps(data).encode()) + b"\n")

def append_entry(file_path: str, key_obj, entry: dict, salt: bytes) -> None:
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, "wb") as f:
            f.write(salt)
    
    with open(file_path, "ab") as f:
        f.write(key_obj.encrypt(json.dumps(entry).encode()) + b"\n")