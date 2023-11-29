from hashlib import sha256

from static_data.constants import *


class Hash:
    def __init__(self, plain_text: str = None):
        if plain_text is not None:
            self.plainText = plain_text

        else:
            self.plainText = self.__read_file()

        self.hashText = str()

        self.hash = sha256()

    @staticmethod
    def __read_file(file_path: str = PLAIN_TEXT_FILE_PATH) -> str:
        try:
            with open(file_path, 'r') as file:
                contents = file.read()
                return contents
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return ''
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ''

    def write_hash_text_to_file(self):
        self.__generate_hash_text()

        with open(HASH_FILE_PATH, 'w') as file:
            file.write(self.hashText)

    def __generate_hash_text(self):
        self.hash.update(self.plainText.encode())

        self.hashText = self.hash.hexdigest()
