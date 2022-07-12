from cryptography.fernet import Fernet
import os

class Encrypt:
    def __init__(self) -> None:
        self.key = self._generate_key()        
        self.fernet = Fernet(self.key)
        
    def _generate_key(self):
        try:
            os.mkdir(os.path.join(os.getcwd(), "config_files"))
        except FileExistsError:
            print("Folder exists")
        finally:
            my_key_file = "config_files/key_file.txt"
            if os.path.exists(my_key_file):
                with open(my_key_file, 'rb') as myfile:
                    master_key = myfile.read()
            else:
                master_key = Fernet.generate_key()
                with open(my_key_file, 'wb') as myfile:
                    myfile.write(master_key)
            return master_key
    
    def encrypt(self, plain_text):
        encoded_str = plain_text.encode()
        return self.fernet.encrypt(encoded_str)
    
    def decrypt(self, encrypted_str):
        return self.fernet.decrypt(encrypted_str).decode()