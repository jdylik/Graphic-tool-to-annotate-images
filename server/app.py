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
        cur.execute("SELECT obraz FROM import WHERE id_uz = %s AND czy_adnotacja=%s", (id,0))
        images = cur.fetchall()
        cur.close()
        return json.dumps({"images": images}, ensure_ascii=False)
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
        cur.execute("SELECT obraz FROM import WHERE id_uz = %s AND czy_adnotacja=%s", (id,1))
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
    # data1 = str(data).split(",")
    # login = str(data1).split("\"")[3]
    # password = str(data1).split("\"")[7]

    #powinno sie wycinac dobrze - sprawdzalam
    #nie polecam tutaj splitowac po przecinkach, bo te punkty są w listach wiec przecinki sa w ich srodku
    #ten sposob najbezpieczniejszy
    data2 = str(data).split("\"labels\":")[1] #wywalalo mi bledy ze data jest lista a nie stringiem
    labels=eval(str(data2).split(",\"image index\"")[0]) #eval zamienia z powrotem na liste tam gdzie potrzeba
    data3=str(data).split("\"image index\":")[1]
    image_index=int(str(data3).split(",")[0])
    data4=str(data).split("\"rec_beg_x\":")[1]
    rec_beg_x=eval(str(data4).split(",\"")[0])
    data5 = str(data).split("\"rec_beg_y\":")[1]
    rec_beg_y = eval(str(data5).split(",\"")[0])
    data6 = str(data).split("\"rec_w\":")[1]
    rec_w = eval(str(data6).split(",\"")[0])
    data7 = str(data).split("\"rec_h\":")[1]
    rec_h = eval(str(data7).split("}")[0])
    cur = mysql.connection.cursor()
    try:
        #w tej funkcji logowanie nam niepotrzebne
        #zreszta z logowaniem tez nie dziala
        # cur.execute("SELECT id FROM logowanie WHERE login = %s AND haslo = %s", (login, password))
        # id = cur.fetchall()
        # id = id[0][0]

        #petla tyle razy ile jest zaznaczen na zdj
        for i in range(0, len(labels)):
            label=labels[i]
            #sprawdzamy czy taka etykieta jest w bazie
            cur.execute("SELECT COUNT(*) from kategorie WHERE nazwa = %s", label)
            exists=cur.fetchall()
            exists=exists[0][0]
            #jesli nie ma to najpierw ja dodajemy
            if int(exists)==int(0):
                cur.execute("INSERT INTO kategorie (nazwa) VALUES (%s)",label)
            #wyluskujemy id etykiety
            cur.execute("SELECT id from kategorie where nazwa=%s",label)
            label_id=cur.fetchall()
            label_id=label_id[0][0]
            #dodajemy adnotacje do bazy
            cur.execute("INSERT INTO adnotacje (id_kat,id_o,x_start,y_start,szer,wys) VALUES (%s, %s, %s, %s, %s, %s)",
                        (label_id, image_index,rec_beg_x[i], rec_beg_y[i], rec_w[i], rec_h[i]))
        #na koniec oznaczamy zdjecie jako adnotowane
        cur.execute("UPDATE import SET czy_adnotacja = (%s) WHERE id_o = (%s)", (1, image_index))
        mysql.connection.commit()
        cur.close()
        #zwrocenie czegokolwiek
        return json.dumps({"annotation": labels}, ensure_ascii=False)
    except Exception:
        cur.close()
        return "Ojojoj"


if __name__ == '__main__':
    app.run()
