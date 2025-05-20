from data.films import Film
from data import db_session

db_session.global_init("DataBases/WebSiteDataBase.db")
db_sess = db_session.create_session()
with open('DataBases/films.json', 'r', encoding="utf-8") as file:
    data = eval(file.read())
for i in data:
    if db_sess.query(Film).filter(Film.title == i["title"]).first() == None:
        film = Film()
        film.title = i["title"]
        film.description = i["description"]
        film.sumRating = i["rating"] ** 2
        film.countRating = i["rating"]
        film.date = i["year"]
        db_sess.add(film)
        db_sess.commit()
db_sess.close()