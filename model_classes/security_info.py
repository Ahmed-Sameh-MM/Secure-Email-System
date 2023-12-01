import json


class SecurityInfo:
    def __init__(self, hash_text: str, public_key: str, digital_signature: str):
        self.hashText = hash_text
        self.publicKey = public_key
        self.digitalSignature = digital_signature

    def to_json(self) -> str:
        securityInfoMap = vars(self)
        return json.dumps(securityInfoMap)

    @classmethod
    def from_json(cls, json_data: str):
        security_info = json.loads(json_data)
        return cls(
            security_info['hashText'],
            security_info['publicKey'],
            security_info['digitalSignature'],
        )
