# USE THIS SCRIPT ONCE. IF YOU RUN IT AGAIN YOU SHOULD REGENERATE YOUR CREDENTIALS 

from cryptography.fernet import Fernet
import getpass

print("Please wait for key generation")

key = Fernet.generate_key()
f = open("./creds/key", "wb")
f.write(key)
#read = open("./creds/key", "r").read().replace("b", "")

#read.replace('b\'', '')
#print(read())
f.close


f = open("./creds/key", "r")
print(f.read())
print(key)
f.close
#f.replace('b\'', '')


