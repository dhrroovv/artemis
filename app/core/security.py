from pwdlib import PasswordHash


class Passwords:
    password_hash = PasswordHash.recommended()

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.password_hash.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        return cls.password_hash.verify(password, hashed_password)
