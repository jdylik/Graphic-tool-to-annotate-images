from flask import Flask, request
from flask_cors import CORS
from flask_mysqldb import MySQL
import json

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'projekt_io'
mysql = MySQL(app)

@app.route('/get_logins_and_passwords')
def get_logins_and_passwords():
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT login, hasło from logowanie")
        logdata_list = cur.fetchall()
        cur.close()
        return json.dumps({"logdatalist": logdata_list}, ensure_ascii=False)
    except Exception:
        cur.close()
        return("Ojojoj")
@app.route('/insert_new_data', methods=['POST'])
def insert_new_data():
    data = request.json
    data = data['params']
    new_login = data.split("\"")[1]
    new_password = data.split("\"")[3]
    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO logowanie (login, hasło) VALUES (%s, %s)", (new_login, new_password))
        mysql.connection.commit()
        cur.close()
        return("Success")
    except Exception:
        cur.close()
        return("Ojojoj")
@app.route('/insert_new_image', methods=['POST'])
def insert_new_image():
    data = request.json
    data = data['params']
    data = data.split(",")
    image = data[0].split("\"")[3]
    login = data[1].split("\"")[3]
    password = data[2].split("\"")[3]
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id FROM logowanie WHERE login = %s AND hasło = %s", (login, password))
        id = cur.fetchall()
        id = id[0][0]
        cur.execute("INSERT INTO import (obraz, id_uż) VALUES (%s, %s)", (image, id))
        mysql.connection.commit()
        cur.close()
        return ("Success")
    except Exception:
        cur.close()
        return ("Ojojoj")
@app.route('/get_imported_images', methods=['POST'])
def get_imported_images():
    data = request.json
    data = data['params']
    login = data.split("\"")[3]
    password = data.split("\"")[7]
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id FROM logowanie WHERE login = %s AND hasło = %s", (login, password))
        id = cur.fetchall()
        id = id[0][0]
        cur.execute("SELECT obraz FROM import WHERE id_uż = %s", (id,))
        images = cur.fetchall()
        cur.close()
        return json.dumps({"images": images}, ensure_ascii=False)
    except Exception:
        cur.close()
        return ("Ojojoj")

@app.route('/get_annotated_images', methods=['POST'])
def get_annotated_images():
    data = request.json
    data = data['params']
    login = data.split("\"")[3]
    password = data.split("\"")[7]
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id FROM logowanie WHERE login = %s AND hasło = %s", (login, password))
        id = cur.fetchall()
        id = id[0][0]
        cur.execute("SELECT obraz FROM zadnotowane WHERE id_u = %s", (id,))
        images = cur.fetchall()
        cur.close()
        return json.dumps({"images": images}, ensure_ascii=False)
    except Exception:
        cur.close()
        return ("Ojojoj")

if __name__ == '__main__':
    app.run()
