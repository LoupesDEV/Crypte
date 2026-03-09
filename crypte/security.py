import base64
import hashlib
import os



def derive_key(password: str) -> bytes:
    digest = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(digest)



def test_decryption(file_path: str, key) -> bool:
    if not os.path.exists(file_path):
        return True

    with open(file_path, "rb") as f:
        line = f.readline()
        if not line:
            return True
        try:
            key.decrypt(line.strip())
            return True
        except Exception:
            return False
