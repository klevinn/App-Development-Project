#Done By Calvin

import shelve
from datetime import datetime

# using Luhn's Algorithms 
"""
Outline of Luhn's Algo:
Start from Last Digit:
x2 Odd Digits:
If resulting number of the x2 is a double digit, add both digits together
Then add all the final digits together
If divisible by 10, it is valid
"""


def IntegerList(credit_card_number):
    try:
        x = [int(a) for a in str(credit_card_number)]
        return x
    except:
        x = ""
        return x


def validate_card_number(credit_card_number):
    card_num_digits = IntegerList(credit_card_number)
    if card_num_digits=="":
        print("Blank Card")
        return True
    else:
        if len(str(credit_card_number)) == 16:
        #Start from the most right and move in 2s
            odd_digits = card_num_digits[-1::-2]
            print(odd_digits)

            #Start from second most right digit and move in 2s
            even_digits = card_num_digits[-2::-2]
            print(even_digits)

            odd_digits_sum = 0
            odd_digits_sum = sum(odd_digits)
            print(odd_digits_sum)
            even_digits_sum = 0

            for digit in even_digits:
                digit = digit * 2
                if digit >= 10:
                    digitList = IntegerList(digit)
                    digitSum = sum(digitList)
                    even_digits_sum += digitSum
                else:
                    even_digits_sum += digit
            
            print(even_digits_sum)
            total_sum = even_digits_sum + odd_digits_sum
            valid_card = total_sum % 10
            if valid_card == 0:
                return True
            else:
                return False
        
        else:
            return False

def validate_expiry_date(expiry_year, expiry_month):
    try:
        currentMonth = datetime.now().month
        print(currentMonth)
        print(expiry_month)
        currentYear = datetime.now().year   
        print(currentYear)
        print(expiry_year)
        if expiry_year >= currentYear:
            if expiry_month >= currentMonth:
                return True
            else:
                return False
        else:
            return False
    except:
        print("Left Blank")
        return True
"""
Testing Codes
print(IntegerList(12334))
validate_card_number(12395)
print(validate_card_number(12395))
"""

def Sanitise(stringInput):
    stringInput = stringInput.strip()
    return stringInput

#Validate Session

def validate_session(session , dictionary):
    user_found = False
    for key in dictionary:
        userid_in_shelve = dictionary[key].get_user_id()
        if session == userid_in_shelve:
            return True
        else:
            user_found = False
    
    return user_found

def validate_session_open_file_admin(session):
    staff_found = False
    users_dict = {}
    db = shelve.open("staff", "r")
    try:
        users_dict = db['Users']
        print("File found.")
    except:
        print("File could not be found.")
        return False
    
    db.close()

    for key in users_dict:
        staffname = users_dict[key].get_staff_id()
        emptyStr = ""
        print(staffname)
        print(session)
        if session == staffname:
            name = users_dict[key].get_username()
            return True , name
        else:
            staff_found = False
        
    return staff_found , emptyStr

def validate_session_admin(session,dictionary):
    staff_found = False
    emptyStr = ""
    for key in dictionary:
        staffname = dictionary[key].get_staff_id()
        if session == staffname:
            name = dictionary[key].get_username()
            return True , name
        else:
            staff_found = False
    return staff_found , emptyStr


'''
Cannot use previous password (WIP)
'''

