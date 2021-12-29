#This Python File is to add Staff member if there is no staff accounts currently regsitered in
import shelve

import Staff

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

for key in userDict:
    emailinshelve = userDict[key].get_email()
    if emailInput == emailinshelve.lower():
        print("Registered email & inputted email:", emailinshelve, emailInput)
        duplicated_email = True
        print("Duplicate Email")
        break
    else:
        print("Registered email & inputted email:", emailinshelve, emailInput)
        email_duplicates = False
        print("New Email")

for key in userDict:
    usernameinshelve = userDict[key].get_username()
    if nameInput == usernameinshelve:
        print("Registered Username & inputted username:", usernameinshelve, nameInput)
        duplicated_username = True
        print("Duplicated Username")
        break
    else:
        print("Registered Username & inputted username:", usernameinshelve, nameInput)
        username_duplicates = False
        print("New Username")

if(duplicated_email == False) and (duplicated_username == False):
    print("Hello")
    user = Staff.Staff(nameInput, emailInput, 'Staff1234')
    for key in userDict:
        #To assign Staff ID, ensure that it is persistent and is accurate to the list
        staffidshelve = userDict[key].get_staff_id()
        if user.get_staff_id() == staffidshelve or user.get_staff_id() < staffidshelve:
            print(str(user.get_staff_id()), str(userDict[key].get_staff_id()))
            user.set_staff_id(user.get_staff_id() + 1)
            print(str(user.get_staff_id()) + "Hello1")
        else:
            print("Hello-olleH")
            
    userDict[user.get_staff_id()] = user
    db["Users"] = userDict
    db.close()