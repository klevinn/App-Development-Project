#This Python File is to add Staff member if there is no staff accounts currently regsitered in
#Done By Calvin
import shelve
from flask_bcrypt import generate_password_hash

import Staff
from Functions import duplicate_email, duplicate_username, generate_staff_id

print("Welcome to Master Console For Admin Accounts")
emailInput = input("What is the Staff's Email: ")
nameInput = input("What is the Staff's Name: ")
duplicated_email = False
duplicated_username = False
userDict = {}
db = shelve.open("staff", "c")

try:
    if 'Users' in db:
        userDict = db['Users']
    else:
        db["Users"] = userDict
except:
    print("Error in retrieving Users from staff.db")

duplicated_email = duplicate_email(emailInput, userDict)
duplicated_username = duplicate_username(nameInput, userDict)


if(duplicated_email == False) and (duplicated_username == False):
    #staff_id = generate_staff_id()
    #print(staff_id)
    #pw_hash = generate_password_hash(staff_id)
    #print(pw_hash)
    #user = Staff.Staff(nameInput, emailInput, pw_hash)
    #user.set_staff_id(staff_id)


    print("Hello")
    user = Staff.Staff(nameInput, emailInput, 'Staff1234')
    for key in userDict:
        #To assign Staff ID, ensure that it is persistent and is accurate to the list
        staffidshelve = userDict[key].get_staff_id()
        if user.get_staff_id() != staffidshelve and user.get_staff_id() < staffidshelve:
            print(user.get_staff_id())
            user.set_staff_id(user.get_staff_id())
        else:
            if user.get_staff_id() == staffidshelve or user.get_staff_id() < staffidshelve:
                print(str(user.get_staff_id()), str(userDict[key].get_staff_id()))
                user.set_staff_id(user.get_staff_id() + 1)
                print(str(user.get_staff_id()) + "Hello1")
            
    userDict[user.get_staff_id()] = user
    db["Users"] = userDict
    db.close()