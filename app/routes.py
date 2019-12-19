from flask import render_template, flash, redirect, url_for, request, session
from app import app
from app.forms import *
from app.db import *

uri = "bolt://hobby-jhijfgnijmdigbkenbpomfdl.dbs.graphenedb.com:24787"
driver = GraphDatabase.driver(uri, auth=("admin", "b.BD58tJTtp9NT.s2YQCWQVZYrteRGf"))
tmp_list = None

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/create_account', methods=['POST', 'GET'])
def create_account():
    form = SingInForm()
    if form.validate_on_submit():
        record = {"login": request.form.get('login'), "password": request.form.get('password')}
        print(record)
        driver.session().write_transaction(create_accountT, record)
        return render_template('login.html', title='Sign In', form=form)
    return render_template('sign_in.html', title='Sign In', form=form)


@app.route('/zaloguj', methods=['POST', 'GET'])
def log_in():
    form = LogIn()
    if form.validate_on_submit():
        record = {"login": request.form.get('login'), "password": request.form.get('password')}
        print(record)
        driver.session().write_transaction(logInT, record)
        return redirect('/index')
        # return render_template('login.html', title='Sign In', form=form)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/pokaz_filmy' , methods=['POST', 'GET'])
def show_movies():
    print(request.form)
    global tmp_list
    if session.get('list') is not None:
        tmp_list = session['list']
    if request.method == 'POST':
        if request.form.get('Wypozycz') == 'Wypozycz':
            print(session.get('login'))
            if session.get('login') is not None:
                print("login@@@@@@")
                record = {"type": tmp_list[0]["type"], "year": tmp_list[0]['year'], "title": tmp_list[0]['title'], "login" : session['login']}
                with driver.session() as s:
                    records = s.read_transaction(rent_Movie, **record)
            else:
                return redirect(url_for('log_in'))
                flash("aby kontynuowac musisz sie zalogowac!")

    return render_template('wypozycz_film.html', title='Wypozycz film', list = tmp_list)

@app.route('/wypozycz', methods=['POST', 'GET'])
def rent():
    form = RentForms()
    if form.validate_on_submit():
        record = {"type": request.form.get('type'), "year": request.form.get('year'), "title": request.form.get('title')}
        records = []
        with driver.session() as s:
            records = s.read_transaction(show_Movie, **record)
        print(records)
        global tmp_list
        tmp_list = records
        session['list'] = records
        return redirect(url_for('show_movies'))
    return render_template('wypozycz.html', title='Wypozycz', form=form)

@app.route('/oddaj', methods=['POST', 'GET'])
def return_movie():
    form = AddForm()
    if form.validate_on_submit():
        record = {"type": request.form.get('type'), "year": request.form.get('year'), "title": request.form.get('title')}
        driver.session().write_transaction(create_Movie, record)
        return redirect(url_for('index'))
    return render_template('dodaj.html', title='Dodaj Pozycje', form=form)

@app.route('/dodaj', methods=['POST', 'GET'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        record = {"type": request.form.get('type'), "year": request.form.get('year'), "title": request.form.get('title')}
        driver.session().write_transaction(create_Movie, record)
        return redirect(url_for('index'))
    return render_template('dodaj.html', title='Dodaj Pozycje', form=form)

@app.route('/wszystkie_filmy', methods=['POST', 'GET'])
def all():
    records = driver.session().write_transaction(all_Movie)
    session['list'] = records
    return render_template('dostepne_filmy.html', title='Pokaz filmy')

@app.route('/wypozyczone_filmy', methods=['POST', 'GET'])
def rented():
    records = driver.session().write_transaction(rented_Movie)
    session['list'] = records
    return render_template('wypozyczone_filmy.html', title='Pokaz filmy')
