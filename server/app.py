from flask import Flask
from flask_cors import CORS
from flask import render_template

app = Flask(__name__)
CORS(app)

@app.route("/greeting")
def greeting():  # put application's code here
    return {"greeting": "Let's start!"}
def button_click():
    return {"clk": "Std"}

@app.route("/")
def index():  # put application's code here
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
