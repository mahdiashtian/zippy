from src.users.utils import check_password, hash_password


class PasswordHash:
    def __init__(self, hash_: bytes):
        try:
            assert len(hash_) == 60, 'bcrypt hash should be 60 chars.'
            assert hash_.count(b'$') == 3, 'bcrypt hash should have 3x "$".'
            self.hash = hash_.decode('utf-8')
            self.rounds = int(self.hash.split('$')[2])
        except (AssertionError, IndexError) as e:
            raise ValueError("Invalid bcrypt hash provided") from e

    def __eq__(self, candidate: str) -> bool:
        if isinstance(candidate, self.__class__):
            candidate = candidate.hash
        return check_password(candidate, self.hash.encode('utf-8'))

    def __repr__(self) -> str:
        return f'<{type(self).__name__}>'

    @classmethod
    def new(cls, password: str, rounds: int) -> 'PasswordHash':
        hashed = hash_password(password, rounds)
        return cls(hashed)
