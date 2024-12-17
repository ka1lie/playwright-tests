from cryptography.fernet import Fernet
import getpass

credname = input("Enter name of your credential: ")
password = getpass.getpass("Enter your password: ")

key = open("./creds/key", "rb").read()

# Instance the Fernet class with the key

fernet = Fernet(key)

# then use the Fernet class instance 
# to encrypt the string string must
# be encoded to byte string before encryption
encPassword = fernet.encrypt(password.encode())

print("encrypted string: ", encPassword)

# write the encrypted password to secure locate files
f = open("./creds/" + str(credname), "wb")
f.write(encPassword)