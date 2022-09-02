from typing import Optional
from settings import ROOT_PATH, DB_PATH
from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)


class Connection:
    def __init__(self):
        self._connection: Optional[sqlite3.Connection] = None

    def __enter__(self):
        self._connection = sqlite3.connect(DB_PATH)

        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()


@app.route('/phones/create/', methods=['GET', 'POST'])
def create():
    with Connection() as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS hw8 
                    (ID INTEGER PRIMARY KEY, 
                    contactName VARCHAR,
                    phoneValue VARCHAR)""")

        name = request.form.get('name')
        phone = request.form.get('phone')

        if name != None and phone != None:
            values = [name, phone]
            insert_query = ("""INSERT INTO hw8(contactName, phoneValue) VALUES (?,?)""")
            cur.execute(insert_query, values)
            con.commit()

    return render_template('template.html')


@app.route('/phones/read/', methods=['GET'])
def read():
    with Connection() as con:
        cur = con.cursor()
        cur.execute("""SELECT * FROM hw8""")
        rows = cur.fetchall()
        phones_str = []
        for row in rows:
            phones_str.append({'name': row[1], 'phone': row[2]})

    return render_template('read.html', context=phones_str)


@app.route('/phones/update/', methods=['POST', 'GET'])
def update():
    with Connection() as con:
        cur = con.cursor()

        if request.method == 'POST':
            oldname = request.form.get('oldname')
            print(oldname)
            values = [oldname]
            query = """SELECT * FROM hw8 WHERE contactName = ?"""
            cur.execute(query, values)
            res = cur.fetchall()
            print(res)
            if res:
                return redirect(f"/phones/update/{oldname}")

    return render_template('update.html')


@app.route('/phones/update/<oldname>', methods=['GET', 'POST'])
def update_helper(oldname):
    with Connection() as con:
        cur = con.cursor()
        new_name = request.form.get('newname')
        new_phone = request.form.get('newphone')
        if new_name != None and new_phone != None:
            values = [new_name, new_phone, oldname]
            update_query = ("""UPDATE hw8 SET contactName = ?, phoneValue = ? WHERE contactName = ?""")
            cur.execute(update_query, values)
            con.commit()

    return render_template('update_helper.html')


@app.route('/phones/delete', methods=['GET', 'POST', 'PUT'])
def delete():
    with Connection() as con:
        cur = con.cursor()
        todel = request.form.get('todel')
        if todel != None:
            values = [todel]
            delete_query = ("""DELETE FROM hw8 WHERE contactName = ?""")
            cur.execute(delete_query, values)

    return render_template('delete.html')


if __name__ == '__main__':
    app.run(debug=True)








