
def create_Movie(tx, data):
    result = tx.run("CREATE (a:Movie) "
                    "SET a.type = $type, a.year=$year, a.title=$title", type=data["type"], year=data["year"], title=data["title"])



def rent_Movie(tx, **data):
    print(data["year"])
    records = []
    # if data["year"]
    for record in tx.run("MATCH (a:Movie)"
                         "WHERE a.type = $type and a.year=$year and a.title=$title "
                         "RETURN a", type=data["type"], year=data["year"], title=data["title"]):
        print(record.data()["a"])
        records.append(record)
    return records
