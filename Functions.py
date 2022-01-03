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

def get_user_name(idnumber, dictionary):
    for key in dictionary:
        if idnumber == key:
            UserName = dictionary[key].get_username()
            return UserName