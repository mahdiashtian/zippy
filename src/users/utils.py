import bcrypt


def hash_password(password: str, rounds=12) -> bytes:
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt(rounds)
    return bcrypt.hashpw(pw, salt)


def check_password(password: str, password_in_db: bytes) -> bool:
    password_bytes = bytes(password, "utf-8")
    return bcrypt.checkpw(password_bytes, password_in_db)
