from flask import Flask, render_template

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/baseAgent')
def base_agent():
    return render_template('baseAgent.html')

@app.route('/welcomeAgent')
def welcome_agent():
    return render_template('welcomeAgent.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
