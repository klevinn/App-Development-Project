#imported modules
from flask import Flask, render_template, request, redirect, url_for, session
import shelve
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

#imported files
import Forms
import User, Staff

#Functions that are repeated

app = Flask(__name__)

#Secret Key Required for sessions
app.secret_key = "session_key"
#Limiter for login security
limiter = Limiter(app, key_func=get_remote_address)

@app.route('/' , methods=["GET","POST"])
def home():
    return render_template('home.html')


"""Account Management -- (login, signup, etc) By Calvin"""

@app.route('/login' , methods=["GET","POST"])
@limiter.limit("2/second")
def login():
    if "user" not in session or "staff" not in session:
        login_form = Forms.CreateLoginForm(request.form)
        if request.method == 'POST' and login_form.validate():
            #.lower() for email because capitalisation is not important in emails.
            emailInput = login_form.email.data.lower()
            passwordInput = login_form.password.data
            userDict = {}
            db = shelve.open("user", "c")
            #Using Flagname = "C" because if DB doesn't exist a file will be created instead of showing an error

            try:
                if 'Users' in db:
                    userDict = db['Users']
                else:
                    db["Users"] = userDict
            except:
                print("Error in retrieving Users from user.db.")

            #Preset Variables for later codes
            #Prevents UnboundLocalError

            validemail = False #Set to True if email is in shelve
            validpassword = False #Set to True if password is matching to the one in the shelf
            validstaffemail = False #Set to True if email inputted is in the staff database
            #These will store the data that is taken out from the shelve, used for comparison with input
            passwordinshelve = ""
            emailinshelve = ""

            for key in userDict:
                #getting email stored in the shelve
                emailinshelve = userDict[key].get_email()
                #comparing the data and seeing if matched
                if emailInput == emailinshelve.lower():
                    email_key = userDict[key]
                    validemail = True #As previously mentioned, set to true if found in shelve
                    #Console Checking
                    print("Registered Email & Inputted Email: ", emailinshelve, emailInput)
                    break
                
                    #For Console
                    #Tries looking through the Staff Database to see if email inputted is inside
            if validemail == True:
                passwordinshelve = email_key.get_password()
                if passwordInput == passwordinshelve:
                    validpassword = True
                    #Console Checking
                    print("Registered Password & Inputted Password: ", passwordinshelve, passwordInput)

            db.close()

            print("Now Trying Staff Email")
            #Flagname = "c" to create if not present == Prevents any error
            staffdb = shelve.open("staff" , "c")
            try:
                if 'Users' in staffdb:
                        userDict = staffdb['Users']
                else:
                    staffdb["Users"] = userDict
            except:
                print("Error in retrieving Users from staff.db.")

            for key in userDict:
                print("Staff Email Retrieved")
                emailinshelve = userDict[key].get_email()
                if emailInput == emailinshelve.lower():
                    staff_email_key = userDict[key]
                    validstaffemail = True
                    print("STAFF -- Registered Email & Inputted Email: ", emailinshelve, emailInput)
                    staffdb.close()
                    break
                else:
                    print("Invalid Staff Email.")
                    
                
            
            
            if validstaffemail == True:
                print("Hello-New")
                passwordinshelve = staff_email_key.get_password()
                if passwordInput == passwordinshelve:
                    staffdb.close()

                    staffname = staff_email_key.get_username()
                    session["staff"] = staffname

                    return redirect(url_for("staffapp" , staff = staffname))
                        
            if validemail == True and validpassword == True:
                print("Successful Login")

                userid = email_key.get_user_id()
                session["user"] = userid

                return redirect(url_for("user"))

            else:
                db.close()
                return render_template('user/guest/login.html', form=login_form, failedAttempt=True)

        else:
            return render_template('user/guest/login.html' , form=login_form)
    else:
        return redirect(url_for("home"))

@app.route('/logout')
def logout():
    session.pop("user", None)
    session.pop("staff", None)
    return redirect(url_for("home"))

@app.route('/signup' , methods=["GET","POST"])
def signup():
    if "user" not in session:
        signup_form = Forms.CreateSignUpForm(request.form)
        if request.method == 'POST' and signup_form.validate():
            print("Successful Running")
            #For duplicates
            #Pre determining Variables
            duplicated_email = False #Set to true if another email is already registered in the shelve
            duplicated_username = False #Set to true if another username is already registered in the shelve
            password_confirm = signup_form.password_confirm.data
            passwordInput = signup_form.password.data
            emailInput = signup_form.email.data.lower()
            usernameInput = signup_form.username.data
            
            #To determine if passwords are matched or not
            if password_confirm == passwordInput:
                    matched_pw = False
                    #Console
                    print("Matched Passwords")
            else:
                matched_pw = True
                #Console
                print("Password not matched")

            userDict = {}
            db = shelve.open("user", "c")

            try:
                if 'Users' in db:
                    userDict = db['Users']
                else:
                    db["Users"] = userDict
            except:
                print("Error in retrieving Users from user.db")
            
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
                    if usernameInput == usernameinshelve:
                        print("Registered Username & inputted username:", usernameinshelve, usernameInput)
                        duplicated_username = True
                        print("Duplicated Username")
                        break
                    else:
                        print("Registered Username & inputted username:", usernameinshelve, usernameInput)
                        username_duplicates = False
                        print("New Username")
            
            if (matched_pw == False) and (duplicated_email == False) and (duplicated_username == False):
                print("Hello")
                user = User.User(usernameInput, emailInput, passwordInput)
                print(user.get_user_id())
                for key in userDict:
                    useridshelve = userDict[key].get_user_id()
                    print("Running")
                    if user.get_user_id() != useridshelve and user.get_user_id() < useridshelve:
                        user.set_user_id(user.get_user_id())
                    if user.get_user_id() == useridshelve or user.get_user_id() < useridshelve:
                        print(str(user.get_user_id()), str(userDict[key].get_user_id()))
                        user.set_user_id(user.get_user_id() + 1)
                        print(str(user.get_user_id()) + "Hello1")

                print(user.get_user_id())
                userDict[user.get_user_id()] = user
                db["Users"] = userDict
                db.close()

                session["Customer"] = emailInput
                session["user"] = user.get_user_id()

                return redirect(url_for("signup2"))
            else:
                print("Hello2")
                db.close()
                return render_template('user/guest/signup.html', form=signup_form, duplicated_email=duplicated_email, duplicated_username=duplicated_username, matched_pw=matched_pw) 
        else:
            print("Hello3")
            return render_template('user/guest/signup.html',  form=signup_form)
    else:
        return redirect(url_for("home"))


@app.route('/signup2' , methods=["GET","POST"])
def signup2():
    if "user" in session:
        if "Customer" in session:
            CustEmail = session["Customer"]
            print(CustEmail)

            payment_form = Forms.CreateAddPaymentForm(request.form)
            if request.method == 'POST':
                print("Running")
                CustFound = False

                card_name = payment_form.card_name.data.upper()
                print(card_name)
                card_num = payment_form.card_no.data
                print(card_num)
                card_expiry = payment_form.card_expiry.data
                print(card_expiry)
                card_cvv = payment_form.card_CVV.data
                print(card_cvv)
            

                users_dict = {}
                db = shelve.open("user", "c")
                try:
                    if 'Users' in db:
                        users_dict = db['Users']
                    else:
                        session.clear()
                        return redirect(url_for("home"))
                except:
                    print("Error in retrieving Users from user.db")
                
                for key in users_dict:
                    print("retrieving")
                    emailinshelve = users_dict[key].get_email()
                    if CustEmail == emailinshelve:
                        customerkey = users_dict[key]
                        CustFound = True
                        break

                if CustFound == False:
                    session.clear()
                    return redirect(url_for("home"))

                customerkey.set_card_name(card_name)
                customerkey.set_card_no(card_num)
                customerkey.set_card_expiry(card_expiry)
                customerkey.set_card_cvv(card_cvv)

                db['Users'] = users_dict
                print("Payment added")


                db.close()
                return redirect(url_for("signup3"))
            else:
                print("Error")
                return render_template('user/guest/signup2.html', form=payment_form)
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


@app.route('/signup3' , methods=["GET","POST"])
def signup3():
    if "user" in session:
        if "Customer" in session:
            CustEmail = session["Customer"]
            print(CustEmail)

            shipping_form = Forms.CreateAddShippingAddressForm(request.form)
            if request.method == 'POST':
                print("Running")
                CustFound = False

                shipping_address = shipping_form.shipping_address.data.upper()
                print(shipping_address)
                postal_code = shipping_form.postal_code.data
                print(postal_code)
                unit_number = shipping_form.unit_number.data
                print(unit_number)
                phone_no = shipping_form.phone_no.data
                print(phone_no)


                users_dict = {}
                db = shelve.open("user", "c")
                try:
                    if 'Users' in db:
                        users_dict = db['Users']
                    else:
                        session.clear()
                        return redirect(url_for("home"))
                except:
                    print("Error in retrieving Users from user.db")
                
                for key in users_dict:
                    print("retrieving")
                    emailinshelve = users_dict[key].get_email()
                    if CustEmail == emailinshelve:
                        customerkey = users_dict[key]
                        CustFound = True
                        break

                if CustFound == False:
                    session.clear()
                    return redirect(url_for("home"))

                customerkey.set_shipping_address(shipping_address)
                customerkey.set_unit_number(unit_number)
                customerkey.set_postal_code(postal_code)
                customerkey.set_phone_number(phone_no)

                db['Users'] = users_dict
                print("Address added")


                db.close()
                session.pop("Customer" , None)
                return redirect(url_for("signupC"))
            else:
                return render_template('user/guest/signup3.html' , form = shipping_form)
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))
    

@app.route('/signupC' , methods=["GET","POST"])
def signupC():
    return render_template('user/guest/signupcomplete.html')

@app.route('/user' , methods=["GET","POST"])
def user():
    if "user" in session:
        userid = session["user"]
        users_dict ={}
        db = shelve.open('user', 'c')

        try:
            if 'Users' in db:
                users_dict = db['Users']
            else:
                db["Users"] = users_dict
        except:
            print("Error in retrieving User from staff.db")

        

        db.close()


        user_list = []
        for key in users_dict:
            if key == userid:
                user = users_dict.get(key)
                user_list.append(user)
                name = user.get_username()
                break
        

        return render_template('user/loggedin/useraccount.html' , user = name, count=len(user_list), user_list=user_list)
    else:
        return redirect(url_for("login"))

@app.route('/infoedit' , methods=["GET","POST"])
def userinfo():
    if "user" in session:
        idNumber = session["user"]
        users_dict ={}
        db = shelve.open('user', 'c')

        try:
            if 'Users' in db:
                users_dict = db['Users']
            else:
                db["Users"] = users_dict
        except:
            print("Error in retrieving User from staff.db")
        
        for key in users_dict:
            if idNumber == key:
                UserName = users_dict[key].get_username()
        
        db.close()

        update_user = Forms.CreateUserInfoForm(request.form)
        if request.method == "POST" and update_user.validate():
            print("Successful Running")
            existing_email = False
            existing_username = False
            nameInput = update_user.new_username.data
            emailInput = update_user.new_email.data.lower()
            users_dict ={}
            db = shelve.open('user', 'c')

            try:
                if 'Users' in db:
                    users_dict = db['Users']
                else:
                    db["Users"] = users_dict
            except:
                print("Error in retrieving User from user.db")

            
            
            for key in users_dict:
                if key != idNumber:
                    emailinshelve = users_dict[key].get_email()
                    if emailInput == emailinshelve.lower():
                        print("Registered email & inputted email:", emailinshelve, emailInput)
                        existing_email = True
                        print("Duplicate Email")
                        break
                    else:
                        print("Registered email & inputted email:", emailinshelve, emailInput)
                        existing_email = False
                        print("New Email")
            
            for key in users_dict:
                if key != idNumber:
                    usernameinshelve = users_dict[key].get_username()
                    if nameInput == usernameinshelve:
                        print("Registered Username & inputted username:", usernameinshelve, nameInput)
                        existing_username = True
                        print("Duplicated Username")
                        break
                    else:
                        print("Registered Username & inputted username:", usernameinshelve, nameInput)
                        existing_username = False
                        print("New Username")

            if(existing_email == False) and (existing_username == False):
                for key in users_dict:
                    if key == idNumber:
                        user = users_dict[key]
                        user.set_username(nameInput)
                        user.set_email(emailInput)
                        db["Users"] = users_dict

                        """
                        session["user"] = idNumber
                        idNumber = session["user"]
                        """

                db.close()
                return redirect(url_for("user"))

            else:
                print("Hello2")
                db.close()
                return render_template('user/loggedin/user_info_edit.html', form=update_user, duplicated_email=existing_email, duplicated_username=existing_username, user = UserName) 
        else:
            users_dict = {}
            db = shelve.open('user', 'r')
            try:
                if 'Users' in db:
                    users_dict = db['Users']
                else:
                    db["Users"] = users_dict
            except:
                print("Error in retrieving Users from user.db")
            db.close()

            user = users_dict.get(idNumber)
            update_user.new_username.data = user.get_username()
            update_user.new_email.data = user.get_email()
            return render_template('user/loggedin/user_info_edit.html', form=update_user, user = UserName) 
    else:
        return redirect(url_for("login"))

@app.route('/pwedit' , methods=["GET","POST"])
def userpw():
    if "user" in session:
        idNumber = session["user"]
        users_dict ={}
        db = shelve.open('user', 'c')

        try:
            if 'Users' in db:
                users_dict = db['Users']
            else:
                db["Users"] = users_dict
        except:
            print("Error in retrieving User from staff.db")
        
        for key in users_dict:
            if idNumber == key:
                UserName = users_dict[key].get_username()
        
        db.close()

        update_password = Forms.CreateNewPasswordForm(request.form)
        if request.method == "POST":
            print("Successful Running")
            matched_pw = True
            old_password = update_password.old_password.data 
            password = update_password.password.data
            password_cfm = update_password.password_confirm.data

            if password == password_cfm:
                matched_pw = False
            else:
                matched_pw = True


            users_dict ={}
            db = shelve.open('user', 'c')

            try:
                if 'Users' in db:
                    users_dict = db['Users']
                else:
                    db["Users"] = users_dict
            except:
                print("Error in retrieving User from user.db")

            user = users_dict.get(idNumber)
            #using accessor methods to update data
            registered_password = user.get_password()

            if old_password == registered_password:
                same_pw = False
            else:
                same_pw = True

            if (matched_pw == False) and (same_pw == False):
                user.set_password(password)
                db['Users'] = users_dict
                db.close()
                return redirect(url_for("user"))
            
            else:
                db.close()
                return render_template('user/loggedin/user_password_edit.html', form=update_password, matched_pw=matched_pw, same_pw = same_pw) 


        else:

            return render_template('user/loggedin/user_password_edit.html', form=update_password, user = UserName)
    else:
        return redirect(url_for("login"))

@app.route('/useraddress' , methods=["GET","POST"])
def useraddress():
    if "user" in session:
        idNumber = session["user"]
        users_dict ={}
        db = shelve.open('user', 'c')

        try:
            if 'Users' in db:
                users_dict = db['Users']
            else:
                db["Users"] = users_dict
        except:
            print("Error in retrieving User from staff.db")
        
        for key in users_dict:
            if idNumber == key:
                UserName = users_dict[key].get_username()
        
        db.close()

        update_address = Forms.CreateAddShippingAddressForm(request.form)
        if request.method == "POST":
            print("Successful Running")
            address = update_address.shipping_address.data.upper()
            postal_code = update_address.postal_code.data
            unit_number = update_address.unit_number.data
            phone_no = update_address.phone_no.data

            users_dict ={}
            db = shelve.open('user', 'c')

            try:
                if 'Users' in db:
                    users_dict = db['Users']
                else:
                    db["Users"] = users_dict
            except:
                print("Error in retrieving User from user.db")

            user = users_dict.get(idNumber)
            #using accessor methods to update data
            user.set_shipping_address(address)
            user.set_postal_code(postal_code)
            user.set_unit_number(unit_number)
            user.set_phone_number(phone_no)

            db['Users'] = users_dict
            db.close()

            return redirect(url_for("user"))
        
        else:
            users_dict = {}
            db = shelve.open('user', 'r')
            try:
                if 'Users' in db:
                    users_dict = db['Users']
                else:
                    db["Users"] = users_dict
            except:
                print("Error in retrieving Users from user.db")
            db.close()

            user = users_dict.get(idNumber)
            update_address.shipping_address.data = user.get_shipping_address()
            print(user.get_shipping_address())
            update_address.unit_number.data = user.get_unit_number()
            print(user.get_postal_code())
            update_address.postal_code.data = user.get_postal_code()
            print(user.get_unit_number())
            update_address.phone_no.data = user.get_phone_number()
            print(user.get_phone_number())
            return render_template('user/loggedin/user_address.html', form=update_address, user = UserName)
    
    else:
        return redirect(url_for('login'))

@app.route('/usercard' , methods=["GET","POST"])
def usercard():
    if "user" in session:
        idNumber = session["user"]
        users_dict ={}
        db = shelve.open('user', 'c')

        try:
            if 'Users' in db:
                users_dict = db['Users']
            else:
                db["Users"] = users_dict
        except:
            print("Error in retrieving User from staff.db")
        
        for key in users_dict:
            if idNumber == key:
                UserName = users_dict[key].get_username()
        
        db.close()

        update_card = Forms.CreateAddPaymentForm(request.form)
        if request.method == 'POST':
            print("Successful Running")
            card_name =  update_card.card_name.data.upper()
            card_no = update_card.card_no.data
            card_expiry = update_card.card_expiry.data
            card_cvv = update_card.card_CVV.data

            users_dict ={}
            db = shelve.open('user', 'c')

            try:
                if 'Users' in db:
                    users_dict = db['Users']
                else:
                    db["Users"] = users_dict
            except:
                print("Error in retrieving User from user.db")
            
            user = users_dict.get(idNumber)
            #using accessor methods to update data
            user.set_card_no(card_no)
            user.set_card_name(card_name)
            user.set_card_expiry(card_expiry)
            user.set_card_cvv(card_cvv)


            db['Users'] = users_dict
            db.close()

            return redirect(url_for("user"))
        else:
            users_dict = {}
            db = shelve.open('user', 'r')
            try:
                if 'Users' in db:
                    users_dict = db['Users']
                else:
                    db["Users"] = users_dict
            except:
                print("Error in retrieving Users from user.db")
            db.close()

            user = users_dict.get(idNumber)
            update_card.card_name.data = user.get_card_name()
            print(user.get_card_name())
            update_card.card_no.data = user.get_card_no()
            print(user.get_card_no())
            update_card.card_expiry.data = user.get_card_expiry()
            print(user.get_card_expiry())
            update_card.card_CVV.data = user.get_card_cvv()
            print(user.get_card_cvv())
            return render_template('user/loggedin/user_cardinfo.html', form=update_card, user = UserName)
    
    else:
        return redirect(url_for('login'))


    #return render_template('user/loggedin/user_cardinfo.html')

@app.route('/deletecard' , methods = ["GET", "POST"])
def deleteCard():
    if "user" in session:
        idNumber = session["user"]
        users_dict ={}
        db = shelve.open('user', 'c')

        try:
            if 'Users' in db:
                users_dict = db['Users']
            else:
                db["Users"] = users_dict
        except:
            print("Error in retrieving User from staff.db")
        
        for key in users_dict:
            if idNumber == key:
                UserName = users_dict[key].get_username()
        
        emptyString = ""
        user = users_dict.get(idNumber)
        user.set_card_no(emptyString)
        user.set_card_name(emptyString)
        user.set_card_expiry(emptyString)
        user.set_card_cvv(emptyString)

        db['Users'] = users_dict
        db.close()

        return redirect(url_for("user" , user = UserName))
    
    else:
        return redirect(url_for('login'))


@app.route('/deleteaddress' , methods=["GET" , "POST"])
def deleteAddress():
    if "user" in session:
        idNumber = session["user"]
        users_dict ={}
        db = shelve.open('user', 'c')

        try:
            if 'Users' in db:
                users_dict = db['Users']
            else:
                db["Users"] = users_dict
        except:
            print("Error in retrieving User from staff.db")
        
        for key in users_dict:
            if idNumber == key:
                UserName = users_dict[key].get_username()
        
        emptyString = ""
        user = users_dict.get(idNumber)
        user.set_shipping_address(emptyString)
        user.set_postal_code(emptyString)
        user.set_unit_number(emptyString)
        user.set_phone_number(emptyString)

        db['Users'] = users_dict
        db.close()

        return redirect(url_for("user" , user = UserName))
    
    else:
        return redirect(url_for("login"))

@app.route('/staffapp' , methods=["GET","POST"])
def staffapp():
    if "staff" in session:
        StaffName = session["staff"]
        return render_template('user/staff/staffappoint.html' , staff = StaffName)
    else:
        return redirect(url_for('login'))

@app.route('/stafffeed' , methods=["GET","POST"])
def stafffeed():
    if "staff" in session:
        StaffName = session["staff"]
        return render_template('user/staff/stafffeedback.html' , staff = StaffName)
    else:
        return redirect(url_for('login'))

@app.route('/staffinvent' , methods=["GET","POST"])
def staffinvent():
    if "staff" in session:
        StaffName = session["staff"]
        return render_template('user/staff/staffinventory.html' , staff = StaffName)
    else:
        return redirect(url_for('login'))

@app.route('/stafflist' , methods=["GET","POST"])
def stafflist():
    if "staff" in session:
        StaffName = session["staff"]
        staff_dict = {}
        db = shelve.open('staff', 'c')
        try:
            if 'Users' in db:
                staff_dict = db['Users']
            else:
                db["Users"] = staff_dict
        except:
            print("Error in retrieving User from staff.db")

        db.close()

        #Displaying the appending data into the stafflist so that it can be used to display data on the site
        staff_list = []
        for key in staff_dict:
            staff = staff_dict.get(key)
            staff_list.append(staff)


        return render_template('user/staff/stafflist.html', count=len(staff_list), staff_list=staff_list , staff = StaffName)
    else:
        return redirect(url_for('login'))

@app.route('/staffprod' , methods=["GET","POST"])
def staffprod():
    if "staff" in session:
        StaffName = session["staff"]
        return render_template('user/staff/staffproduct.html' , staff = StaffName)
    else:
        return redirect(url_for('login'))

@app.route('/staffupdate/<int:id>/', methods=['GET', 'POST'])
def staffupdate(id):
    if "staff" in session:
        StaffName = session["staff"]
        update_staff = Forms.CreateStaffMemberForm(request.form)
        if request.method == 'POST' and update_staff.validate():
            users_dict = {}
            db = shelve.open('staff', 'c')
            try:
                if 'Users' in db:
                    users_dict = db['Users']
                else:
                    db["Users"] = users_dict
            except:
                print("Error in retrieving Users from staff.db")

            #key is the id, so it will edit the data of the staff member and its corresponding key
            user = users_dict.get(id)
            #using accessor methods to update data
            user.set_username(update_staff.staff_name.data)
            user.set_email(update_staff.staff_email.data)

            db['Users'] = users_dict
            db.close()

            return redirect(url_for('stafflist'))

        else:
            users_dict = {}
            db = shelve.open('staff', 'r')
            try:
                if 'Users' in db:
                    users_dict = db['Users']
                else:
                    db["Users"] = users_dict
            except:
                print("Error in retrieving Users from staff.db")
            db.close()

            user = users_dict.get(id)
            update_staff.staff_name.data = user.get_username()
            update_staff.staff_email.data = user.get_email()

            return render_template('user/staff/staffupdate.html', form=update_staff, staff = StaffName)
    else:
        return redirect(url_for('login'))

@app.route('/staffadd' , methods=["GET","POST"])
def staffadd():
    if "staff" in session:
        StaffName = session["staff"]
        staff_form = Forms.CreateStaffMemberForm(request.form)
        if request.method == 'POST' and staff_form.validate():
            print("Successful Running")
            duplicated_email = False
            duplicated_username = False
            emailInput = staff_form.staff_email.data.lower()
            nameInput = staff_form.staff_name.data
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
                    print(staffidshelve , user.get_staff_id())

                    if user.get_staff_id() != staffidshelve and user.get_staff_id() < staffidshelve:
                        user.set_staff_id(user.get_staff_id())
                    else:
                        if user.get_staff_id() == staffidshelve or user.get_staff_id() < staffidshelve:
                            print(str(user.get_staff_id()), str(userDict[key].get_staff_id()))
                            user.set_staff_id(user.get_staff_id() + 1)
                            print(str(user.get_staff_id()) + "Hello1")

                        
                userDict[user.get_staff_id()] = user
                db["Users"] = userDict
                db.close()
                return redirect(url_for("stafflist"))
            else:
                print("Hello2")
                db.close()
                return render_template('user/staff/staffadd.html', form=staff_form, duplicated_email=duplicated_email, duplicated_username=duplicated_username, staff = StaffName) 
        else:
            print("Hello3")
            return render_template('user/staff/staffadd.html',  form=staff_form, staff = StaffName)
    else:
        return redirect(url_for('login'))


@app.route('/deleteUser/<int:id>', methods=["GET", 'POST'])
def deleteStaff(id):
    if "staff" in session:
        StaffName = session["staff"]
        users_dict = {}
        db = shelve.open('staff', 'w')
        try:
            if 'Users' in db:
                users_dict = db['Users']
            else:
                db["Users"] = users_dict
        except:
            print("Error in retrieving Users from staff.db")

        users_dict.pop(id)

        db['Users'] = users_dict
        db.close()

        return redirect(url_for('stafflist', staff = StaffName))
    else:
        return redirect(url_for('login'))


@app.route('/staffaccountlist' , methods=["GET","POST"])
def staffaccountlist():
    if "staff" in session:
        StaffName = session["staff"]
        return render_template('user/staff/staffaccountlist.html', staff = StaffName)
    else:
        return redirect(url_for('login'))

"""Custom Error Pages Made By Calvin"""

@app.errorhandler(401)
def error401(error):
    return render_template('errors/error401.html'), 401

@app.errorhandler(403)
def error403(error):
    return render_template('errors/error403.html'), 403

@app.errorhandler(404)
def error404(error):
    return render_template('errors/error404.html'), 404

@app.errorhandler(413)
def error413(error):
    return render_template('errors/error413.html'), 413

@app.errorhandler(429)
def error429(error):
    return render_template('errors/error429.html'), 429

@app.errorhandler(500)
def error500(error):
    return render_template('errors/error500.html'), 500

@app.errorhandler(501)
def error501(error):
    return render_template('errors/error501.html'), 501

@app.errorhandler(502)
def error502(error):
    return render_template('errors/error502.html'), 502

@app.errorhandler(503)
def error503(error):
    return render_template('errors/error503.html'), 503

if __name__ == '__main__':
    app.run(debug=True)
