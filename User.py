from Person import Person

class User(Person):
    def __init__(self, username, email, password):
        super().__init__(username, email, password)
        self.__card_name = ""
        self.__card_no = ""
        self.__card_expiry = ""
        self.__card_cvv = ""
        self.__shipping_address = ''
        self.__unit_number = ''
        self.__postal_code = ''
        self.__phone_number = 0

    def set_card_name(self, card_name):
        self.__card_name = card_name
    def set_card_no(self, card_no):
        self.__card_no = card_no
    def set_card_expiry(self, card_expiry):
        self.__card_expiry = card_expiry
    def set_card_cvv(self, card_cvv):
        self.__card_cvv = card_cvv
    def set_shipping_address(self, shipping_address):
        self.__shipping_address = shipping_address
    def set_unit_number(self, unit_number):
        self.__unit_number = unit_number
    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code
    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number


    def get_card_name(self):
        return self.__card_name
    def get_card_no(self):
        return self.__card_no
    def get_card_expiry(self):
        return self.__card_expiry
    def get_card_cvv(self):
        return self.__card_cvv
    def get_shipping_address(self):
        return self.__shipping_address
    def get_unit_number(self):
        return self.__unit_number
    def get_postal_code(self):
        return self.__postal_code
    def get_phone_number(self):
        return self.__phone_number

