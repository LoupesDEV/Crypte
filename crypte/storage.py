import json
import os



def load_encrypted_entries(file_path: str, key) -> list[dict]:
    entries: list[dict] = []
    if not os.path.exists(file_path):
        return entries

    with open(file_path, "rb") as f:
        for line in f:
            try:
                data = json.loads(key.decrypt(line.strip()).decode())
                entries.append(data)
            except Exception:
                pass
    return entries



def save_all_entries(file_path: str, key, entries: list[dict]) -> None:
    with open(file_path, "wb") as f:
        for data in entries:
            f.write(key.encrypt(json.dumps(data).encode()) + b"\n")



def append_entry(file_path: str, key, entry: dict) -> None:
    with open(file_path, "ab") as f:
        f.write(key.encrypt(json.dumps(entry).encode()) + b"\n")
