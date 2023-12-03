from src.encryption import Encryption
from src.hash import Hash
from src.digital_signature import DigitalSignature
from model_classes.security_info import SecurityInfo
from utils.utils import Utils

from static_data.constants import *

if __name__ == "__main__":
    # Sender Side

    hashText = Hash().generate_hash_text()

    key = b"1234567812345678"
    Encryption().encrypt_file(key, PLAIN_TEXT_FILE_PATH, CIPHER_TEXT_FILE_PATH)

    publicKey, digitalSignature = DigitalSignature().get_signature(
        plain_text_file_path=PLAIN_TEXT_FILE_PATH
    )

    senderSecurityInfo = SecurityInfo(
        hash_text=hashText,
        public_key=publicKey,
        digital_signature=digitalSignature,
    )

    Utils.write_security_info_file(
        security_info=senderSecurityInfo,
    )

    # Receiver Side

    Encryption().decrypt_file(key, CIPHER_TEXT_FILE_PATH, DECRYPTED_TEXT_FILE_PATH)

    receiverSecurityInfo = Utils.read_security_info_file(SECURITY_INFO_FILE_PATH)

    print(
        Hash.verify_hash(
            sender_hash=receiverSecurityInfo.hashText,
            decrypted_text_file_path=DECRYPTED_TEXT_FILE_PATH,
        )
    )

    print(
        DigitalSignature.verify_sender_signature(
            public_key_string=receiverSecurityInfo.publicKey,
            sender_signature=receiverSecurityInfo.digitalSignature,
            decrypted_file_path=DECRYPTED_TEXT_FILE_PATH,
        )
    )
