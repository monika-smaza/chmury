from flask import render_template, flash, redirect, url_for, request, session
from app import app
from app.forms import *
from app.db import *

uri = "bolt://hobby-jhijfgnijmdigbkenbpomfdl.dbs.graphenedb.com:24787"
driver = GraphDatabase.driver(uri, auth=("admin", "b.BD58tJTtp9NT.s2YQCWQVZYrteRGf"))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/dostepne_filmy')
def available():
    # records = request.form.get('records')
    list = session.pop('my_list', [])
    print(list)
    return render_template('dostepne_filmy.html', title='Dodaj Pozycje')

@app.route('/wypozycz', methods=['POST', 'GET'])
def rent():
    form = RentForms()
    if form.validate_on_submit():
        record = {"type": request.form.get('type'), "year": request.form.get('year'), "title": request.form.get('title')}
        #//name = form.type.data
        with driver.session() as s:
            records = s.read_transaction(rent_Movie, **record)
        session['my_list'] = records
        return redirect(url_for('available'))
    return render_template('wypozycz.html', title='Wypozycz', form=form)

@app.route('/dodaj', methods=['POST', 'GET'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        record = {"type": request.form.get('type'), "year": request.form.get('year'), "title": request.form.get('title')}
        driver.session().write_transaction(create_Movie, record)
        # ÷form.create_Movie(driver)
        return redirect(url_for('index'))
    return render_template('dodaj.html', title='Dodaj Pozycje', form=form)
