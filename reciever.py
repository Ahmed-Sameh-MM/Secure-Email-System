import socket
import win32com.client
import ctypes  # for the VM_QUIT to stop PumpMessage()
import pythoncom
import time
import psutil
import os
import pathlib

from src.encryption import Encryption
from src.hash import Hash
from src.digital_signature import DigitalSignature
from utils.utils import Utils

from static_data.reciever_constants import *


class Handler_Class(object):
    def __init__(self):
        # First action to do when using the class in the DispatchWithEvents
        inbox = self.Application.GetNamespace("MAPI").GetDefaultFolder(6)
        messages = inbox.Items
        # Check for unread emails when starting the event
        for message in messages:
            if message.UnRead:
                print(message.Subject)  # Or whatever code you wish to execute.

    def OnQuit(self):
        # To stop PumpMessages() when Outlook Quit
        # Note: Not sure it works when disconnecting!!
        ctypes.windll.user32.PostQuitMessage(0)

    def OnNewMailEx(self, receivedItemsIDs):
        # RecrivedItemIDs is a collection of mail IDs separated by a ",".
        # You know, sometimes more than 1 mail is received at the same moment.
        global key
        if not os.path.exists(SAVE_ATTACHMENT_PATH):
            os.makedirs(SAVE_ATTACHMENT_PATH)

        for ID in receivedItemsIDs.split(","):
            print(f"ID ========== ${ID}")
            mail = self.Session.GetItemFromID(ID)

            print("Subject:", mail.Subject)
            # print("Sender:", mail.SenderName)
            # print("Received Time:", mail.ReceivedTime)
            # print("Body:", mail.Body)
            # print("id:", mail.EntryID)

            filesToDecrypt = []
            # Check for attachments
            if mail.Attachments.Count > 0:
                print("Attachments:")
                for attachment in mail.Attachments:
                    print(attachment.FileName)
                    # Save attachment to local storage
                    save_path = os.path.join(
                        pathlib.Path(__file__).parent.resolve(),
                        SAVE_ATTACHMENT_PATH,
                        attachment.FileName,
                    )
                    attachment.SaveAsFile(save_path)
                    print(f"Attachment saved to: {save_path}")
                    if attachment.FileName.endswith(".json"):
                        print("Getting security information")
                        security_info_path = save_path

                    elif attachment.FileName.endswith(".txt"):
                        filesToDecrypt.append(attachment.FileName)

                print("Decrypting file(s)")
                for i in range(len(filesToDecrypt)):
                    Encryption().decrypt_file(
                        key,
                        "attachments/" + filesToDecrypt[i],
                        "attachments/decrypted_text" + str(i) + ".txt",
                    )
                print("File(s) Decrypted Successfully")

                receiverSecurityInfo = Utils.read_security_info_file(security_info_path)

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


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 10000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    print("Received from server: " + client_socket.recv(1024).decode())

    # Loop
    while True:
        try:
            outlook_open = check_outlook_open()
        except:
            outlook_open = False
        # If outlook opened then it will start the DispatchWithEvents
        if outlook_open == True:
            resp = client_socket.recv(1024).decode()
            if resp == "EmailSent":
                outlook = win32com.client.DispatchWithEvents(
                    "Outlook.Application", Handler_Class
                )
                pythoncom.PumpMessages()
            # To not check all the time (should increase 10 depending on your needs)
            time.sleep(10)


# Function to check if outlook is open
def check_outlook_open():
    list_process = []
    for pid in psutil.pids():
        p = psutil.Process(pid)
        # Append to the list of process
        list_process.append(p.name())
    # If outlook open then return True
    if "OUTLOOK.EXE" in list_process:
        return True
    else:
        return False


# Loop
key = b"1234567812345678"

client_program()
