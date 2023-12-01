import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization

from utils.utils import Utils
from static_data.constants import *


class DigitalSignature:
    def __init__(self):
        self.privateKey, self.publicKey = self.__generate_rsa_key_pair()

    @staticmethod
    def __generate_rsa_key_pair():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        public_key = private_key.public_key()

        return private_key, public_key

    def get_signature(self) -> tuple[str, str]:
        plainText = Utils.read_file()

        signature = self.privateKey.sign(
            plainText.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )

        signature = base64.b64encode(signature).decode('utf-8')

        publicKeyString = self.publicKey.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()

        return publicKeyString, signature

    @staticmethod
    def verify_sender_signature(public_key_string: str, sender_signature: str) -> bool:
        plain_text = Utils.read_file(
            file_path=DECRYPTED_TEXT_FILE_PATH,
        )

        signature = base64.b64decode(sender_signature)

        publicKeyBytes = public_key_string.encode('utf-8')

        # Deserialize the PEM-encoded public key
        publicKey = serialization.load_pem_public_key(
            publicKeyBytes,
            backend=default_backend(),
        )

        try:
            publicKey.verify(
                signature,
                plain_text.encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256(),
            )
            return True
        except Exception:
            return False
