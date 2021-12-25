from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

@app.route('/' , methods=["GET","POST"])
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup' , methods=["GET","POST"])
def signup():
    return render_template('signup.html')

@app.route('/signup2' , methods=["GET","POST"])
def signup2():
    return render_template('signup2.html')

@app.route('/signup3' , methods=["GET","POST"])
def signup3():
    return render_template('signup3.html')

@app.route('/signupC' , methods=["GET","POST"])
def signupC():
    return render_template('signupcomplete.html')

@app.route('/user' , methods=["GET","POST"])
def user():
    return render_template('useraccount.html')

@app.route('/infoedit' , methods=["GET","POST"])
def userinfo():
    return render_template('user_info_edit.html')

@app.route('/pwedit' , methods=["GET","POST"])
def userpw():
    return render_template('user_password_edit.html')

@app.route('/useraddress' , methods=["GET","POST"])
def useraddress():
    return render_template('user_address.html')

@app.route('/usercard' , methods=["GET","POST"])
def usercard():
    return render_template('user_cardinfo.html')

@app.route('/staffapp' , methods=["GET","POST"])
def staffapp():
    return render_template('staffappoint.html')

@app.route('/stafffeed' , methods=["GET","POST"])
def stafffeed():
    return render_template('stafffeedback.html')

@app.route('/staffinvent' , methods=["GET","POST"])
def staffinvent():
    return render_template('staffinventory.html')

@app.route('/stafflist' , methods=["GET","POST"])
def stafflist():
    return render_template('stafflist.html')

@app.route('/staffprod' , methods=["GET","POST"])
def staffprod():
    return render_template('staffproduct.html')

@app.route('/staffadd' , methods=["GET","POST"])
def staffadd():
    return render_template('staffadd.html')

if __name__ == '__main__':
    app.run(debug=True)
