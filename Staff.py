from Person import Person

class Staff(Person):
    def __init__(self, username, email, password):
        super().__init__(username, email, password)