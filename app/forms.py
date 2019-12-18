from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from neo4j import GraphDatabase

type_all = [{'type':'Akcji'}, {'type':'Komedia'}, {'type':'Dramat'}, {'type':'Historyczny'}]
year_all = [{'year' : str(i)} for i in range(1980, 2020)]


class Form(FlaskForm):
    type = type_all
    year = year_all
    title = StringField('Nazwa')


class RentForms(Form):
    available_only = BooleanField('Tylko dostępne')
    show = SubmitField('Wypożycz')

class AddForm(Form):
    show = SubmitField('Dodaj')
