# USE THIS SCRIPT ONCE. IF YOU RUN IT AGAIN YOU SHOULD REGENERATE YOUR CREDENTIALS 

from cryptography.fernet import Fernet
import getpass

print("Please wait for key generation")

key = Fernet.generate_key()
f = open("./creds/key", "wb")
f.write(key)
f.close

