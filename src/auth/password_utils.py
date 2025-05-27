import hashlib
import random 


generic_string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def hash_password(password):
    #hash password with sha256
    return hashlib.sha256(password.encode()).hexdigest()

def generate_password():
   password = ""
   for i in range(10):
       char = random.choice(generic_string)
       password = password + char
   
   return password

def generate_key():
    key = ""
    for i in range(20):
        char = random.choice(generic_string)
        key = key + char
    
    return "key" + key