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
        cur.execute("SELECT login, haslo from logowanie")
        logdata_list = cur.fetchall()
        cur.close()
        return json.dumps({"logdatalist": logdata_list}, ensure_ascii=False)
    except Exception:
        cur.close()
        return "Ojojoj"


@app.route('/insert_new_data', methods=['POST'])
def insert_new_data():
    data = request.json
    data = data['params']
    new_login = data.split("\"")[1]
    new_password = data.split("\"")[3]
    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO logowanie (login, haslo) VALUES (%s, %s)", (new_login, new_password))
        mysql.connection.commit()
        cur.close()
        return "Success"
    except Exception:
        cur.close()
        return "Ojojoj"


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
        cur.execute("SELECT id FROM logowanie WHERE login = %s AND haslo = %s", (login, password))
        id = cur.fetchall()
        id = id[0][0]
        cur.execute("INSERT INTO import (obraz, id_uz) VALUES (%s, %s)", (image, id))
        mysql.connection.commit()
        cur.close()
        return "Success"
    except Exception:
        cur.close()
        return "Ojojoj"


@app.route('/get_imported_images', methods=['POST'])
def get_imported_images():
    data = request.json
    data = data['params']
    login = data.split("\"")[3]
    password = data.split("\"")[7]
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id FROM logowanie WHERE login = %s AND haslo = %s", (login, password))
        id = cur.fetchall()
        id = id[0][0]
        cur.execute("SELECT obraz FROM import WHERE id_uz = %s AND czy_adnotacja=%s", (id, 0))
        images = cur.fetchall()
        cur.execute("SELECT id_o FROM import WHERE id_uz = %s AND czy_adnotacja=%s", (id, 0))
        ids = cur.fetchall()
        cur.close()
        return json.dumps({"images": images, "indexes": ids}, ensure_ascii=False)
    except Exception:
        cur.close()
        return "Ojojoj"


@app.route('/get_annotated_images', methods=['POST'])
def get_annotated_images():
    data = request.json
    data = data['params']
    login = data.split("\"")[3]
    password = data.split("\"")[7]
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id FROM logowanie WHERE login = %s AND haslo = %s", (login, password))
        id = cur.fetchall()
        id = id[0][0]
        cur.execute("SELECT obraz FROM import WHERE id_uz = %s AND czy_adnotacja=%s", (id, 1))
        images = cur.fetchall()
        cur.close()
        return json.dumps({"images": images}, ensure_ascii=False)
    except Exception:
        cur.close()
        return "Ojojoj"


@app.route('/save_annotations', methods=['POST'])
def save_annotations():
    data = request.json
    data = data['params']
    data = eval(data)
    login = data["login"]
    password = data["password"]
    labels = data["labels"]
    image_index = data["image index"]
    rec_beg_x = data["rec_beg_x"]
    rec_beg_y = data["rec_beg_y"]
    rec_w = data["rec_w"]
    rec_h = data["rec_h"]
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id FROM logowanie WHERE login = %s AND haslo = %s", (login, password))
        id = cur.fetchall()
        id = id[0][0]
        for i in range(0, len(labels)):
            cur.execute("SELECT COUNT(*) FROM kategorie WHERE nazwa = %s AND id_uz = %s", (labels[i], id))
            if_exists = cur.fetchall()
            if_exists = if_exists[0][0]
            if int(if_exists) == 0:
                cur.execute("INSERT INTO kategorie (nazwa, id_uz) VALUES (%s, %s)", (labels[i], id))
                mysql.connection.commit()
            cur.execute("SELECT id FROM kategorie WHERE nazwa=%s AND id_uz = %s", (labels[i], id))
            label_id = cur.fetchall()
            label_id = label_id[0][0]
            cur.execute(
                "INSERT INTO adnotacje (id_kat, id_o, x_start, y_start, szer, wys) VALUES (%s, %s, %s, %s, %s, %s)",
                (label_id, image_index, rec_beg_x[i], rec_beg_y[i], rec_w[i], rec_h[i]))
        cur.execute("UPDATE import SET czy_adnotacja = (%s) WHERE id_o = (%s) AND id_uz = (%s)", (1, image_index, id))
        mysql.connection.commit()
        cur.close()
        return json.dumps({"annotation": labels}, ensure_ascii=False)
    except Exception:
        cur.close()
        return "Ojojoj"


if __name__ == '__main__':
    app.run()
