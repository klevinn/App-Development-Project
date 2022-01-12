from User import User

class Appoint(User):
    def __init__(self):
        super().__init__()
        self.__doctor = ''
        self.__date = ''
        self.__condition = ''
        self.__request = ''
        self.__booked = False

    def set_doctor(self, doctor):
        self.__doctor = doctor
    def set_date(self, date):
        self.__date = date
    def set_condition(self, condition):
        self.__condition = condition
    def set_request(self, request):
        self.__request = request
    
    def get_doctor(self):
        return self.__doctor
    def get_date(self):
        return self.__date
    def get_condition(self):
        return self.__condition
    def get_request(self):
        return self.__request
    
    def set_booked(self):
        self.__booked = True