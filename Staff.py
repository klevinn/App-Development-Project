#Done By Calvin

from Person import Person
#Child Class
#Class Used for staff to store staff member ID 

class Staff(Person):


    def __init__(self):
        super().__init__()
        staff_id = 0
        staff_id += 1
        self.__expired = ''
        self.__staff_id = staff_id

    def set_staff_id(self, staff_id):
        self.__staff_id = staff_id
    
    def get_staff_id(self):
        return self.__staff_id
    
    def set_expired(self):
        self.__expired = True
    
    def set_unexpired(self):
        self.__expired = False
    
    def get_expired(self):
        return self.__expired