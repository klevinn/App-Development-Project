from Person import Person
#Child Class
#Class Used for staff to store staff member ID 

class Staff(Person):
    staff_id = 0

    def __init__(self, username, email, password):
        super().__init__(username, email, 'Staff1234')
        Staff.staff_id += 1
        self.__staff_id = Staff.staff_id

    def set_staff_id(self, staff_id):
        self.__staff_id = staff_id
    
    def get_staff_id(self):
        return self.__staff_id