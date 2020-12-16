from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Post
import collections


# форма логина
class LoginForm(FlaskForm):
    username = StringField('Введите логин', validators=[DataRequired()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    remember_me = BooleanField('Оставаться в системе')
    submit = SubmitField('Подтвердить')


# форма регистрации
class RegistrationForm(FlaskForm):
    # имя
    #тест в 4 лабе
    username = StringField('Логин', validators=[DataRequired(),Length(min=3, max=15)])
    #
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')

    # проверка уже наличия имени или почты в базе данных
    # Подтверждение имени
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Такое имя занято, используйте другое')

    # Подтверждение почты
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Эта почта уже занята, используйте другую')


# форма редактирования профиля
class EditProfileForm(FlaskForm):
    username = StringField('Новый логин пользователя', validators=[DataRequired(),Length(min=3, max=15)])
    about_me = TextAreaField('Расскажите о себе', validators=[Length(min=0, max=140)])
    submit = SubmitField('Подтвердить')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Такое имя занято, используйте другое.')


class AdminAddPostForm(FlaskForm):
    # имя
    def my_price_check(self, cost):
        if type(cost.data) is int:
            if int(cost.data) < 0:
                raise ValidationError('must be >0')

        if len(str(cost.data)) > 16:
            raise ValidationError('Not to much for u?')

    name = StringField('Название игры', validators=[DataRequired(), Length(min=3, max=15)])

    body = TextAreaField('Описание', validators=[Length(min=0, max=140)])

    janre = SelectField(label='Жанр', choices=[('action', 'Шутер'),
                                               ('rpg', 'Ролевая игра'),
                                               ('strategy', 'Стратегия')])
    pegi = SelectField(label='Возрастной рейтинг', choices=[('3+', '3+'),
                                                            ('7+', '7+'),
                                                            ('12+', '12+'),
                                                            ('16+', '16+'),
                                                            ('18+', '18+')])

    submit = SubmitField('Зарегестрировать игру')
    cost = IntegerField('Введите цену', validators=[my_price_check])

    # проверка уже наличия имени или почты в базе данных
    # Подтверждение имени
    def validate_name(self, name):
        post = Post.query.filter_by(name=name.data).first()
        if post is not None:
            raise ValidationError('Такое название игры уже занято, используйте другое')


# Отображение всех игр
class AdminShowDeleteForm(FlaskForm):
    name = StringField('Название игры', validators=[DataRequired(), Length(min=3, max=15)])
    submit = SubmitField('Удалить игру')



#  def validate_name(self, name):
#     post = Post.query.filter_by(name=name.data).first()
#    if post is None:
#       raise ValidationError('Пожалуйста, используйте другое название игры')


class AdminShowDeleteAll(FlaskForm):
    submit_all = SubmitField('Удалить все игры')


# Отображение всех пользователей
class AdminShowDelete_usersForm(FlaskForm):
    username = StringField('имя пользователя', validators=[DataRequired(), Length(min=3, max=15)])
    submit = SubmitField('Удалить пользователя')


#  def validate_name(self, name):
#     post = Post.query.filter_by(name=name.data).first()
#    if post is None:
#       raise ValidationError('Пожалуйста, используйте другое название игры')


class AdminShowDeleteAll_users(FlaskForm):
    submit_all = SubmitField('(Временно!)Удалить всех пользователей')


class AdminShowMoneyAdd_users(FlaskForm):


    username = StringField('имя пользователя', validators=[DataRequired()])
    money = IntegerField('Введите новый баланс', validators=[DataRequired()])
    submit_money = SubmitField('Изменить')

    def validate_money(self, money):
        if money is None or money == 0:
            raise ValidationError('Пожалуйста, используйте другое название игры')


class AddGameForm(FlaskForm):
    submit_1 = SubmitField('Добавить в библиотеку')


class BuyGameForm(FlaskForm):
    submit_2 = SubmitField('Купить и добавить в библиотеку')


class GetAdminForm(FlaskForm):
    admin_key = StringField('Введите ключ для получения прав администратора', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')
