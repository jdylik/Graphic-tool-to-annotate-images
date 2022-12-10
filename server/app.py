from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/greeting")
def greeting():  # put application's code here
    return {"greeting": "Let's start!"}
def button_click():
    return {"clk": "Std"}


if __name__ == '__main__':
    app.run()
