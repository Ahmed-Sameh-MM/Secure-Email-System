from src.encryption import Encryption
from src.hash import Hash
from static_data.constants import *

if __name__ == '__main__':
    h = Hash()

    h.write_hash_text_to_file()

    key = b"1234567812345678"
    Encryption().encrypt_file(key, PLAIN_TEXT_FILE_PATH, CIPHER_TEXT_FILE_PATH)

    # Encryption().decrypt_file(key, CIPHER_TEXT_FILE_PATH, DECRYPTED_TEXT_FILE_PATH)
