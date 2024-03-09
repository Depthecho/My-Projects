import sqlite3 as sq
import os
from DataBase import DataBase
from flask import Flask, render_template, request, flash, url_for, abort, session, redirect

DATABASE = '/tmp/shoes.db'
DEBUG = True
SECRET_KEY = '34556163qwe34556163'


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update({'DATABASE': os.path.join(app.root_path, 'shoes.db')})


def connect_db():
    con = sq.connect(app.config['DATABASE'])
    con.row_factory = sq.Row
    return con


def create_db():
    db = connect_db()
    with open('create_db.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


@app.route('/index')
@app.route('/')
def index():
    db_con = connect_db()
    dbase = DataBase(db_con)
    return render_template('index.html', title='Shoe Store', menu=dbase.get_objects('mainmenu'))


@app.route('/catalog')
def catalog():
    db_con = connect_db()
    dbase = DataBase(db_con)
    return render_template('catalog.html', title='Catalog', menu=dbase.get_objects('mainmenu'), shoes=dbase.get_objects
    ('shoes'))


@app.route('/add_catalog', methods=['GET', 'POST'])
def add_shoe():
    db_con = connect_db()
    dbase = DataBase(db_con)
    if request.method == 'POST':
        if len(request.form['name']) < 3:
            flash('Ошибка добавления обуви')
        else:
            res = dbase.add_shoes(request.form['name'], request.form['description'], request.form['size'],
                                  request.form['price'], request.form['url'])
            if res:
                flash('Обувь успешно добавлена в каталог!', category='success')
            else:
                flash('Ошибка добавления обуви в каталог!', category='error')

    return render_template('add_shoe.html', title='Add shoe', menu=dbase.get_objects('mainmenu'), shoes=dbase.get_objects
    ('shoes'))


@app.route('/show_shoe/<shoe_id>')
def show_shoe(shoe_id):
    db_con = connect_db()
    dbase = DataBase(db_con)
    name, shoe = dbase.get_shoe(shoe_id)
    if not name:
        abort(404)
    return render_template('shoes.html', title=name, shoe=shoe, menu=dbase.get_objects('mainmenu'))


@app.errorhandler(404)
def page_not_found(error):
    db_con = connect_db()
    dbase = DataBase(db_con)
    return render_template('page404.html', title='Page not found',  menu=dbase.get_objects('mainmenu'))


if __name__ == '__main__':
    create_db()
    app.run()


# Не могу сообразить, почему не работает функция показа обуви отдельно