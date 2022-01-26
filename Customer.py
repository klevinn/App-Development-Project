from User import User

#Made By XuZhi
class Customer(User):
    def __init__(self):
        super().__init__()
        self.__session_id = ''
        self.__date = ''
        self.__docter = ''

    def set_us(self, use):
        self.__session_id=use
    def get_us(self):
        return self.__session_id
    def set_date(self,date):
        self.__date=date
    def get_date(self):
        return self.__date
    def set_doc(self,doc):
        self.__docter=doc
    def get_doc(self):
        return self.__docter
    


