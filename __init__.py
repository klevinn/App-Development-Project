#imported modules
from flask import Flask, render_template, request, redirect, url_for, session, flash
import shelve
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_bcrypt import Bcrypt
from flask_mail import Mail , Message
from werkzeug.utils import secure_filename
import urllib.request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from src import Avatar

#imported files
import Forms
import User, Staff, Feedback
from Security_Validation import validate_card_number, Sanitise, validate_expiry_date, validate_session, validate_session_open_file_admin, validate_session_admin
from Functions import duplicate_email, duplicate_username, get_user_name, check_banned, fix_unit_number, fix_expiry_year, allowed_file, generate_random_password, generate_staff_id, generate_feedback_id
#Start Of Web Dev
app = Flask(__name__)
#Done by calvin
#Hashing of passwords
bcrypt = Bcrypt(app)

#For sending of emails
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'doctoronthego2022@gmail.com'
#Environment Variable set on my computer, because of pushing to Github this is for safety
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASS')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

#Secret Key Required for sessions
app.secret_key = "session_key"
s = Serializer(app.secret_key, expires_in=600)

#For Profile Picture Upload
PROFILEPIC_UPLOAD_PATH = 'static/images/profilepic'
app.config['UPLOAD_FOLDER'] = PROFILEPIC_UPLOAD_PATH
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


#Limiter for login security
limiter = Limiter(app, key_func=get_remote_address)

@app.route('/' , methods=["GET","POST"])
def home():
    if 'user' in session:
        idNumber = session["user"]
        print("%d entering page" %(idNumber))
        users_dict ={}
        db = shelve.open('user', 'c')

        try:
            if 'Users' in db:
                users_dict = db['Users']
            else:
                db["Users"] = users_dict
        except:
            print("Error in retrieving User from staff.db")
        
        UserName = get_user_name(idNumber, users_dict)
        valid_session = validate_session(idNumber, users_dict)

        db.close()
        if valid_session:
            print("%s is entering and his session is Valid" %(UserName))
            return render_template('user_home.html' , user = UserName)
        else:
            session.clear()
            print("Invalid Session")
            return render_template('home.html')

    elif 'staff' in session:
        StaffName = session["staff"]
        print("%s is entering the page" %(StaffName))
        valid_session, name = validate_session_open_file_admin(StaffName)
        if valid_session:
            print("%s is entering and his session is Valid" %(StaffName))
            return render_template('admin_home.html' , staff = name)
        else:
            session.clear()
            print("Invalid Session")
            return redirect(url_for('home'))
    else:
        print("Guest Entering Website")
        return render_template('home.html')

"""Account Management -- (login, signup, etc) By Calvin"""

""" LOGIN AND SIGNUP DONE BY CALVIN"""
@app.route('/login' , methods=["GET","POST"])
@limiter.limit("2/second")
def login():
    if "user" not in session or "staff" not in session:
        login_form = Forms.CreateLoginForm(request.form)
        if request.method == 'POST' and login_form.validate():
            #.lower() for email because capitalisation is not important in emails.
            emailInput = login_form.email.data.lower()
            passwordInput = login_form.password.data
            #print(emailInput, passwordInput)

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
            banned = False



            for key in userDict:
                #getting email stored in the shelve
                emailinshelve = userDict[key].get_email()
                ban_status = userDict[key].get_ban_status()
                #comparing the data and seeing if matched
                if emailInput == emailinshelve.lower():
                    email_key = userDict[key]
                    validemail = True #As previously mentioned, set to true if found in shelve
                    #Console Checking
                    print("Email Found: ", emailinshelve, emailInput)
                    if ban_status == True:
                        banned = True
                    break
                
                    #For Console
                    #Tries looking through the Staff Database to see if email inputted is inside
            if validemail == True:
                print("Email Found, Now trying Password")
                passwordinshelve = email_key.get_password()
                matching_pw = bcrypt.check_password_hash(passwordinshelve , passwordInput)
                if matching_pw == True:
                    print("Correct Password")
                    validpassword = True
                    #Console Checking

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
                    print("STAFF EMAIL FOUND--: ", emailinshelve, emailInput)
                    staffdb.close()
                    break
                else:
                    print("Invalid Staff Email.")
                    
                
            
            
            if validstaffemail == True:
                print("Running: Checking Staff Password")
                passwordinshelve = staff_email_key.get_password()
                #matching = bcrypt.check_password_hash(passwordinshelve, passwordInput)
                #if matching:
                if passwordInput == passwordinshelve:
                    print("Correct Password")
                    staffname = staff_email_key.get_staff_id()
                    session["staff"] = staffname
                    staffdb.close()
                    return redirect(url_for("staffapp" , staff = staffname))
                        
            if validemail == True and validpassword == True:
                if banned != True:
                    print("Successful Login")

                    userid = email_key.get_user_id()
                    session["user"] = userid

                    return redirect(url_for("user"))

                else:
                    print("Banned User tried to Log In")
                    return render_template('user/guest/login.html', form=login_form, bannedUser=True)

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
            emailInput = Sanitise(signup_form.email.data.lower())
            usernameInput = Sanitise(signup_form.username.data)
            
            #To determine if passwords are matched or not
            if password_confirm == passwordInput:
                    matched_pw = False
                    pw_hash = bcrypt.generate_password_hash(passwordInput)
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
            
            duplicated_email = duplicate_email(emailInput, userDict)
            duplicated_username = duplicate_username(usernameInput, userDict)
            check_ban = check_banned(emailInput, userDict)

            
            if (matched_pw == False) and (duplicated_email == False) and (duplicated_username == False) and (check_ban != True):
                print("Account Made!, Creating USER ID")
                user = User.User(usernameInput, emailInput, pw_hash)
                print(user.get_user_id())
                for key in userDict:
                    useridshelve = userDict[key].get_user_id()
                    print("Running")
                    if user.get_user_id() != useridshelve and user.get_user_id() < useridshelve:
                        user.set_user_id(user.get_user_id())
                    if user.get_user_id() == useridshelve or user.get_user_id() < useridshelve:
                        user.set_user_id(user.get_user_id() + 1)
                        #For Testing
                        #print(str(user.get_user_id()), str(userDict[key].get_user_id()))
                        #print(str(user.get_user_id()) + "Hello1")

                print(user.get_user_id(),  "was the next available user id.")
                userDict[user.get_user_id()] = user
                db["Users"] = userDict
                db.close()

                session["Customer"] = emailInput
                session["user"] = user.get_user_id()

                return redirect(url_for("signup2"))
            else:
                print("SignIn Failed: Error Encountered")
                db.close()
                return render_template('user/guest/signup.html', form=signup_form, duplicated_email=duplicated_email, duplicated_username=duplicated_username, matched_pw=matched_pw, check_ban = check_ban) 
        else:
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

                card_name = Sanitise(payment_form.card_name.data.upper())
                print(card_name)
                card_num = payment_form.card_no.data
                print(card_num)
                valid_card_num = validate_card_number(card_num)
                card_expiry_month = fix_unit_number(payment_form.card_expiry_month.data) 
                card_expiry_year = fix_expiry_year(payment_form.card_expiry_year.data)
                print(card_expiry_year)
                if card_expiry_year != False:
                    expiry_date = ('%s-%s-01' %(card_expiry_year, card_expiry_month))
                    print(expiry_date)
                    try:
                        card_expiry_year = int(card_expiry_year)
                    except:
                        card_expiry_year = card_expiry_year
                    valid_card_expiry = validate_expiry_date(card_expiry_year, payment_form.card_expiry_month.data)
                    card_cvv = payment_form.card_CVV.data
                    print(card_cvv)
                
                    if valid_card_num == True & valid_card_expiry == True:
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
                            print("Retrieving Emails")
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
                        customerkey.set_card_expiry_month(card_expiry_month)
                        customerkey.set_card_expiry_year(card_expiry_year)
                        customerkey.set_card_cvv(card_cvv)

                        db['Users'] = users_dict
                        print("Payment added")


                        db.close()
                        return redirect(url_for("signup3"))
                    else:
                        print("Invalid Card Number")
                        return render_template('user/guest/signup2.html' , form=payment_form, valid_card_num = valid_card_num, valid_card_expiry = valid_card_expiry)
                else:
                    print("Invalid Expiry Date")
                    return render_template('user/guest/signup2.html' , form=payment_form, valid_card_num = valid_card_num, card_expiry_year = card_expiry_year)
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

                shipping_address = ("BLK " + Sanitise(shipping_form.shipping_address.data.upper()))
                print(shipping_address)
                postal_code = ("(S)" + str(shipping_form.postal_code.data))
                print(postal_code)
                unit_number1 = fix_unit_number(shipping_form.unit_number1.data)
                unit_number2 = fix_unit_number(shipping_form.unit_number2.data)
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
                    print("Retrieving Emails")
                    emailinshelve = users_dict[key].get_email()
                    if CustEmail == emailinshelve:
                        customerkey = users_dict[key]
                        CustFound = True
                        break

                if CustFound == False:
                    session.clear()
                    return redirect(url_for("home"))

                customerkey.set_shipping_address(shipping_address)
                customerkey.set_unit_number1(unit_number1)
                customerkey.set_unit_number2(unit_number2)
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
        
        UserName =  get_user_name(idNumber, users_dict)
        
        valid_session = validate_session(idNumber, users_dict)

        db.close()

        if valid_session:
            session.pop('Customer',None)
            return render_template('user/guest/signupcomplete.html' , user = UserName)
        else:
            session.clear()
            return redirect(url_for('home'))
    
    else:
        return redirect(url_for("login"))

@app.route('/passwordforget', methods=["GET","POST"])
def passwordforget():
    email_form = Forms.CreateEmailForm(request.form)
    if request.method == "POST" and email_form.validate():
        email = Sanitise(email_form.email.data)
        #Temp reset password solution, send a temp password and let the users use and reset in their own free time
        #Safety issue if someone access their mail, uses the temp password , if they havent change, and login
        userDict = {}
        db = shelve.open("user", "c")

        try:
            if 'Users' in db:
                userDict = db['Users']
            else:
                db["Users"] = userDict
        except:
            print("Error in retrieving Users from user.db")
        
        validemail = False

        for key in userDict:
            #getting email stored in the shelve
            emailinshelve = userDict[key].get_email()
            ban_status = userDict[key].get_ban_status()
            #comparing the data and seeing if matched
            if email == emailinshelve.lower() and ban_status != True:
                email_key = userDict[key]
                validemail = True #As previously mentioned, set to true if found in shelve
                #Console Checking
                print("Registered Email & Inputted Email: ", emailinshelve, email)

        email_key.set_previous_password(email_key.get_password())

        temp_pw = generate_random_password()
        pw_hash =  bcrypt.generate_password_hash(temp_pw)
        
        if validemail == True:
            email_key.set_password(pw_hash)
            db['Users'] = userDict
            db.close()


            token = s.dumps(email_key.get_user_id())
            url = url_for('passwordreset', token=token)
            print(temp_pw, "is the temporary password sent")
            print(url, "is the temporary URL sent")
            pw_msg = "Dear user you have requested for a password request. Use this temporary password to log in and reset afterwards: %s \n OR \n Use this link to reset password instead: http://127.0.0.1:5000%s " %(temp_pw, url)
            msg = Message('Password Reset', sender = 'doctoronthego2022@gmail.com', recipients = [email])
            msg.body = pw_msg
            mail.send(msg)

            return render_template("user/guest/passwordforget.html", form = email_form, sent = True)
        else:
            #session["reset"] = email
            return render_template("user/guest/passwordforget.html", form = email_form, sent = True, validemail=validemail, ban_status = ban_status)
    else:
        return render_template("user/guest/passwordforget.html", form = email_form)

@app.route('/passwordreset/<token>', methods=["GET", "POST"])
def passwordreset(token):
    valid = False
    try:
        data = s.loads(token)
        print(data)
        valid = True
    except:
        valid = False

    userDict = {}
    db = shelve.open("user", "c")

    try:
        if 'Users' in db:
            userDict = db['Users']
        else:
            db["Users"] = userDict
    except:
        print("Error in retrieving Users from user.db")

    email = userDict[data].get_email()

    if valid == True:
        reset_password = Forms.CreateResetPWForm(request.form)
        if request.method =="POST" and reset_password.validate():
            reset_password.email.data = email
            newpw = reset_password.new_password.data
            print(newpw)
            newpwcfm = reset_password.confirm_password.data
            print(newpwcfm)
            oldpw = userDict[data].get_previous_password()
            reused = False
            reused = bcrypt.check_password_hash(oldpw, newpw)

            if newpwcfm == newpw:
                pwmatched = True
                hashed = bcrypt.generate_password_hash(newpw)
            else:
                pwmatched = False


            if reused == False and pwmatched == True:
                userDict[data].set_password(hashed)
                db['Users'] = userDict
                db.close()
                return render_template('user/guest/passwordreset.html', form=reset_password, sent = True)
            else:
                return render_template('user/guest/passwordreset.html', form=reset_password, sent = False, reused = reused , pwmatched = pwmatched)
        else:
            reset_password.email.data = email
            return render_template('user/guest/passwordreset.html', form=reset_password, sent = False)
    else:
        db.close()
        print("Token No Longer Valid")
        return redirect(url_for('home'))

"""
POTENTIAL PASSWORD RESET (Email sent and given link)

@app.route('/passwordreset', methods = ["GET","POST"])
def passwordreset():
    if "reset" in session:
        reset_password = Forms.CreateResetPWForm(request.form)
        if request.method =="POST" and reset_password.validate():
            checkEmail = session["reset"]
            banned = False
            validemail = False
            correct_email = ''
            password_confirm = reset_password.confirm_password.data
            passwordInput = reset_password.new_password.data
            emailInput = Sanitise(reset_password.email.data.lower())

            if checkEmail == emailInput:
                correct_email = True
            else:
                correct_email = False

                #To determine if passwords are matched or not
            if password_confirm == passwordInput:
                matched_pw = False
                pw_hash = bcrypt.generate_password_hash(passwordInput)
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
                #getting email stored in the shelve
                emailinshelve = userDict[key].get_email()
                ban_status = userDict[key].get_ban_status()
                #comparing the data and seeing if matched
                if emailInput == emailinshelve.lower():
                    email_key = userDict[key]
                    validemail = True #As previously mentioned, set to true if found in shelve
                    #Console Checking
                    print("Registered Email & Inputted Email: ", emailinshelve, emailInput)
                    if ban_status == True:
                        banned = True
                    break

            if (matched_pw == False) and (validemail == True) and (correct_email == True):
                if banned != True:
                        print("Reset Password")
                        email_key.set_password(pw_hash)
                        db['Users'] = userDict
                        db.close()
                        session.pop('reset')
                        return render_template("user/guest/passwordreset.html", form = reset_password , sent = True)
                else:
                    db.close()
                    return render_template('user/guest/passwordreset.html', form=reset_password, banned = banned, sent = False) 
            else:
                db.close()
                return render_template('user/guest/passwordreset.html', form=reset_password, matched_pw=matched_pw, banned = banned, validemail= False, sent = False, correct_email = correct_email) 

        else:
            return render_template("user/guest/passwordreset.html", form=reset_password, sent = False)
    else:
        return redirect(url_for('home'))
"""
"""
Email Verification
@app.route('/emailVerify/<token>', methods =["GET","POST"])
def emailVerify(token):
    return render_template("user/loggedin/emailverification.html")

"""
""" USER PROFILE SETTINGS DONE BY CALVIN"""

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

        
        valid_session = validate_session(userid, users_dict)

        db.close()

        changed = False
        change = ''

        if valid_session:
            user_list = []
            for key in users_dict:
                if key == userid:
                    user = users_dict.get(key)
                    user_list.append(user)
                    name = user.get_username()
                    break
            
            if 'change' in session:
                changed = True
                change = session['change']
                print(change)
                session.pop('change')
            
            av = Avatar(type="pixel-art-neutral", seed=name)

            return render_template('user/loggedin/useraccount.html' , user = name, count=len(user_list), user_list=user_list, changed = changed, change = change, av=av)
        else:
            session.clear()
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))

"""
#https://tutorial101.blogspot.com/2021/04/python-flask-upload-and-display-image.html
#https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
@app.route('/uploadProfilePic' , methods=["GET","POST"])
def uploadPic():
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

        UserName =  get_user_name(idNumber, users_dict)
        
        valid_session = validate_session(idNumber, users_dict)
        

        #db.close()
        if valid_session:
            if request.method == "POST":
                if "profilePic" not in request.files:
                    print("No File Sent")
                    return redirect(url_for("user"))
                
                file = request.files['profilePic']
                filename = file.filename

                #Find way to manage filesize

                if filename != '':
                    if file and allowed_file(filename):
                        filename = secure_filename(filename)
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                        #Need to make a unique identifier for each profile pic, UserId?
                        #need rename file -- either just rename /  split extension and add it to the new name
                        #Create a new file path with the new name

                        #how to display profile image?, use a getter method to get the path and display?
                        #meaning need to store in dict(getter n setter methods already created)

                        #overwrite == just by setting and getting?
                        #Too tired rn try tmr
                    else:
                        db.close()
                        print("Image not correct format")
                        return redirect(url_for('user'))
                else:
                    db.close()
                    print("No file inputted")
                    return redirect(url_for('user'))
                        
            else:
                db.close()
                return render_template('user/loggedin/useraccount.html', user = UserName)
        else:
            db.close()
            session.clear()
            return redirect(url_for("home"))
    else:
        return redirect(url_for('login'))
"""

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

        UserName =  get_user_name(idNumber, users_dict)
        
        valid_session = validate_session(idNumber, users_dict)
        

        db.close()

        if valid_session:
            update_user = Forms.CreateUserInfoForm(request.form)
            if request.method == "POST" and update_user.validate():
                print("Successful Running")
                existing_email = False
                existing_username = False
                nameInput = Sanitise(update_user.new_username.data)
                emailInput = Sanitise(update_user.new_email.data.lower())
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

                check_ban = check_banned(emailInput, users_dict)

                if(existing_email == False) and (existing_username == False) and (check_ban != True):
                    for key in users_dict:
                        if key == idNumber:
                            user = users_dict[key]
                            oldEmail = user.get_email()
                            user.set_username(nameInput)
                            user.set_email(emailInput)
                            db["Users"] = users_dict

                            email_msg = "Dear user, you have changed your email from %s to %s! If this was not you, contact our staff at 6251 2112 to help fix your issue! " %(oldEmail, emailInput)
                            msg = Message('Change In Email', sender = 'doctoronthego2022@gmail.com', recipients = [oldEmail])
                            msg.body = email_msg
                            mail.send(msg)

                            """
                            session["user"] = idNumber
                            idNumber = session["user"]
                            """
                    
                    session['change'] = 'Info'

                    db.close()
                    return redirect(url_for("user"))

                else:
                    print("Edit Failed = Error Occured")
                    db.close()
                    return render_template('user/loggedin/user_info_edit.html', form=update_user, duplicated_email=existing_email, duplicated_username=existing_username, user = UserName, check_ban = check_ban) 
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
            session.clear()
            return redirect(url_for("home"))
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
        
        UserName =  get_user_name(idNumber, users_dict)
        
        valid_session = validate_session(idNumber, users_dict)
        
        db.close()

        if valid_session:
            update_password = Forms.CreateNewPasswordForm(request.form)
            if request.method == "POST":
                print("Successful Running")
                matched_pw = True
                old_pw = False
                old_password = update_password.old_password.data 
                password = update_password.password.data
                password_cfm = update_password.password_confirm.data
                
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

                if old_password == password:
                    old_pw = True
                    matched_pw = False

                else:
                    if password == password_cfm:
                        matched_pw = False
                        hashed_pw = bcrypt.generate_password_hash(password)
                    else:
                        matched_pw = True


                #using accessor methods to update data
                registered_password = user.get_password()
                same_password_hash = bcrypt.check_password_hash(registered_password, old_password)
                email = user.get_email()

                if same_password_hash == True:
                    same_pw = False
                else:
                    same_pw = True

                if (matched_pw == False) and (same_pw == False) and (old_pw == False):
                    user.set_password(hashed_pw)
                    db['Users'] = users_dict
                    db.close()

                    pw_msg = "Dear user, you have changed your password! If this was not you, contact our staff at 6251 2112 to help fix your issue! "
                    msg = Message('Change In Password', sender = 'doctoronthego2022@gmail.com', recipients = [email])
                    msg.body = pw_msg
                    mail.send(msg)

                    session['change'] = 'Password'

                    return redirect(url_for("user"))
                
                else:
                    db.close()
                    return render_template('user/loggedin/user_password_edit.html', form=update_password, matched_pw=matched_pw, same_pw = same_pw, old_password = old_pw, user = UserName) 
            else:

                return render_template('user/loggedin/user_password_edit.html', form=update_password, user = UserName)
        else:
            session.clear()
            return redirect(url_for("home"))
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
        

        UserName =  get_user_name(idNumber, users_dict)
        valid_session = validate_session(idNumber, users_dict)
        
        db.close()
        if valid_session:
            update_address = Forms.CreateAddShippingAddressForm(request.form)
            if request.method == "POST":
                print("Successful Running")
                
                address = ("BLK " + Sanitise(update_address.shipping_address.data.upper()))
                postal_code = ("(S)" + str(update_address.postal_code.data))
                unit_number1 = fix_unit_number(update_address.unit_number1.data)
                unit_number2 = fix_unit_number(update_address.unit_number2.data)
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
                user.set_unit_number1(unit_number1)
                user.set_unit_number2(unit_number2)
                user.set_phone_number(phone_no)

                db['Users'] = users_dict
                db.close()

                session['change'] = 'Address'

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
                update_address.shipping_address.data = (user.get_shipping_address()[4:])
                print(user.get_shipping_address())
                unitnum1 = user.get_unit_number1()
                unitnum2 = user.get_unit_number2()
                print('hi',unitnum1, unitnum2)
                print(len(unitnum1), len(unitnum2))
                if len(unitnum1) == 0 or len(unitnum2) == 0:
                    update_address.unit_number1.data = unitnum1
                    update_address.unit_number2.data = unitnum2
                else:
                    update_address.unit_number1.data = int(unitnum1)
                    update_address.unit_number2.data = int(unitnum2)
                print(user.get_postal_code())
                shortened_postal = user.get_postal_code()[3:]
                print(shortened_postal)
                if len(shortened_postal) == 0 or shortened_postal == 'None':
                    update_address.postal_code.data =shortened_postal
                else:
                    update_address.postal_code.data = int(shortened_postal)

                update_address.phone_no.data = user.get_phone_number()
                print(user.get_phone_number())
                return render_template('user/loggedin/user_address.html', form=update_address, user = UserName)
        else:
            session.clear()
            return redirect(url_for("home"))
    
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
        
        UserName =  get_user_name(idNumber, users_dict)
        
        valid_session = validate_session(idNumber, users_dict)

        db.close()

        if valid_session:
            update_card = Forms.CreateAddPaymentForm(request.form)
            if request.method == 'POST':
                print("Running")
                CustFound = False

                card_name = Sanitise(update_card.card_name.data.upper())
                print(card_name)
                card_num = update_card.card_no.data
                print(card_num)
                valid_card_num = validate_card_number(card_num)
                card_expiry_month = fix_unit_number(update_card.card_expiry_month.data) 
                card_expiry_year = fix_expiry_year(update_card.card_expiry_year.data)
                print(card_expiry_year)
                if card_expiry_year != False:
                    expiry_date = ('%s-%s-01' %(card_expiry_year, card_expiry_month))
                    print(expiry_date)
                    try:
                        card_expiry_year = int(card_expiry_year)
                    except:
                        card_expiry_year = card_expiry_year
                    valid_card_expiry = validate_expiry_date(card_expiry_year, update_card.card_expiry_month.data)
                    card_cvv = update_card.card_CVV.data


                    if valid_card_num == True and valid_card_expiry == True:
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
                        user.set_card_no(card_num)
                        user.set_card_name(card_name)
                        user.set_card_expiry_month(card_expiry_month)
                        user.set_card_expiry_year(card_expiry_year)
                        user.set_card_cvv(card_cvv)


                        db['Users'] = users_dict
                        db.close()

                        session['change'] = 'Card'

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

                        #update_card.card_no.data = user.get_card_no()
                        #print(user.get_card_no())
                        try:
                            card_month = fix_unit_number(int(user.get_card_expiry_month()))
                            card_year = fix_expiry_year(int(user.get_card_expiry_year()))
                        except:
                            card_month = fix_unit_number(user.get_card_expiry_month())
                            card_year = fix_expiry_year(user.get_card_expiry_year())
                            
                        if len(card_month) == 0 or len(card_year) == 0:
                            update_card.card_expiry_year.data = card_year
                            update_card.card_expiry_month.data = card_month
                        else:
                            update_card.card_expiry_year.data = int(card_year)
                            update_card.card_expiry_month.data = int(card_month)

                        update_card.card_CVV.data = user.get_card_cvv()
                        print(user.get_card_cvv())
                        return render_template('user/loggedin/user_cardinfo.html', form=update_card, user = UserName, valid_card_num = valid_card_num, valid_card_expiry=valid_card_expiry)
                
                else:
                    print("Invalid Expiry Date")
                    return render_template('user/guest/signup2.html' , form=update_card, valid_card_num = valid_card_num, card_expiry_year = card_expiry_year)
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
                try:
                    card_month = fix_unit_number(int(user.get_card_expiry_month()))
                    card_year = fix_expiry_year(int(user.get_card_expiry_year()))
                except:
                    card_month = fix_unit_number(user.get_card_expiry_month())
                    card_year = fix_expiry_year(user.get_card_expiry_year())

                if len(card_month) == 0 or len(card_year) == 0:
                    update_card.card_expiry_year.data = card_year
                    update_card.card_expiry_month.data = card_month
                else:
                    update_card.card_expiry_year.data = int(card_year)
                    update_card.card_expiry_month.data = int(card_month)
                update_card.card_CVV.data = user.get_card_cvv()
                print(user.get_card_cvv())
                return render_template('user/loggedin/user_cardinfo.html', form=update_card, user = UserName)
        
        else:
            return redirect(url_for("home"))
    
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
        
        UserName =  get_user_name(idNumber, users_dict)

        valid_session = validate_session(idNumber, users_dict)

        if valid_session:
            emptyString = ""
            user = users_dict.get(idNumber)
            user.set_card_no(emptyString)
            user.set_card_name(emptyString)
            user.set_card_expiry_month(emptyString)
            user.set_card_expiry_year(emptyString)
            user.set_card_cvv(emptyString)

            db['Users'] = users_dict
            db.close()

            return redirect(url_for("user" , user = UserName))
        else:
            db.close()
            session.clear()
            return redirect(url_for("home"))
    
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
        
        UserName =  get_user_name(idNumber, users_dict)
        valid_session = validate_session(idNumber, users_dict)

        if valid_session:
            emptyString = ""
            user = users_dict.get(idNumber)
            user.set_shipping_address(emptyString)
            user.set_postal_code(emptyString)
            user.set_unit_number1(emptyString)
            user.set_unit_number2(emptyString)
            user.set_phone_number(emptyString)

            db['Users'] = users_dict
            db.close()

            return redirect(url_for("user" , user = UserName))

        else:
            db.close()
            session.clear()
            return redirect(url_for("home"))
    
    else:
        return redirect(url_for("login"))

"""ADMIN ACCOUNT SETTINGS DONE MY CALVIN"""

@app.route('/staffapp' , methods=["GET","POST"])
def staffapp():
    if "staff" in session:
        StaffName = session["staff"]
        valid_session, name = validate_session_open_file_admin(StaffName)

        userDict = {}
        db = shelve.open('user', 'c')
        try:
            if 'Users' in db:
                userDict = db['Users']
            else:
                db['Users']= userDict
        except:
            print("Error in retrieving Users from feedback db")
        
        db.close()
        
        if valid_session:
            # Take in form submissions and dislay the data to the list.
            # Upon submission the data will be stored into a list?, Recommend creating a .get() and .set() method for form inputs
            return render_template('user/staff/staffappoint.html' , staff = name)
        else:
            session.clear()
            return redirect(url_for("home"))
    else:
        return redirect(url_for('login'))

@app.route('/stafffeed/<int:page>' , methods=["GET","POST"])
def stafffeed(page=1):
    if "staff" in session:
        StaffName = session["staff"]
        valid_session, name = validate_session_open_file_admin(StaffName)

        feedback_dict = {}
        db = shelve.open('feedback', 'c')
        try:
            if 'Users' in db:
                feedback_dict = db['Users']
            else:
                db['Users'] = feedback_dict
        except:
            print("Error in retrieving Users from feedback db")
        
        db.close()

        if valid_session:
            """
            feedbackform = open("forsimulation.txt", 'a')
            feedbackform.write('Name, Type, Description, \n')
            feedbackform.close()

            Because of problems with delete feedback page, might need to change it to shelf and deal with dictionaries.

            Created feedback id function already
            """
            display_dict = {}
            page_num = 1
            feedback_list = []
            for key in feedback_dict:
                if len(feedback_list) == 5:
                    display_dict[page_num] = feedback_list
                    page_num += 1

                    feedback_list = []
                    feedback = feedback_dict.get(key)
                    feedback_list.append(feedback)
                    display_dict[page_num] = feedback_list
                else:
                    feedback = feedback_dict.get(key)
                    feedback_list.append(feedback)
                    display_dict[page_num] = feedback_list
            """
            feed = open("forsimulation.txt", 'r')
            line = feed.read()
            test = line.split(', \n')
            print(test)
            for i in test:
                if len(feedback_list) == 5:
                    display = i.split(", ")
                    feedback_list.append(display)
                    print(feedback_list)

                    display_dict[page_num] = feedback_list
                    page_num += 1

                    feedback_list = []
                    display = i.split(", ")
                    print(display, "HELLo")
                    #feedback_list.append(display)
                    display_dict[page_num] = feedback_list
                else:
                    display = i.split(", ")
                    feedback_list.append(display)
                    display_dict[page_num] = feedback_list
                    feed.close()
            """

            feedback_list = display_dict[page]
            all_keys = display_dict.keys()
            max_value = max(all_keys)

            
            return render_template('user/staff/stafffeedback.html' , count=len(feedback_list), feedback_list=feedback_list , staff = name, display_dict = display_dict, page=page, max_value=max_value)
        else:
            session.clear()
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/deleteFeedback/<int:id>', methods=['GET', "POST"])
#@app.route('/deleteFeedback/<str:id>', methods=['GET', "POST"])
def deleteFeedback(id):
    if "staff" in session:
        StaffName = session["staff"]
        valid_session, name = validate_session_open_file_admin(StaffName)
        
        feedback_dict = {}
        db = shelve.open('feedback', 'w')
        try:
            if 'Users' in db:
                feedback_dict = db['Users']
            else:
                db['Users'] = feedback_dict
        except:
            print("Error in retrieving Users from feedback db")

        if valid_session:
            feedback_dict.pop(id)

            db['Users'] = feedback_dict
            db.close()

            return redirect(url_for('stafffeed', page=1, staff = name))
        else:
            db.close()
            session.clear()
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/staffinvent' , methods=["GET","POST"])
def staffinvent():
    if "staff" in session:
        StaffName = session["staff"]
        valid_session, name = validate_session_open_file_admin(StaffName)
        if valid_session:
            #Depends on how Joshua displays the store inventory.
            # Can easily set up some variable system in jinja, and we modify the jinja through here.
            return render_template('user/staff/staffinventory.html' , staff = name)
        else:
            session.clear()
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/stafflist/<int:page>' , methods=["GET","POST"])
def stafflist(page=1):
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
        
        valid_session, name = validate_session_admin(StaffName, staff_dict)

        db.close()

        #Displaying the appending data into the stafflist so that it can be used to display data on the site
        if valid_session:
            display_dict = {}
            page_num = 1
        #Displaying the appending data into the stafflist so that it can be used to display data on the site
            staff_list = []
            for key in staff_dict:
                if len(staff_list) == 10:
                    display_dict[page_num] = staff_list
                    page_num += 1

                    staff_list = []
                    staff = staff_dict.get(key)
                    staff_list.append(staff)
                    display_dict[page_num] = staff_list
                else:
                    staff = staff_dict.get(key)
                    staff_list.append(staff)
                    display_dict[page_num] = staff_list
            
            staff_list = display_dict[page]
            all_keys = display_dict.keys()
            max_value = max(all_keys)

            staffpassword = ''
            if 'staffpw' in session:
                staffpassword = session['staffpw']
                session.pop('staffpw', None)
            
            return render_template('user/staff/stafflist.html', count=len(staff_list), staff_list=staff_list , staff = name, display_dict = display_dict, page=page, max_value=max_value, staffpassword = staffpassword)
        else:
            session.clear()
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/staffprod' , methods=["GET","POST"])
def staffprod():
    if "staff" in session:
        StaffName = session["staff"]
        valid_session, name = validate_session_open_file_admin(StaffName)
        if valid_session:
            #https://www.youtube.com/watch?v=E2hytuQvLlE&ab_channel=teclado
            #in cart, must set it so that the inventory minuses  and just take that code and append
            return render_template('user/staff/staffproduct.html' , staff = name)
        else:
            session.clear()
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

#@app.route('/staffupdate/<string:id>/', methods=['GET', 'POST'])
@app.route('/staffupdate/<int:id>/', methods=['GET', 'POST'])
def staffupdate(id):
    if "staff" in session:
        StaffName = session["staff"]
        valid_session, name = validate_session_open_file_admin(StaffName)
        
        if valid_session:
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
                user.set_username(Sanitise(update_staff.staff_name.data))
                user.set_email(Sanitise(update_staff.staff_email.data))

                db['Users'] = users_dict
                db.close()

                return redirect(url_for('stafflist', page =1))

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

                return render_template('user/staff/staffupdate.html', form=update_staff, staff = name)
        else:
            session.clear()
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/staffadd' , methods=["GET","POST"])
def staffadd():
    if "staff" in session:
        StaffName = session["staff"]
        valid_session , name = validate_session_open_file_admin(StaffName)

        if valid_session:
            staff_form = Forms.CreateStaffMemberForm(request.form)
            if request.method == 'POST' and staff_form.validate():
                print("Successful Running")
                duplicated_email = False
                duplicated_username = False
                emailInput = Sanitise(staff_form.staff_email.data.lower())
                nameInput = Sanitise(staff_form.staff_name.data)
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
                    print("Hello")
                   #staff_id = generate_staff_id()

                    """
                    for key in userDict:
                        staffidshelve = userDict[key].get_staff_id()
                        if staff_id == staffidshelve:
                            staff_id = generate_staff_id()
                    """
 
                    #pw_hash = bcrypt.generate_password_hash(staff_id)
                    #user = Staff.Staff(nameInput, emailInput, pw_hash)
                    #user.set_staff_id(staff_id)

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

                    admin_msg = "You have been added to the staff team! Welcome to the team! "
                    msg = Message('Welcome New Staff Member', sender = 'doctoronthego2022@gmail.com', recipients = [emailInput])
                    msg.body = admin_msg
                    mail.send(msg)

                    return redirect(url_for("stafflist", page = 1))
                else:
                    print("Hello2")
                    db.close()
                    return render_template('user/staff/staffadd.html', form=staff_form, duplicated_email=duplicated_email, duplicated_username=duplicated_username, staff = name) 
            else:
                print("Hello3")
                return render_template('user/staff/staffadd.html',  form=staff_form, staff = name)
        else:
            session.clear()
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

#@app.route('/deleteUser/<string:id>', methods=["GET", 'POST'])
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
        
        valid_session, name = validate_session_admin(StaffName, users_dict)
        staff_pass = ''
        staff_pass = request.form['password']
        print(staff_pass)
        if valid_session:
            if staff_pass == users_dict[id].get_password():
                users_dict.pop(id)

                db['Users'] = users_dict
                db.close()

                session['staffpw'] = True
                
                return redirect(url_for('stafflist', page=1, staff = name))
            else:
                db.close()

                session['staffpw'] = False

                return redirect(url_for('stafflist', page=1, staff = name))
        else:
            db.close()
            session.clear()
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route('/staffaccountlist/<int:page>' , methods=["GET","POST"])
def staffaccountlist(page=1):
    if "staff" in session:
        StaffName = session["staff"]
        user_dict = {}
        db = shelve.open('user', 'c')
        try:
            if 'Users' in db:
                user_dict = db['Users']
            else:
                db["Users"] = user_dict
        except:
            print("Error in retrieving User from user.db")

        valid_session , name = validate_session_open_file_admin(StaffName)

        db.close()

        if valid_session:
            display_dict = {}
            page_num = 1
        #Displaying the appending data into the stafflist so that it can be used to display data on the site
            user_list = []
            for key in user_dict:
                if len(user_list) == 5:
                    display_dict[page_num] = user_list
                    page_num += 1

                    user_list = []
                    user = user_dict.get(key)
                    user_list.append(user)
                    display_dict[page_num] = user_list
                else:
                    user = user_dict.get(key)
                    user_list.append(user)
                    display_dict[page_num] = user_list
            
            user_list = display_dict[page]
            all_keys = display_dict.keys()
            max_value = max(all_keys)

            return render_template('user/staff/staffaccountlist.html', count=len(user_list), user_list=user_list , display_dict = display_dict, staff = name,  page=page, max_value = max_value)
        else:
            session.clear()
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/banUser/<int:id>' , methods=["GET","POST"])
def banUser(id):
    if "staff" in session:
        StaffName = session["staff"]
        users_dict = {}
        db = shelve.open('user', 'c')
        try:
            if 'Users' in db:
                users_dict = db['Users']
            else:
                db["Users"] = users_dict
        except:
            print("Error in retrieving Users from user.db")
        
        valid_session , name = validate_session_open_file_admin(StaffName)

        if valid_session:
            users_dict[id].set_banned()
            user_email = users_dict[id].get_email()
            user_name = users_dict[id].get_username()

            ban_msg = "Dear %s! You have been banned from DoctorOnTheGo. Do contact one of our staff if you feel this was an unfair ban. Have a nice day!" %(user_name)
            msg = Message('Ban Alert', sender = 'doctoronthego2022@gmail.com', recipients = [user_email])
            msg.body = ban_msg
            mail.send(msg)

            db['Users'] = users_dict
            db.close()

            return redirect(url_for('staffaccountlist', page=1, staff = name))
        else:
            db.close()
            session.clear()
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/unbanUser/<int:id>' , methods=["GET","POST"])
def unbanUser(id):
    if "staff" in session:
        StaffName = session["staff"]
        users_dict = {}
        db = shelve.open('user', 'c')
        try:
            if 'Users' in db:
                users_dict = db['Users']
            else:
                db["Users"] = users_dict
        except:
            print("Error in retrieving Users from user.db")
        
        valid_session , name = validate_session_open_file_admin(StaffName)

        if valid_session:
            users_dict[id].set_unbanned()
            user_email = users_dict[id].get_email()
            user_name = users_dict[id].get_username()

            unban_msg = "Dear %s! You have been unbanned from DoctorOnTheGo. We apologise for the inconvenience. Have a nice day!" %(user_name)
            msg = Message('Unban Alert', sender = 'doctoronthego2022@gmail.com', recipients = [user_email])
            msg.body = unban_msg
            mail.send(msg)

            db['Users'] = users_dict
            db.close()

            return redirect(url_for('staffaccountlist', page=1, staff = name))
        else:
            db.close()
            session.clear()
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/resetPasswordUser/<int:id>', methods=["GET", "POST"])
def resetPassUser(id):
    if "staff" in session:
        StaffName = session["staff"]
        users_dict = {}
        db = shelve.open('user', 'c')
        try:
            if 'Users' in db:
                users_dict = db['Users']
            else:
                db["Users"] = users_dict
        except:
            print("Error in retrieving Users from user.db")
        
        valid_session , name = validate_session_open_file_admin(StaffName)
        temp_pw = generate_random_password()
        pw_hash =  bcrypt.generate_password_hash(temp_pw)
        email = users_dict[id].get_email()

        if valid_session:
            users_dict[id].set_password(pw_hash)
            db['Users'] = users_dict
            db.close()
            print(temp_pw)
            pw_msg = "Dear user you have requested for a password request. Use this temporary password to log in and reset afterwards: %s " %(temp_pw)
            msg = Message('Password Reset', sender = 'doctoronthego2022@gmail.com', recipients = [email])
            msg.body = pw_msg
            mail.send(msg)

            return redirect(url_for('staffaccountlist', page=1, staff = name))
        else:
            db.close()
            session.clear()
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

"""Policy Pages Made By Calvin"""
@app.route('/policyPage', methods = ["GET","POST"])
def policyPage():
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
        

        UserName =  get_user_name(idNumber, users_dict)
        valid_session = validate_session(idNumber, users_dict)
        
        db.close()
        if valid_session:
            return render_template('user/user_policies.html', user =UserName)
        else:
            session.clear()
    elif "staff" in session:
        StaffName = session["staff"]
        valid_session , name = validate_session_open_file_admin(StaffName)
        if valid_session:
            return render_template('user/staff_policies.html', staff = name)
        else:
            session.clear()
            return redirect(url_for('home'))
    else:
        return render_template('user/policies.html')

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




"""
#Part Done By XuZhi

@app.route("/News")
def News():
    data=[
        ("01-01-2022",20),
        ("02-01-2022",40),
        ("03-01-2022",30),
        ("04-01-2022",27),
        ("05-01-2022",42),
        ("06-01-2022",36),
        ("07-01-2022",41),
        ("08-01-2022",20)

    ]

    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template('News.html', labels=labels, values=values)
//Unrefined Pt1 code
from flask_bootstrap import Bootstrap


app = Flask(__name__) #Not Needed already previously mentioned
bootstrap = Bootstrap(app) #Quite Unsure what this is for?, Bootstrap incorporated into HTML not WTForms

@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')
@app.route('/News')
def News():
    return render_template('News.html')

@app.route('/consultatioPg1.html')
def consultatioPg1():
    return render_template('consultatioPg1.html')

!!!
#Most of these codes are copied from the Practicals
#Please ensure they fulfill their function before pushing it onto the github
!!!

#In shelve.open you are not suppsoed to add the .db.
#No Use of Adding CreateForm Fucntions if Forms.py is not updated.
#Our customer database is called user
#Our staff database is called staff

@app.route('/createConsultation', methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'c')

        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer.db.")

        consultation = Customer.Customer(create_customer_form.first_name.data, create_customer_form.last_name.data,
                                     create_customer_form.gender.data,
                                     create_customer_form.remarks.data, create_customer_form.email.data,
                                     create_customer_form.date_joined.data,
                                     create_customer_form.doc.data)
        customers_dict[consultation.get_customer_id()] = consultation
        db['Customers'] = customers_dict

        db.close()

        return redirect(url_for('retrieve_customers'))
    return render_template('createConsultation.html', form=create_customer_form)




@app.route('/retrieveCustomer')
def retrieve_customers():
    customers_dict = {}
    db = shelve.open('customer.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)
        print(key)


    return render_template('retrieveCustomer.html', count=len(customers_list), customers_list=customers_list)

@app.route('/viewandchose')
def retrieve_cus():
    customers_dict = {}
    db = shelve.open('customer.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)
        print(key)


    return render_template('viewandchose.html', count=len(customers_list), customers_list=customers_list)



@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = CreateForm(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        users_dict = {}
        db = shelve.open('customer.db', 'w')

        customer_dict = db['Customers']

        customer = customer_dict.get(id)
        customer.set_doc(update_customer_form.doc.data)
        customer.set_first_name(update_customer_form.first_name.data)
        customer.set_last_name(update_customer_form.last_name.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_membership(update_customer_form.membership.data)
        customer.set_remarks(update_customer_form.remarks.data)

        db['Customers'] = users_dict
        db.close()

        return redirect(url_for('retrieve_customers'))
    else:
        users_dict = {}
        oc = shelve.open('user.db', 'w')
        db = shelve.open('customer.db', 'r')
        customer_dict = db['Customers']

        users_dict = oc['Users']
        customer = customer_dict.get(id)
        user=users_dict.get(id)
        db.close()
        oc.close()

        update_customer_form.first_name.data = user.get_first_name()
        update_customer_form.last_name.data = user.get_last_name()
        update_customer_form.gender.data = user.get_gender()
        update_customer_form.remarks.data = user.get_remarks()

        return render_template('updateCustomer.html', form=update_customer_form)



@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']

    users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('retrieve_users'))
@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    users_dict = {}
    db = shelve.open('customer.db', 'w')
    customer_dict = db['Customers']

    customer_dict.pop(id)

    db['Customers'] = customer_dict
    db.close()

    return redirect(url_for('retrieve_customers'))
"""

if __name__ == '__main__':
    app.run(debug=True)
