from flask import Flask
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


@app.route('/name')
def name():  # put application's code here
    return json.dumps({"name": "Tutaj będzie można dodać adnotacje do zdjęć."}, ensure_ascii=False)


if __name__ == '__main__':
    app.run()
