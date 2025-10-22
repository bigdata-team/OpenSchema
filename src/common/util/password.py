def hash_password(password: str, cost: int = 12) -> str:
    import bcrypt

    salt = bcrypt.gensalt(rounds=cost)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode()


def verify_password(password: str, hashed_password: str) -> bool:
    import bcrypt

    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except ValueError:
        return False
