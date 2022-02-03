#i dont think we need to make a guest account
#so idk what this is for

class Guest:
    def __init__(self, email):
        guest_id = 0
        guest_id += 1
        self.__guest_id = guest_id
        self.__email = email
        self.__name = ''
        self.__shipping_add = ''
        self.__unit_no1 = ''
        self.__unit_no2 = ''
        self.__postal_code = ''
        self.__phone_num = 0
        # self.__card_name = ''
        # self.__card_no = ''
        # self.__card_expiry_month = ''
        # self.__card_expiry_year = ''
        # self.__card_cvv = ''

    def set_email(self,email):
        self.__email = email
    #shipping details
    def set_name(self,name):
        self.__name = name
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

    # card details
    # def set_card_name(self, card_name):
    #     self.__card_name = card_name
    # def set_card_no(self, card_no):
    #     self.__card_no = card_no
    # def set_card_expiry_month(self, card_expiry_month):
    #     self.__card_expiry_month = card_expiry_month
    # def set_card_expiry_year(self, card_expiry_year):
    #     self.__card_expiry_year = card_expiry_year
    # def set_card_cvv(self, card_cvv):
    #     self.__card_cvv = card_cvv


    def get_guest_id(self):
        return self.__guest_id
    def get_email(self):
        return self.__email

    #shipping details
    def get_name(self):
        return self.__name
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

    #card details
    # def get_card_name(self):
    #     return self.__card_name
    # def get_card_no(self):
    #     return self.__card_no
    # def get_card_expiry_year(self):
    #     return self.__card_expiry_year
    # def get_card_expiry_month(self):
    #     return self.__card_expiry_month
    # def get_card_cvv(self):
    #     return self.__card_cvv
