#Done By Calvin

from Person import Person

#Child Class
#Used for storing user-relevant info into the shelve

class User(Person):

    def __init__(self, username, email, password):
        super().__init__(username, email, password)
        user_id = 0
        user_id += 1
        self.__user_id = user_id
        self.__card_name = ""
        self.__card_no = ""
        self.__card_cvv = ""
        self.__shipping_address = ''
        self.__unit_number1 = ''
        self.__unit_number2 = ''
        self.__postal_code = ''
        self.__card_expiry_month = ''
        self.__card_expiry_year = ''
        self.__phone_number = 0
        self.__previous_password = ''
        self.__ban_status = False
        self.__profile_picture = ''


    def set_card_name(self, card_name):
        self.__card_name = card_name
    def set_card_no(self, card_no):
        self.__card_no = card_no
    def set_card_expiry_month(self, card_expiry_month):
        self.__card_expiry_month = card_expiry_month
    def set_card_expiry_year(self, card_expiry_year):
        self.__card_expiry_year = card_expiry_year
    def set_card_cvv(self, card_cvv):
        self.__card_cvv = card_cvv
    def set_shipping_address(self, shipping_address):
        self.__shipping_address = shipping_address
    def set_unit_number1(self, unit_number1):
        self.__unit_number1 = unit_number1
    def set_unit_number2(self, unit_number2):
        self.__unit_number2 = unit_number2
    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code
    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number
    def set_user_id(self, user_id):
        self.__user_id = user_id
    #Prevent use of previous password
    def set_previous_password(self, prev_password):
        self.__previous_password = prev_password
    
    def get_account_status(self):
        return self.__account_status
    def get_user_id(self):
        return self.__user_id
    def get_card_name(self):
        return self.__card_name
    def get_card_no(self):
        return self.__card_no
    def get_card_expiry_year(self):
        return self.__card_expiry_year
    def get_card_expiry_month(self):
        return self.__card_expiry_month
    def get_card_cvv(self):
        return self.__card_cvv
    def get_shipping_address(self):
        return self.__shipping_address
    def get_unit_number1(self):
        return self.__unit_number1
    def get_unit_number2(self):
        return self.__unit_number2
    def get_postal_code(self):
        return self.__postal_code
    def get_phone_number(self):
        return self.__phone_number
    def get_previous_password(self):
        return self.__previous_password

    def set_profile_pic(self, profilepicture):
        self.__profile_picture = profilepicture
    def get_profile_pic(self):
        return self.__profile_picture

    def set_banned(self):
        self.__ban_status = True
    def set_unbanned(self):
        self.__ban_status = False
    def get_ban_status(self):
        return self.__ban_status

#Gets last 4 digits of card number and only displays that while censoring the rest
    def get_censored_credit_card(self):
        string_card = str(self.__card_no)
        s = string_card[-4:]
        length = len(string_card) - 4
        z = "*" * length
        card = z + s
        return card

    
    def display_unit_number(self):
        unit_number = ("# %s - %s" %(self.__unit_number1 , self.__unit_number2))
        return unit_number  
    def display_expiry_date(self):
        expiry_date = ('%s-%s' %(self.__card_expiry_year, self.__card_expiry_month))
        return expiry_date