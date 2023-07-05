from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
Apk = Flask(__name__)
Apk.secret_key = "1994Fragoso"

Apk.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = '1994Fragoso',
        servidor = 'localhost',
        database = 'Read'

    )

db = SQLAlchemy(Apk)

class players(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    nationality = db.Column(db.String(40), nullable=False)
    team = db.Column(db.String(50), nullable=False)
    tshirt = db.Column(db.String(3), nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name

class Users(db.Model):
    nickname = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name

"""
class players:
    def __init__(self, name, nationality, team, tshirt_number):
        self.name = name
        self.nationality = nationality
        self.team = team
        self.tshirt_number = tshirt_number

play1 = players("Cristiano Ronaldo", "Portugal", "Real Madrid", "7")
play2 = players("Leonel Messi", "Argentina", "Barcelona", "10")
play3 = players("Kyllian Mbape", "Franca", "PSG", "7")
list = [play1, play2, play3]

class Users:
    def __init__(self, name, nickname, password):
        self.name = name
        self.nickname = nickname
        self.password = password

us1 = Users("Antonio Fragoso", "Witness", "1994")
us2 = Users("Helder Fragoso", "Helder", "1996")
us3 = Users("Alvis Haal", "Alvis", "2023")
list1 = {us1.nickname: us1,
          us2.nickname: us2,
          us3.nickname: us3}
"""

@Apk.route("/")
def index():
    list = players.query.order_by(players.id)
    return render_template("lista2.html", site = "Fifa unoficial", topword = "The Best Players Of World", change = list)

@Apk.route("/new")
def new():
    if 'logged_in_user' not in session or session['logged_in_user'] == None:
        return redirect(url_for('login', next = url_for('new')))
    return render_template("novo2.html", site = "Fifa unoficial", topword = "Register New Player")

@Apk.route('/create', methods = ['POST'],)
def create():
    name = request.form['name']
    nationality = request.form['nationality']
    team = request.form['team']
    tshirt = request.form['tshirt']
    player = players.query.filter_by(name=name).first()
    if player:
        flash('player already exists')
        return redirect(url_for('index'))
    new_player = players(name=name, nationality=nationality, team=team, tshirt=tshirt)
    db.session.add(new_player)
    db.session.commit()
    return redirect(url_for('index'))

@Apk.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login2.html', next = next, site = "Fifa unoficial")


@Apk.route('/authenticate', methods = ['POST'],)
def authenticate():
    user = Users.query.filter_by(nickname=request.form['user']).first()
    if user:
        if request.form['password'] == user.password:
            session['logged_in_user'] = user.nickname
            #flash(user.nickname + ' logged sucessful')
            next_page = request.form['next']
            return redirect(url_for('index'))
    else:
        flash('user not logged')
        return redirect(url_for('login'))

@Apk.route('/logout')
def logout():
    session['logged_in_user'] = None
    flash('logout sucessful')
    return redirect(url_for('login'))


Apk.run(host="0.0.0.0", port="8080", debug=True)