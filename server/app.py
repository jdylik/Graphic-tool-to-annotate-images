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
    data = eval(data)
    new_login = data[len(data) - 2]
    new_password = data[len(data) - 1]
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
    data = eval(data)
    login = data["login"]
    password = data["password"]
    image = data["img"]
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
    data = eval(data)
    login = data["login"]
    password = data["password"]
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


@app.route('/get_annotated_images_no_rects', methods=['POST'])
def get_annotated_images_no_rects():
    data = request.json
    data = data['params']
    data = eval(data)
    login = data["login"]
    password = data["password"]
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id FROM logowanie WHERE login = %s AND haslo = %s", (login, password))
        id = cur.fetchall()
        id = id[0][0]
        cur.execute("SELECT obraz FROM import WHERE id_uz = %s AND czy_adnotacja=%s", (id, 1))
        images = cur.fetchall()
        cur.execute("SELECT id_o FROM import WHERE id_uz = %s AND czy_adnotacja=%s", (id, 1))
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
    data = eval(data)
    login = data["login"]
    password = data["password"]
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id FROM logowanie WHERE login = %s AND haslo = %s", (login, password))
        id = cur.fetchall()
        id = id[0][0]
        cur.execute("SELECT id_o FROM import WHERE id_uz = %s AND czy_adnotacja=%s", (id, 1))
        ids = cur.fetchall()
        ids_list = []
        images = []
        adns = []
        for id_o in ids:
            ids_list.append(id_o[0])
        for id_o in ids_list:
            cur.execute("SELECT obraz FROM import WHERE id_uz = %s AND czy_adnotacja=%s", (id, 1))
            image = cur.fetchall()
            cur.execute("SELECT id_kat, x_start, y_start, szer, wys FROM adnotacje WHERE id_o = %s", (id_o,))
            adn_data = cur.fetchall()
            for rect in adn_data:
                adns.append(id_o)
                adns.append(image)
                category = rect[0]
                cur.execute("SELECT nazwa, szkic_kolor, wyp_kolor FROM kategorie WHERE id = %s AND id_uz = %s",
                            (category, id))
                cat_data = cur.fetchall()
                cat_data = cat_data[0]
                rect = list(rect[1:])
                rect.extend(cat_data)
                adns.extend(rect)
                images.append(adns)
                adns = []
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
    unique_labels = []
    unique_indexes = []
    for i, element in enumerate(labels):
        if element not in unique_labels:
            unique_labels.append(element)
            unique_indexes.append(i)
    image = data["image"]
    rec_beg_x = data["rec_beg_x"]
    rec_beg_y = data["rec_beg_y"]
    rec_w = data["rec_w"]
    rec_h = data["rec_h"]
    fill_colors = data["fill_colors"]
    stroke_colors = data["stroke_colors"]
    unique_fill_c = [fill_colors[i] for i in unique_indexes]
    unique_stroke_c = [stroke_colors[i] for i in unique_indexes]
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id FROM logowanie WHERE login = %s AND haslo = %s", (login, password))
        id = cur.fetchall()
        id = id[0][0]
        cur.execute("SELECT id_o FROM import WHERE obraz = %s AND id_uz = %s", (image, id))
        image_id = cur.fetchall()
        image_id = image_id[0][0]
        cur.execute("SELECT COUNT(*) FROM adnotacje WHERE id_o = %s", (image_id,))
        nr = cur.fetchall()
        nr = int(nr[0][0])
        if len(labels) == 0 and nr != 0:
            cur.execute("DELETE FROM adnotacje WHERE id_o = %s", (image_id,))
        elif len(labels) < nr:
            for i in range(0, len(labels)):
                cur.execute("SELECT COUNT(*) FROM kategorie WHERE nazwa = %s AND id_uz = %s", (unique_labels[i], id))
                if_exists = cur.fetchall()
                if_exists = if_exists[0][0]
                if int(if_exists) == 0:
                    cur.execute("INSERT INTO kategorie (nazwa, szkic_kolor, wyp_kolor, id_uz) VALUES (%s, %s, %s, %s)",
                                (unique_labels[i], str(unique_stroke_c[i]), str(unique_fill_c[i]), id))
                    mysql.connection.commit()
            cur.execute("SELECT x_start, y_start, szer, wys FROM adnotacje WHERE id_o = %s", (image_id,))
            ann_data = cur.fetchall()
            for i in range(0, len(ann_data)):
                annotation = ann_data[i]
                x_start = annotation[0]
                y_start = annotation[1]
                szer = annotation[2]
                wys = annotation[3]
                if x_start not in rec_beg_x or y_start not in rec_beg_y or szer not in rec_w or wys not in rec_h:
                    cur.execute(
                        "DELETE FROM adnotacje WHERE id_o = %s AND x_start = %s AND y_start = %s AND szer = %s AND wys = %s",
                        (image_id, x_start, y_start, szer, wys))
                    mysql.connection.commit()
            cur.execute("SELECT x_start, y_start, szer, wys FROM adnotacje WHERE id_o = %s", (image_id,))
            existing_adn = cur.fetchall()
            for annot in existing_adn:
                for index, element in enumerate(rec_beg_x):
                    if element != annot[0] or rec_beg_y[index] != annot[1] or rec_w[index] != annot[2] or rec_h[
                        index] != annot[3]:
                        cur.execute(
                            "INSERT INTO adnotacje (id_kat, id_o, x_start, y_start, szer, wys) VALUES (%s, %s, %s, %s, %s, %s)",
                            (labels[index], image_id, rec_beg_x[index], rec_beg_y[index], rec_w[index], rec_h[index]))
                        mysql.connection.commit()
        else:
            for i in range(0, len(labels)):
                cur.execute("SELECT COUNT(*) FROM kategorie WHERE nazwa = %s AND id_uz = %s", (labels[i], id))
                if_exists = cur.fetchall()
                if_exists = if_exists[0][0]
                if int(if_exists) == 0:
                    cur.execute("INSERT INTO kategorie (nazwa, szkic_kolor, wyp_kolor, id_uz) VALUES (%s, %s, %s, %s)",
                                (unique_labels[i], str(unique_stroke_c[i]), str(unique_fill_c[i]), id))
                    mysql.connection.commit()
                cur.execute("SELECT id FROM kategorie WHERE nazwa=%s AND id_uz = %s", (labels[i], id))
                label_id = cur.fetchall()
                label_id = label_id[0][0]
                cur.execute(
                    "INSERT INTO adnotacje (id_kat, id_o, x_start, y_start, szer, wys) VALUES (%s, %s, %s, %s, %s, %s)",
                    (label_id, image_id, rec_beg_x[i], rec_beg_y[i], rec_w[i], rec_h[i]))
        cur.execute("UPDATE import SET czy_adnotacja = (%s) WHERE id_o = (%s) AND id_uz = (%s)", (1, image_id, id))
        mysql.connection.commit()
        cur.close()
        return json.dumps({"annotation": labels}, ensure_ascii=False)
    except Exception:
        cur.close()
        return "Ojojoj"

@app.route('/save_image_info', methods=['POST'])
def save_image_info():
    data = request.json
    data = data['params']
    data = eval(data)
    login = data["login"]
    password = data["password"]
    image = data["image"]
    name = data["name"]
    camera = data["camera"]
    location = data["location"]
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id FROM logowanie WHERE login = %s AND haslo = %s", (login, password))
        id = cur.fetchall()
        id = id[0][0]
        cur.execute("SELECT id_o FROM import WHERE obraz = %s AND id_uz = %s", (image, id))
        image_id = cur.fetchall()
        image_id = image_id[0][0]
        cur.execute("SELECT COUNT(*) FROM info WHERE id_o = %s", (image_id,))
        if_exists = cur.fetchall()
        if_exists = if_exists[0][0]
        if int(if_exists) == 0:
            cur.execute("INSERT INTO info (id_o, rodz_kam, pochodzenie, nazwa_pliku) VALUES (%s, %s, %s, %s)", (image_id, camera, location, name))
        else:
            cur.execute("UPDATE info SET rodz_kam = (%s), pochodzenie = (%s), nazwa_pliku = (%s) WHERE id_o = (%s)", (camera, location, name, image_id))
        mysql.connection.commit()
        cur.close()
        return "Sukces"
    except Exception:
        cur.close()
        return "Ojojoj"
@app.route('/get_image_info', methods=['POST'])
def get_image_info():
    data = request.json
    data = data['params']
    data = eval(data)
    login = data["login"]
    password = data["password"]
    image = data["image"]
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id FROM logowanie WHERE login = %s AND haslo = %s", (login, password))
        id = cur.fetchall()
        id = id[0][0]
        cur.execute("SELECT id_o FROM import WHERE obraz = %s AND id_uz = %s", (image, id))
        image_id = cur.fetchall()
        image_id = image_id[0][0]
        cur.execute("SELECT COUNT(*) FROM info WHERE id_o = %s", (image_id,))
        if_exists = cur.fetchall()
        if_exists = if_exists[0][0]
        if int(if_exists) == 0:
            cur.close()
            return "0"
        else:
            cur.execute("SELECT rodz_kam, pochodzenie, nazwa_pliku FROM info WHERE id_o = %s", (image_id,))
            data = cur.fetchall()
            data = data[0]
        cur.close()
        return json.dumps({"description": data}, ensure_ascii=False)
    except Exception:
        cur.execute("SELECT rodz_kam, pochodzenie, nazwa_pliku FROM info WHERE id_o = %s", (image_id,))
        cur.close()
        return "Ojojoj"

@app.route('/get_annotations', methods=['POST'])
def get_annotations():
    data = request.json
    data = data['params']
    data = eval(data)
    login = data["login"]
    password = data["password"]
    image = data["image"]
    rect_indexes = []
    rec_beg_x = []
    rec_beg_y = []
    rec_w = []
    rec_h = []
    labels = []
    fill_colors = []
    stroke_colors = []
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id FROM logowanie WHERE login = %s AND haslo = %s", (login, password))
        id = cur.fetchall()
        id = id[0][0]
        cur.execute("SELECT id_o FROM import WHERE obraz = %s AND id_uz = %s", (image, id))
        image_id = cur.fetchall()
        image_id = image_id[0][0]
        cur.execute("SELECT * FROM adnotacje where id_o=%s", (image_id,))
        anno_info = cur.fetchall()
        anno_num = len(anno_info)
        for i in range(0, anno_num):
            rect_indexes.append(anno_info[i][0])
            rec_beg_x.append(anno_info[i][3])
            rec_beg_y.append(anno_info[i][4])
            rec_w.append(anno_info[i][5])
            rec_h.append(anno_info[i][6])
            cur.execute("SELECT nazwa, szkic_kolor, wyp_kolor FROM kategorie WHERE id = %s AND id_uz = %s",
                        (anno_info[i][1], id))
            cat_data = cur.fetchall()
            labels.append(cat_data[0][0])
            fill_colors.append(cat_data[0][1])
            stroke_colors.append(cat_data[0][2])
        mysql.connection.commit()
        cur.close()
        unique_indexes = []
        unique_elements = []
        for index, element in enumerate(rec_beg_x):
            if element not in unique_elements:
                unique_elements.append(element)
                unique_indexes.append(index)
        rec_beg_x = unique_elements
        rec_beg_y = [rec_beg_y[i] for i in unique_indexes]
        rec_w= [rec_w[i] for i in unique_indexes]
        rec_h = [rec_h[i] for i in unique_indexes]
        labels = [labels[i] for i in unique_indexes]
        stroke_colors = [stroke_colors[i] for i in unique_indexes]
        fill_colors = [fill_colors[i] for i in unique_indexes]
        return json.dumps({"rect index": rect_indexes, "rec_beg_x": rec_beg_x, "rec_beg_y": rec_beg_y, "rec_w": rec_w,
                           "rec_h": rec_h, "labels": labels, "stroke_cols": stroke_colors, "fill_cols": fill_colors},
                          ensure_ascii=False)
    except Exception:
        cur.close()
        return "Ojojoj"


@app.route('/get_categories', methods=['POST'])
def get_categories():
    data = request.json
    data = data['params']
    data = eval(data)
    login = data["login"]
    password = data["password"]
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id FROM logowanie WHERE login = %s AND haslo = %s", (login, password))
        id = cur.fetchall()
        id = id[0][0]
        cur.execute("SELECT COUNT(*) FROM kategorie WHERE id_uz = %s", (id,))
        if_exist = cur.fetchall()
        if_exist = if_exist[0][0]
        if int(if_exist) == 0:
            cur.close()
            return "1"
        else:
            cur.execute("SELECT nazwa FROM kategorie WHERE id_uz = %s", (id,))
            categories = cur.fetchall()
            cur.execute("SELECT szkic_kolor FROM kategorie WHERE id_uz = %s", (id,))
            stroke_cols = cur.fetchall()
            cur.execute("SELECT wyp_kolor FROM kategorie WHERE id_uz=%s", (id,))
            fill_cols = cur.fetchall()
            cur.close()
            return json.dumps({"names": categories, "stroke_colors": stroke_cols, "fill_colors": fill_cols},
                              ensure_ascii=False)
    except Exception:
        cur.close()
        return "Ojojoj"

@app.route('/get_categories_coco', methods=['POST'])
def get_categories_coco():
    data = request.json
    data = data['params']
    data = eval(data)
    login = data["login"]
    password = data["password"]
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id FROM logowanie WHERE login = %s AND haslo = %s", (login, password))
        id = cur.fetchall()
        id = id[0][0]
        cur.execute("SELECT COUNT(*) FROM kategorie WHERE id_uz = %s", (id,))
        if_exist = cur.fetchall()
        if_exist = if_exist[0][0]
        if int(if_exist) == 0:
            cur.close()
            return "1"
        else:
            cur.execute("SELECT id, nazwa FROM kategorie WHERE id_uz = %s", (id,))
            categories = cur.fetchall()
            cur.close()
            return json.dumps({"names": categories}, ensure_ascii=False)
    except Exception:
        cur.close()
        return "Ojojoj"

@app.route('/get_image_and_annotation_info_coco', methods=['POST'])
def get_image_and_annotation_info_coco():
    data = request.json
    data = data['params']
    data = eval(data)
    login = data["login"]
    password = data["password"]
    ind = data["indexes"]
    categories = []
    names = []
    camera = []
    location = []
    ids_for_adns = []
    id_kat = []
    x_start = []
    y_start = []
    szer = []
    wys = []
    adnid = []
    idadn = 1
    images = []
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id FROM logowanie WHERE login = %s AND haslo = %s", (login, password))
        id = cur.fetchall()
        id = id[0][0]
        cur.execute("SELECT id_o from import WHERE id_uz = %s AND czy_adnotacja = 1", (id, ))
        id_o = cur.fetchall()
        temp = [id_o[index - 1][0] for index in ind]
        ind = temp
        ind_in_order = []
        for index in ind:
            cur.execute("SELECT obraz from import WHERE id_uz = %s AND id_o = %s AND czy_adnotacja = 1", (id, index))
            image = cur.fetchall()
            image = image[0][0]
            images.append(image)
        for i in range(len(images)):
            cur.execute("SELECT rodz_kam, pochodzenie, nazwa_pliku from info WHERE id_o = %s", (ind[i],))
            info = cur.fetchall()
            camera.append(info[0][0])
            location.append(info[0][1])
            names.append(info[0][2])
            cur.execute("SELECT * from adnotacje WHERE id_o = %s", (ind[i],))
            adns = cur.fetchall()
            for adn in adns:
                ids_for_adns.append(idadn)
                adnid.append(adn[0])
                id_kat.append(adn[1])
                x_start.append(adn[2])
                y_start.append(adn[3])
                szer.append(adn[4])
                wys.append(adn[5])
                ind_in_order.append(ind[i])
                idadn += 1
        cur.close()
        return json.dumps({"id_o":ind_in_order, "names": names, "camera": camera, "location": location, "adnid": adnid,
                           "ids_for_adns":ids_for_adns,"id_kat":id_kat, "x_start":x_start, "y_start":y_start,
                           "szer":szer, "wys":wys}, ensure_ascii=False)
    except Exception:
        cur.close()
        return "Ojojoj"

@app.route('/get_names_of_files', methods=['POST'])
def get_names_of_files():
    data = request.json
    data = data['params']
    data = eval(data)
    login = data["login"]
    password = data["password"]
    ind = data["indexes"]
    names = []
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id FROM logowanie WHERE login = %s AND haslo = %s", (login, password))
        id = cur.fetchall()
        id = id[0][0]
        cur.execute("SELECT id_o from import WHERE id_uz = %s AND czy_adnotacja = 1", (id,))
        id_o = cur.fetchall()
        real_ind = []
        for index, t_index in enumerate(ind):
            val = id_o[index][0]
            real_ind.append(val)
        names = []
        for t_index in real_ind:
            cur.execute("SELECT nazwa_pliku from info WHERE id_o = %s",(t_index,))
            name = cur.fetchall()
            name = name[0][0]
            names.append(name)
        return json.dumps({"names": names}, ensure_ascii=False)
    except Exception:
        cur.close()
        return "Ojojoj"
@app.route('/change_index_to_id', methods=['POST'])
def change_index_to_id():
    data = request.json
    data = data['params']
    data = eval(data)
    login = data["login"]
    password = data["password"]
    ind = data["indexes"]
    names = []
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id FROM logowanie WHERE login = %s AND haslo = %s", (login, password))
        id = cur.fetchall()
        id = id[0][0]
        cur.execute("SELECT id_o from import WHERE id_uz = %s AND czy_adnotacja = 1", (id,))
        id_o = cur.fetchall()
        new_id = []
        for index,id in enumerate(id_o):
            if index in ind:
                new_id.append(id)
        return json.dumps({"ids": new_id}, ensure_ascii=False)
    except Exception:
        cur.close()
        return "Ojojoj"

if __name__ == '__main__':
    app.run()
