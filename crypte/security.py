import base64
import os
from argon2.low_level import hash_secret_raw, Type # type: ignore


TIME_COST = 3
MEMORY_COST = 65536
PARALLELISM = 4
HASH_LEN = 32

def derive_key(password: str, salt: bytes) -> bytes:
    raw_key = hash_secret_raw(
        secret=password.encode(),
        salt=salt,
        time_cost=TIME_COST,
        memory_cost=MEMORY_COST,
        parallelism=PARALLELISM,
        hash_len=HASH_LEN,
        type=Type.ID
    )
    return base64.urlsafe_b64encode(raw_key)

def test_decryption(file_path: str, key_obj) -> bool:
    if not os.path.exists(file_path):
        return True
    try:
        with open(file_path, "rb") as f:
            f.seek(16)
            line = f.readline()
            if not line:
                return True
            key_obj.decrypt(line.strip())
            return True
    except Exception:
        return False