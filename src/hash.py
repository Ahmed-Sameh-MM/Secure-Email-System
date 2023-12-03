from hashlib import sha256
from utils.utils import Utils


class Hash:
    def __init__(self, plain_text_path: str = None):
        if plain_text_path is not None:
            self.plainText = Utils.read_file(
                file_path=plain_text_path,
            )

        else:
            self.plainText = Utils.read_file()

        self.hash = sha256()

    def generate_hash_text(self) -> str:
        self.hash.update(self.plainText.encode())

        return self.hash.hexdigest()

    @staticmethod
    def verify_hash(sender_hash: str, decrypted_text_file_path) -> bool:
        h = Hash(
            plain_text_path=decrypted_text_file_path,
        )

        hashText = h.generate_hash_text()

        if sender_hash == hashText:
            return True

        return False
