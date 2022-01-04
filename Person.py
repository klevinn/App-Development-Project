import random
#Default Class == Used for storing accounts inside the shelve

class Person:

    def __init__(self, username, email, password):
        self.__username = username
        self.__email = email
        self.__password = password
        

    def set_username(self, username):
        self.__username = username
    def set_email(self, email):
        self.__email = email
    def set_password(self, password):
        self.__password = password

    def get_username(self):
        return self.__username
    def get_email(self):
        return self.__email
    def get_password(self):
        return self.__password
 
 #Since hashed passwords are very long, generate a random number of stars as a string to display the password
    def get_censored_password(self):
        length = random.randint(6,10)
        s = "*" * length
        return s