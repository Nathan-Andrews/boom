import bcrypt
import secrets
import time

import api.boomjson as bj # cfg helper functions

API_KEY_LIFETIME = 3600 * 24 * 30 # 30 days

def hash_password(raw):
    return bcrypt.hashpw(raw.encode(), bcrypt.gensalt()).decode()

def verify_password(raw, hashed):
    return bcrypt.checkpw(raw.encode(), hashed.encode())

def generate_api_key():
    key = secrets.token_hex(32)
    expires = int(time.time()) + API_KEY_LIFETIME
    return key, expires

def validate_key(api_key):
    users = bj.load_users()
    now = int(time.time())

    for username, u in users.items():
        if u.get("api_key") == api_key:
            if u.get("api_key_expires", 0) < now:
                return False, None  # Expired
            return True, username

    if api_key == DEFKEY:
        return True, "default"

    return False, None

DEFKEY, _ = generate_api_key()


