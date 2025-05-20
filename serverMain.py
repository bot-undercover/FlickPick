from flask import Flask, request, render_template, redirect, abort

from Main.data.api import *
import socket
from Main.data import db_session
#
PasswordForAdmin = "12345"
#
app = Flask(__name__)

@app.route('/')
def homePage():
    return renderTemplate("main.html")


@app.route('/login')
def login():
    if getLocalUserData().id != -1: return redirect("/")
    return renderTemplate("login.html")


# Эта платформа позволяет находить новые фильмы, оценивать, советовать их другим пользователям!
@app.route('/register')
def register():
    if getLocalUserData().id != -1: return redirect("/")
    return renderTemplate("register.html")


@app.route('/account')
@app.route('/account/<int:id>')
def account(id=-1):
    if id == -1: id = getLocalUserData().id
    if getLocalUserData().id == -1 and id != None: return redirect("/login")
    return accountRender(id)


@app.route('/films')
@app.route('/films/<id>')
def films(id=-1):
    if getLocalUserData().id == -1: return redirect("/login")
    if id != -1:
        return filmRender(id)
    return renderTemplate("films.html", films=getFilms().order_by((-Film.sumRating / Film.countRating)).all()[:10])


@app.route('/special-dial')
def specialDeal():
    return renderTemplate("specialDial.html")


@app.route('/api', methods=['GET', 'POST'])
def api():
    return Api()

@app.route('/admin')
def adminPanel():
    if not getLocalUserData().isAdmin:
        abort(404)
    return renderTemplate("adminPanel.html")

def start(debug=False):
    db_session.global_init("DataBases/WebSiteDataBase.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.login == "admin").first()
    if not user:
        user = User()
        user.login = "admin"
        user.ratingCount = 100
        user.ratingSum = 1000
        user.isAdmin = True
        user.hashedPassword = hashlib.sha512(PasswordForAdmin.encode()).hexdigest()
        user.name = "Администратор"
        db_sess.add(user)
    db_sess.commit()
    db_sess.close()
    print(f"# login: admin password: {PasswordForAdmin}")
    app.run(port=80, host=socket.gethostbyname(socket.gethostname()), debug=debug)


if __name__ == '__main__':
    start(True)
