from static_data.constants import *
from model_classes.security_info import SecurityInfo


class Utils:
    @staticmethod
    def read_file(file_path: str = PLAIN_TEXT_FILE_PATH) -> str:
        try:
            with open(file_path, "r") as file:
                contents = file.read()
                return contents
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return ""
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ""

    @staticmethod
    def read_security_info_file(security_info_file_path: str) -> SecurityInfo:
        securityInfoJson = Utils.read_file(
            file_path=security_info_file_path,
        )
        return SecurityInfo.from_json(securityInfoJson)

    @staticmethod
    def write_security_info_file(security_info: SecurityInfo):
        with open(SECURITY_INFO_FILE_PATH, "w") as file:
            file.write(security_info.to_json())
