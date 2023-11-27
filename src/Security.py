import bcrypt


class SecurityManager:
    @staticmethod
    def generate_hash(password: str) -> bytes:
        hashed = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )
        return hashed

    @staticmethod
    def compare(password: str, hashed: bytes) -> bool:
        result = bcrypt.hashpw(
            password.encode('utf-8'),
            hashed
        ) == hashed
        return result


if __name__ == "__main__":
    x = SecurityManager.generate_hash("senha_difícil")
    print(x)
    # b'$2b$12$k.4mDLFGbKbJgDyDkVupFeFj9RsthpuH6EBfx2wUjf9QKHrcludMy'
