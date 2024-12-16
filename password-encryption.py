from cryptography.fernet import Fernet
import getpass

# we will be encrypting the below string.

credname = input("Enter name of your credential: ")
password = getpass.getpass("Enter your password: ")

# generate a key for encryption and decryption
# You can use fernet to generate 
# the key or use random key generator
# here I'm using fernet to generate key

#key = Fernet.generate_key()

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

# decrypt the encrypted string with the 
# Fernet instance of the key,
# that was used for encrypting the string
# encoded byte string is returned by decrypt method,
# so decode it to string with decode methods

# decPassword = fernet.decrypt(encPassword).decode()
# print("decrypted string: ", decPassword)