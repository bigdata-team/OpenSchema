def hash_password(password: str, cost: int = 12) -> str:
    import bcrypt

    salt = bcrypt.gensalt(rounds=cost)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode()


def verify_password(password: str, hashed: str) -> bool:
    import bcrypt

    return bcrypt.checkpw(password.encode(), hashed.encode())
