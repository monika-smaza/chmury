import json
from flask import flash, session
def create_Movie(tx, data):
    result = tx.run("CREATE (a:Movie) "
                    "SET a.type = $type, a.year=$year, a.title=$title", type=data["type"], year=data["year"], title=data["title"])



def show_Movie(tx, **data):
    print(data["year"])
    records = []
    # if data["year"]
    for record in tx.run("MATCH (a:Movie)"
                         "WHERE a.type = $type and a.year=$year and a.title=$title "
                         "RETURN a", type=data["type"], year=data["year"], title=data["title"]):
        print(record.data()["a"]["properties"])
        print(record.data())
        print(record["a"].get("type"))
        print(record["a"].get("title"))
        print(record["a"].get("year"))
        records.append({"type": record["a"].get("type"),
                        "year": record["a"].get("year"),
                        "title": record["a"].get("title")})
    return records

def all_Movie(tx):
    records = []
    for record in tx.run("MATCH (a:Movie)"
                        "RETURN a"):

        print(record.data()["a"]["properties"])
        print(record.data())
        print(record["a"].get("type"))
        print(record["a"].get("title"))
        print(record["a"].get("year"))
        records.append({"type": record["a"].get("type"),
                        "year": record["a"].get("year"),
                        "title": record["a"].get("title")})
    return records

def my_Movie(tx):
    records = []
    for record in tx.run("MATCH (a:User)"
                        "RETURN a"):

        print(record.data()["a"]["properties"])
        print(record.data())
        print(record["a"].get("type"))
        print(record["a"].get("title"))
        print(record["a"].get("year"))
        records.append({"type": record["a"].get("type"),
                        "year": record["a"].get("year"),
                        "title": record["a"].get("title")})
    return records


def rented_Movie(tx):
    records = []
    for record in tx.run("MATCH (a:Movie)-[r:RENT]-(u:User)"
                        "RETURN u, r, a"):
        print(record.data()["u"]["login"])
        print(record.data()["r"])
        print(record.data()["a"])

        print(record.data()["a"]["properties"])
        print(record.data())
        print(record["a"].get("type"))
        print(record["a"].get("title"))
        print(record["a"].get("year"))
        records.append({"type": record["a"].get("type"),
                        "year": record["a"].get("year"),
                        "title": record["a"].get("title"),
                        "login": record.data()["u"]["login"]})
    return records

def create_accountT(tx, data):
    records = []
    i = 0
    for record in tx.run("MATCH (a:User)"
                         "WHERE a.login = $login "
                         "RETURN a", login=data["login"]):
        i+=1

    if i == 0:
        result = tx.run("CREATE (a:User) "
                        "SET a.login = $login, a.password=$password", login=data["login"], password=data["password"])
        # session['login'] = data["login"]
        flash("Pomyslnie utworzono konto!")
    else:
        flash("Konto o podanym loginie istnieje")

def logInT(tx, data):
    records = []
    i = 0
    for record in tx.run("MATCH (a:User)"
                         "WHERE a.login = $login and a.password = $password "
                         "RETURN a", login=data["login"], password=data["password"]):
        i+=1

    if i > 0:
        session['login'] = data["login"]
        flash("Zalogowano")
    else:
        flash("Zły login lub hasło")
