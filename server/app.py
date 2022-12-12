from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/name')
def name():  # put application's code here
    return {"name":"Tutaj będzie można dodać adnotacje do zdjęć."}


if __name__ == '__main__':
    app.run()
