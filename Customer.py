from User import User

#Made By XuZhi
class Customer(User):
    def __init__(self):
        super().__init__()
        Customer.count_id += 1
        self.user = ''
        self.__customer =Customer.count_id
        self.__email = ''
        self.__date = ''
        self.__docter = ''

    def set_us(self, use):
        self.user=use
    def get_us(self):
        return self.user
    def set_customer_id(self, customer_id):
        self.__customer_id=customer_id
    def get_customer_id(self):
        return self.__customer
    def set_email(self, email):
        self.__email=email
    def get_email(self):
        return self.__email
    def set_date(self,date):
        self.__date=date
    def get_date(self):
        return self.__date
    def set_doc(self,doc):
        self.__docter=doc
    def get_doc(self):
        return self.__docter

