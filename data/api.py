from flask import Flask, request, render_template, redirect, make_response, abort, send_file
from cryptography.fernet import Fernet
import hashlib, os, string, datetime
from random import choices

from .users import User
from .films import Film
from . import db_session


def guestUser():
    user = User()
    user.id = -1
    user.name = "Гость"
    user.about = ""
    user.isAdmin = False
    user.picture = "guest.png"
    return user


def Api():
    out = []
    db_sess = db_session.create_session()
    if request.method == 'POST':
        print(request.form)
        if "from" in request.form.keys():
            if request.form["from"] == "login":
                user = db_sess.query(User).filter(User.login == request.form["login"]).first()
                if user and user.hashedPassword == hashlib.sha512(request.form["password"].encode()).hexdigest():
                    cookieKey = Fernet.generate_key()
                    out = make_response(redirect("/account"))
                    out.set_cookie("user", str(cookieKey))
                    user = db_sess.query(User).filter(User.login == request.form["login"]).first()
                    user.cookie = str(cookieKey)
                elif user:
                    out = redirect("/login?alert=Неправильный пароль!")
                else:
                    out = redirect("/login?alert=Нет такого пользователя!")
            elif request.form["from"] == "register":
                if not db_sess.query(User).filter(
                        User.name == request.form["login"]).first() == None: return redirect(
                    f"/register?alert=Пользователь с таким логином уже существует!")
                newUser = User()
                newUser.name = request.form["login"]
                newUser.login = newUser.name
                newUser.hashedPassword = hashlib.sha512(request.form["password"].encode()).hexdigest()
                cookieKey = Fernet.generate_key()
                newUser.cookie = str(cookieKey)
                db_sess.add(newUser)
                out = make_response(redirect("/account"))
                out.set_cookie("user", str(cookieKey))
        elif "film" in request.form.keys():
            move = request.form["film"]
            if move == "add":
                pass
            elif move == "del":
                pass
            elif move == "rateup":
                pass
            elif move == "ratedown":
                pass
            elif move == "publishComment":
                pass
            elif move == "deleteComment":
                pass
            elif move == "find":
                pass
        elif "account" in request.form.keys():
            move = request.form["account"].split()
            if move[0] == "deleteAccount":
                out = redirect(
                    "/account?prompt=Вы уверены что хотите удалить аккаунт? Для этого введите 'Да'.&where=deleteAccount")
            elif move[0] == "changeAbout":
                out = redirect(
                    f"/account?prompt=Изменение описания&standart={getLocalUserData().about}&where=changeAbout")
            elif move[0] == "banAccount":
                if getLocalUserData().isAdmin:
                    user = db_sess.query(User).filter(User.id == int(move[1])).first()
                    if user.picture != "guest.png":
                        os.remove(f"./static/usersPictures/{user.picture}")
                    user.banned = True
                    user.name = "Забаненый"
                    user.picture = "guest.png"

                out = redirect(f"/account/{move[1]}")
            elif move[0] == "unbanAccount":
                if getLocalUserData().isAdmin:
                    user = db_sess.query(User).filter(User.id == int(move[1])).first()
                    user.banned = False
                    user.name = "Разбаненый"
                out = redirect(f"/account/{move[1]}")
            elif move[0] == "changeName":
                out = redirect(f"/account?prompt=Новое имя:&standart={getLocalUserData().name}&where=changeName")
            elif move[0] == "rateup":
                user = db_sess.query(User).filter(
                    User.id == int(move[1]) and int(move[1]) != getLocalUserData().id).first()
                user.ratingSum += 1
                user.ratingCount += 1
                out = redirect(f"/account/{move[1]}")
            elif move[0] == "ratedown":
                user = db_sess.query(User).filter(
                    User.id == int(move[1]) and int(move[1]) != getLocalUserData().id).first()
                user.ratingSum -= 1
                user.ratingCount += 1
                out = redirect(f"/account/{move[1]}")
            elif move[0] == "exitAccount":
                user = db_sess.query(User).filter(User.id == getLocalUserData().id).first()
                user.cookie = ""
                out = make_response(redirect("/login"))
                out.set_cookie("user", "", expires=0)
        elif "ftp" in request.form.keys():
            if getLocalUserData().banned:
                return redirect(f"/account/{getLocalUserData().id}")
            move, = request.form["ftp"],
            if move == "download" and request.form["id"] != None:
                if request.form["id"] != -1:
                    return send_file(f".\\static\\usersPictures\\{getUserById(request.form["id"]).picture}",
                                     as_attachment=True,
                                     download_name=str(request.form["id"]) + "." +
                                                   getUserById(request.form["id"]).picture.split(".")[-1])
            elif move == "upload":
                return renderTemplate("uploading.html")
            elif move == "getFile":
                if getLocalUserData().id != -1:
                    file = request.files['file']
                    newName = generate(64) + "." + file.filename.split(".")[-1]
                    with open(".\\static\\usersPictures\\" + newName, "wb") as f:
                        f.write(file.read())
                    user = db_sess.query(User).filter(User.id == getLocalUserData().id).first()
                    if user.picture != "guest.png":
                        os.remove(os.getcwd() + "\\static\\usersPictures\\" + user.picture)
                    user.picture = newName
            out = redirect(f"/account/{getLocalUserData().id}")

    else:
        data = request.args.get('move')
        if data:
            if data == "deleteAccount" and request.args.get('data').lower() == "да":
                if not getLocalUserData().banned:
                    user = db_sess.query(User).filter(User.id == getLocalUserData().id).first()
                    db_sess.delete(user)
                    out = make_response(redirect("/login"))
                    out.set_cookie("user", "", expires=0)
            elif data == "changeAbout":
                if not getLocalUserData().banned:
                    user = db_sess.query(User).filter(User.id == getLocalUserData().id).first()
                    user.about = request.args.get('data')
            elif data == "changeName":
                if not getLocalUserData().banned:
                    user = db_sess.query(User).filter(User.id == getLocalUserData().id).first()
                    user.name = request.args.get('data')
    db_sess.commit()
    db_sess.close()
    return out


def getLocalUserData():
    if request.cookies.get("user"):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.cookie == str(request.cookies.get("user"))).first()
        db_sess.close()
        if user:
            return user
    return guestUser()


def getUserById(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    db_sess.close()
    if user:
        return user
    else:
        return guestUser()


def getFilmById(id):
    db_sess = db_session.create_session()
    film = db_sess.query(Film).filter(Film.id == id).first()
    db_sess.close()
    return film


def getFilms(**args):
    db_sess = db_session.create_session()
    films = db_sess.query(Film).filter(**args)
    db_sess.close()
    return films


def accountRender(id):
    user = getUserById(id)
    localUser = getLocalUserData()
    data = {}
    if user.id == localUser.id or localUser.isAdmin: data
    if not user: return renderTemplate("account.html", showedUser="--None--", showedPicture="guest.png")
    return renderTemplate("account.html", showedUser=user.name, showedPicture=user.picture,
                          isAdmin="🔐" if user.isAdmin else "", showedId=user.id, about=user.about,
                          creationDate=user.creationDate.strftime('%H:%M %d/%m/%Y'),
                          ban="unbanAccount" if user.banned else "banAccount",
                          banSymbol="🔓" if user.banned else "🔒",
                          rating=str(round(user.ratingSum / user.ratingCount, 2)).ljust(4, "0"), **data)


def filmRender(id, **data):
    film = getFilmById(id)
    return renderTemplate("filmPage.html", title=film.title, showedPicture=film.picture, id=film.id,
                          description=film.description, publishedDate=film.date,
                          rating=str(round(film.sumRating / film.countRating, 2)).ljust(4, "0"), **data)


def renderTemplate(template_name_or_list, **args):
    user = getLocalUserData()
    if user.id == -1:
        data = """<li><a href="/login">Вход / Регистрация</a></li>"""
    else:
        data = f"""<li><a href="/films">Каталог фильмов</a></li>{'''<li><a href="/admin">Админ панель</a></li>''' if user.isAdmin else ""}"""
    return render_template(template_name_or_list, **args, user=user.name, picture=user.picture, pages=data)


def specialDial():
    user = getLocalUserData()


def generate(length):
    return "".join(choices(string.ascii_letters + string.digits, k=length))
