from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup2')
def signup2():
    return render_template('signup2.html')

@app.route('/signup3')
def signup3():
    return render_template('signup3.html')

@app.route('/signupC')
def signupC():
    return render_template('signupcomplete.html')

@app.route('/user')
def user():
    return render_template('useraccount.html')

@app.route('/infoedit')
def userinfo():
    return render_template('user_info_edit.html')

@app.route('/pwedit')
def userpw():
    return render_template('user_password_edit.html')

@app.route('/useraddress')
def useraddress():
    return render_template('user_address.html')

@app.route('/usercard')
def usercard():
    return render_template('user_cardinfo.html')

@app.route('/staffapp')
def staffapp():
    return render_template('staffappoint.html')

@app.route('/stafffeed')
def stafffeed():
    return render_template('stafffeedback.html')

@app.route('/staffinvent')
def staffinvent():
    return render_template('staffinventory.html')

@app.route('/stafflist')
def stafflist():
    return render_template('stafflist.html')

@app.route('/staffprod')
def staffprod():
    return render_template('staffproduct.html')

if __name__ == '__main__':
    app.run(debug=True)
