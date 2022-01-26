#Done By Calvin

import random
#Default Class == Used for storing accounts inside the shelve

class Person:

    def __init__(self):
        self.__username = ''
        self.__email = ''
        self.__password = ''
        self.__first_name = ''
        self.__last_name = ''
        self.__gender = ''
        

    def set_username(self, username):
        self.__username = username
    def set_email(self, email):
        self.__email = email
    def set_password(self, password):
        self.__password = password
    #XuZhi
    def set_first_name(self, first_name):
        self.__first_name = first_name
    def set_last_name(self, last_name):
        self.__last_name = last_name
    def set_gender(self, gender):
        self.__gender = gender

    def get_username(self):
        return self.__username
    def get_email(self):
        return self.__email
    def get_password(self):
        return self.__password
    
    #XuZhi
    def get_first_name(self):
        return self.__first_name
    def get_last_name(self):
        return self.__last_name
    def get_gender(self):
        return self.__gender
 
 #Since hashed passwords are very long, generate a random number of stars as a string to display the password
    def get_censored_password(self):
        length = random.randint(6,10)
        s = "*" * length
        return s