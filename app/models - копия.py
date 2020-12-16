from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db,login
from flask_login import UserMixin
from hashlib import md5

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


#Таблица - корзина покупок
Basket = db.Table('Basket',
    db.Column('pokypatel_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('igra_id', db.Integer, db.ForeignKey('post.id'))
)
# Таблица пользователя
class User(UserMixin,db.Model):
    # поля
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # связь с постами пользователя
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    #---
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    balance = db.Column(db.Integer) #?
    #---
    igra = db.relationship(
        'User', secondary=Basket,
        primaryjoin=(Basket.c.pokypatel_id == id),
        secondaryjoin=(Basket.c.igra_id == posts.id),
        backref=db.backref('Basket', lazy='dynamic'), lazy='dynamic')
    #работа с аватаркой в профиль
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

    #Если админ
    #####
    def follow(self, post):
        #if not self.is_following(post):
            self.igra.append(post)

    def unfollow(self, post):
        #if self.is_following(post):
            self.basket.remove(post)

    #def is_following(self, post):
       # return self.basket.filter(
         #   Basket.c.igra_id == post.id).count() > 0
    ###
    #def followed_posts(self):
     #   return Post.query.join(
      #      Basket, (Basket.c.igra_id == Post.user_id)).filter(
       #     Basket.c.pokypatel_id == self.id).order_by(
        #    Post.timestamp.desc())

# Таблица постов пользователя
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    #---
    name = db.Column(db.String(32), index=True, unique=True)
    janre = db.Column(db.String(64), index=True, unique=False)
    pegi = db.Column(db.String(4), index=True, unique=False)

    cost = db.Column(db.Integer) #?
    #---

    # время написания этого поста (Будет годом выпуска)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # связь с табилцей пользователей ссылается на id из таблицы user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    basket = db.relationship(
        'Post', secondary=Basket,
        secondaryjoin=(Basket.c.igra_id == id),
        backref=db.backref('Basket', lazy='dynamic'), lazy='dynamic')

    # работа с иконкой игры
    def avatar(self, size):
        if self.janre == 'rpg':
            digest = md5(self.email.lower().encode('utf-8')).hexdigest()
            return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
                digest, size)



    def __repr__(self):
        return '<Post {}>'.format(self.body)


# terminal
#flask db migrate -m "new fields in user model" - добавить новые поля в базы данных
#flask db upgrade - обновить бд