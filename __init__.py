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

if __name__ == '__main__':
    app.run()
