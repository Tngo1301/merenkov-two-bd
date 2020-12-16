# Для создания дополнительной базы данных
import sqlite3
from datetime import datetime
from hashlib import md5

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# Таблица - корзина покупок
class Basket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokypatel_name = db.Column(db.String(64), db.ForeignKey('user.username'))
    igra_name = db.Column(db.String(32), db.ForeignKey('post.name'))

    def create_buy(self):
        object = Basket(self.id, self.pokypatel_name, self.igra_name)
        return object


# Таблица пользователя
class User(UserMixin, db.Model):
    # поля
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # связь с постами пользователя
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # Для админа
    status = db.Column(db.String(32))

    # ---
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    balance = db.Column(db.Integer)  # ?

    # ---

    # работа с аватаркой в профиль
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # задаем хэш вместо пароля в таблицу
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # проверяем совпадает ли пароль пользователя, с параметром
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # купить игру
    def buy_game(self, post):
        if self.balance is None:
            return 0
        if post is None:
            return 0
        elif type(post.cost) != int:
            return 0
        elif int(post.cost) > self.balance:
            return 0
        else:
            self.balance -= int(post.cost)

    def get_admin(self):
        self.status = 'Admin'


# Таблица постов пользователя
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # ---
    name = db.Column(db.String(32), index=True, unique=True)
    janre = db.Column(db.String(64), index=True, unique=False)
    pegi = db.Column(db.String(4), index=True, unique=False)

    cost = db.Column(db.Integer)  # ?
    # ---

    # время написания этого поста (Будет годом выпуска)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # связь с табилцей пользователей ссылается на id из таблицы user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # работа с иконкой игры
    def avatar(self, size):
        conn = sqlite3.connect('sqlite.db')
        cursor = conn.cursor()
        if self.janre == 'rpg':
            cursor.execute("SELECT Hint from demo where Name = 'string_first'")

        elif self.janre == 'action':
            cursor.execute("SELECT Hint from demo where Name = 'string_second'")

        elif self.janre == 'strategy':
            cursor.execute("SELECT Hint from demo where Name = 'string_third'")

        link = "".join(str(cursor.fetchall()).split('\'')[1:-1])
        conn.close()
        return link.format(size)

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Model1(db.Model):
    __bind_key__ = 'my_sql2'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

# terminal
# flask db migrate -m "new fields in user model" - добавить новые поля в базы данных
# flask db upgrade - обновить бд
