from Crypto.Cipher import AES
from static_data.constants import *


class Encryption:
    @staticmethod
    def encrypt_file(
        key,
        in_filename: str = PLAIN_TEXT_FILE_PATH,
        out_filename: str = CIPHER_TEXT_FILE_PATH,
        chunk_size: int = 16,
    ):
        """Encrypts a file using AES (ECB mode) with the given key.
        key: The encryption key - a string that must be either 16, 24 or 32 bytes long. Longer keys are more secure.
        in_filename:Name of the input file
        out_filename: If None, CIPHER_TEXT_FILE_PATH will be used.
        chunk_size: Sets the size of the chunk which the function uses to read and encrypt the file. Larger chunk sizes can be faster for some files and machines. chunk_size must be divisible by 16.
        """

        encryptor = AES.new(key, AES.MODE_ECB)

        with open(in_filename, "rb") as infile:
            with open(out_filename, "wb") as outfile:
                while True:
                    chunk = infile.read(chunk_size)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b" " * (16 - len(chunk) % 16)

                    outfile.write(encryptor.encrypt(chunk))

    @staticmethod
    def decrypt_file(
        key,
        in_filename: str = CIPHER_TEXT_FILE_PATH,
        out_filename: str = DECRYPTED_TEXT_FILE_PATH,
        chunk_size: int = 16,
    ):
        """Decrypts a file using AES (ECB mode) with the
        given key. Parameters are similar to encrypt_file.
        """

        with open(in_filename, "rb") as infile:
            decryptor = AES.new(key, AES.MODE_ECB)
            with open(out_filename, "wb") as outfile:
                while True:
                    chunk = infile.read(chunk_size)
                    if len(chunk) == 0:
                        break

                    decryptedString = decryptor.decrypt(chunk).decode("utf-8")

                    # Remove the spaces at the end of the string
                    decryptedString = decryptedString.rstrip()

                    outfile.write(decryptedString.encode())
