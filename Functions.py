def duplicate_username(username, dictionary):
    for key in dictionary:
        usernameinshelve = dictionary[key].get_username()
        if username == usernameinshelve:
            print("Registered Username & inputted username:", usernameinshelve, username)
            print("Duplicated Username")
            return True
        
        else:
            print("Registered Username & inputted username:", usernameinshelve, username)
            print("New Username")
    
    return False

def duplicate_email(email,dictionary):
    for key in dictionary:
        emailinshelve = dictionary[key].get_email()
        if email == emailinshelve.lower():
            print("Registered email & inputted email:", emailinshelve, email)
            print("Duplicate Email")
            return True
        else:
            print("Registered email & inputted email:", emailinshelve, email)
            print('New Email')
    
    return False

def check_banned(email,dictionary):
    for key in dictionary:
        emailinshelve = dictionary[key].get_email()
        if email == emailinshelve.lower():
            banned_status = dictionary[key].get_ban_status()
            if banned_status == True:
                return True
            else:
                return False


def get_user_name(idnumber, dictionary):
    for key in dictionary:
        if idnumber == key:
            UserName = dictionary[key].get_username()
            return UserName

def fix_unit_number(number):
    if number:
        if number < 10:
            number = str(number)
            number = ("0%s" %(number)) 
            return number
        else:
            number = str(number)
            return number
    else:
        return ''

'''
def break_unit_number(number):
    unit_number1 = number[2:4]
    unit_number2 = number[7:9]
    unit_number1 = int(unit_number1)
    unit_number2 = int(unit_number2)
    return unit_number1, unit_number2
''' 

"""
unit_number1, unit_number2 = break_unit_number("# 04 - 05")
print(unit_number1)
print(unit_number2)
"""