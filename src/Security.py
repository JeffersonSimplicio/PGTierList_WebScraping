import bcrypt


class SecurityManager:
    @staticmethod
    def generate_hash(password: str) -> bytes:
        hashed = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )
        return hashed
