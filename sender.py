import socket, threading
import win32com.client as client
import os
import pythoncom

# from encryption import encrypt_file
from src.encryption import Encryption
from src.hash import Hash
from src.digital_signature import DigitalSignature
from model_classes.security_info import SecurityInfo
from utils.utils import Utils

from static_data.sender_constants import *


def send_email(to, subject, body, attachment_paths=None):
    pythoncom.CoInitialize()
    outlook_app = client.Dispatch("Outlook.Application")
    mail_item = outlook_app.CreateItem(0)  # 0 represents olMailItem constant
    mail_item.To = to
    mail_item.Subject = subject
    mail_item.Body = body

    if attachment_paths:
        for attachment_path in attachment_paths:
            attachment = os.path.abspath(attachment_path)
            if os.path.exists(attachment):
                mail_item.Attachments.Add(attachment)
            else:
                print(f"Attachment file not found: {attachment_path}")

    mail_item.Send()


class ClientThread(threading.Thread):
    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csocket = clientsocket

        print("[+] New thread started for ", ip, ":", str(port))

    def run(self):
        global key

        print("Connection from : ", ip, ":", str(port))
        self.csocket.send("Welcome to the multi-thraeded server".encode())
        data = "dummydata"
        while len(data):
            to = input("To: ")
            subject = input("Subject: ")
            body = input("Body: ")
            attachments_paths = input("Attachments path: ")
            attachments_paths = attachments_paths.split(" ")

            hashText = Hash(plain_text_path=attachments_paths[0]).generate_hash_text()
            Encryption().encrypt_file(key, attachments_paths[0], CIPHER_TEXT_FILE_PATH)
            print("1")
            publicKey, digitalSignature = DigitalSignature().get_signature(
                attachments_paths[0]
            )
            print("2")
            senderSecurityInfo = SecurityInfo(
                hash_text=hashText,
                public_key=publicKey,
                digital_signature=digitalSignature,
            )
            print("3")
            Utils.write_security_info_file(
                security_info=senderSecurityInfo,
            )
            print("4")
            attachments_paths = []
            attachments_paths.append(CIPHER_TEXT_FILE_PATH)
            attachments_paths.append(SECURITY_INFO_FILE_PATH)

            attachments_paths = " ".join(attachments_paths)

            j = {
                "to": to,
                "subject": subject,
                "body": body,
                "attachments_paths": attachments_paths,
            }
            send_email(
                j["to"], j["subject"], j["body"], str(j["attachments_paths"]).split(" ")
            )

            self.csocket.send("EmailSent".encode())

            if data == "quit":
                self.csocket.send(str.encode("Ok, Bye Bye"))
                self.csocket.close()
                data = ""

        print("Client at ", self.ip, " disconnected...")


host = socket.gethostname()
port = 10000
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((host, port))
key = b"1234567812345678"

while True:
    tcpsock.listen(4)
    print("Listening for incoming connections...")
    (clientsock, (ip, port)) = tcpsock.accept()
    # pass clientsock to the ClientThread thread object being created
    newthread = ClientThread(ip, port, clientsock)
    newthread.start()
