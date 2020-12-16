from app import app, db
from flask import render_template, flash, redirect, url_for, request
#
from app.config import Config
from flask_admin import Admin, BaseView, expose
#

# Запоминание времени последнего посещения пользователем сайта
from datetime import datetime
from app.forms_folder.forms import LoginForm, RegistrationForm, EditProfileForm, AdminAddPostForm, AdminShowDeleteForm, \
    AdminShowDeleteAll, AdminShowDelete_usersForm, AdminShowDeleteAll_users, AdminShowMoneyAdd_users, AddGameForm, \
    BuyGameForm, \
    GetAdminForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Basket
from werkzeug.urls import url_parse


# url_for(идет по названию функции в этом файле)


# testing homepage

@app.route('/')
@app.route('/homePage', methods=['GET', 'POST'])
def homePage():
    posts = Post.query.all()
    return render_template('base.html',
                           title='homePage',
                           posts=posts)


# Аутентификация
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Если пользователь уже зарегистрирован
    if current_user.is_authenticated:
        # перенаправление ----------------------!
        return redirect(url_for('index'))
    # В ином случае
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data).first()  # метод first возвращает 1 результат если найдет такой,
        # all возвращает все

        if user is None or not user.check_password(form.password.data):
            flash('bad name or password')
            return redirect(url_for('login'))

        # Эта функция будет регистрировать пользователя во время входа в систему,
        # поэтому это означает, что на любых будущих страницах, к которым пользователь переходит,
        # будет установлена ​​переменная current_user для этого пользователя
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        # return redirect('/index') # если всё выше чики брики, перекинет на страницу /index
        return redirect(next_page)
    # сама форма страницы логина
    return render_template('login.html', title='Sign In', form=form)


# testing index
@app.route('/index')
@login_required  # требуется авторизация чтобы зайти на эту страницу
def index():
    return render_template("index.html", title='Home Page')


@app.route('/admin_help')
@login_required  # требуется авторизация чтобы зайти на эту страницу
def admin_help():
    return render_template("admin_help.html", title='Home Page')


@app.route('/add_to_balance')
@login_required  # требуется авторизация чтобы зайти на эту страницу
def add_to_balance():
    return render_template("add_to_balance.html", title='wallet control')


# testing new index
@app.route('/newIndex')
@login_required
def newIndex():
    return render_template('new_index.html', title='Home')


@app.route('/get_admin', methods=['GET', 'POST'])
@login_required
def get_admin():
    if current_user.status == 'Admin':
        return redirect(url_for('homePage'))
    else:
        form = GetAdminForm()
        if form.submit.data:
            input_key = form.admin_key.data
            # you-will-never-guess
            if input_key == str(Config.SECRET_KEY):
                current_user.status = 'Admin'
                db.session.commit()
                flash("Права администратора успешно получены")
                return redirect(url_for('homePage'))

            else:
                flash("Неправильный введенный код")
    return render_template('get_admin.html', title='Home', form=form)


# регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Если пользователь уже под логином
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # В ином случае регистрирю его
    form = RegistrationForm()
    if form.validate_on_submit():
        # Получение из формы
        name = form.username.data
        mail = form.email.data
        # создаю обьект
        user = User(username=name, email=mail, balance=0, status='User')
        user.set_password(form.password.data)  # задаю пароль( а именно хеш)
        # доавляю в базу данных
        db.session.add(user)
        # комичу
        db.session.commit()
        flash('Спасибо за регистрацию!')
        # перенаправляю
        return redirect(url_for('login'))
    # сам вид формы
    return render_template('register.html', title='Register', form=form)


# Выход из аккаунта
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# Страница игры
@app.route('/gamePage/<name>', methods=['GET', 'POST'])
def gamePage(name):
    # Если страница не найдена вернет ошибку 404
    post = Post.query.filter_by(name=name).first_or_404()
    form = AddGameForm()  # форма бесплатного добавления игры в библиотеку
    form2 = BuyGameForm()  # форма покупки игры

    if form.submit_1.data:
        if Basket.query.filter_by(igra_name=name, pokypatel_name=current_user.username).first():
            flash("эта игра уже есть в библиотеке")
        else:
            b1 = Basket(pokypatel_name=current_user.username, igra_name=name)
            db.session.add(b1)
            db.session.commit()
            return redirect(url_for('newIndex'))

    elif form2.submit_2.data:
        if Basket.query.filter_by(igra_name=name, pokypatel_name=current_user.username).first():
            flash("Вы уже купили эту игру")

        else:
            post = Post.query.filter_by(name=name).first()
            current_user.balance = int(current_user.balance)
            if int(post.cost) > current_user.balance:
                flash("У вас недостаточно средств на счете")
            else:
                current_user.balance -= int(post.cost)
                b1 = Basket(pokypatel_name=current_user.username, igra_name=name)
                db.session.add(b1)
                db.session.commit()
                return redirect(url_for('newIndex'))

    return render_template('gamePage.html', post=post, name=name, form=form, form2=form2)


# Страница пользователя
@app.route('/user/<username>')
@login_required
def user(username):
    # Если страница не найдена вернет ошибку 404
    user = User.query.filter_by(username=username).first_or_404()
    posts = []
    # Его купленные игры(пока пустышка)
    baskets = Basket.query.filter_by(pokypatel_name=username).all()
    for basket in baskets:
        posts.append(Post.query.filter_by(name=basket.igra_name).first())
    return render_template('user.html', user=user, posts=posts)


# редактирование профиля
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Ваши изменения были сохранены.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Редактировать профиль',
                           form=form)




@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


# Добавление админом игры в базу данных
@app.route('/admin_create_post', methods=['GET', 'POST'])
@login_required
def admin_create_post():
    janres = ['rpg', 'action']
    if current_user.status == 'Admin':
        # В ином случае регистрирю его
        form = AdminAddPostForm()
        if form.validate_on_submit():
            # Получение из формы
            name = form.name.data
            body = form.body.data
            pegi = form.pegi.data
            janre = form.janre.data
            cost = form.cost.data
            # создаю обьект
            post = Post(name=name, body=body, pegi=pegi, janre=janre, cost=cost)
            # доавляю в базу данных
            db.session.add(post)
            # комичу
            db.session.commit()
            flash("игра {} успешно зарегстрирована".format(name))
            # перенаправляю
            return redirect(url_for('admin_show_posts'))
    else:
        return redirect(url_for('admin_help'))
    # сам вид формы
    return render_template('admin_create_post.html', title='creating_post', form=form, janres=janres)


# Страница просмотра всех зарестрированных  игр в базе данных,
#   также удаление
@app.route('/admin_show_posts', methods=['GET', 'POST'])
@login_required
def admin_show_posts():
    if current_user.status == 'Admin':
        # Если страница не найдена вернет ошибку 404
        # Его купленные игры
        form = AdminShowDeleteForm()
        form2 = AdminShowDeleteAll()
        posts = Post.query.all()
        #  было form.submit.data:
        if form.validate_on_submit()and form.submit.data:
            name = form.name.data
            if not Post.query.filter_by(name=name).first():
                flash("Игры {} нет".format(name))
            else:
                flash("игра {} успешно удалена".format(name))
                Post.query.filter_by(name=name).delete()
                Basket.query.filter_by(igra_name=name).delete()
                db.session.commit()
            return redirect(url_for('admin_show_posts'))

        if form2.submit_all.data:
            if not Post.query.all():
                flash("Игр нет")
            else:
                flash("Все игры удалены")
                Post.query.delete()
                Basket.query.delete()
                db.session.commit()
                return redirect(url_for('admin_show_posts'))
    else:
        return redirect(url_for('admin_help'))
    return render_template('admin_show_posts.html', user=user, posts=posts, form=form, form2=form2,
                           lenght=len(Post.query.all()))


# Страница просмотра всех зарегистрированных  игр в базе данных,
#   также удаление
@app.route('/admin_show_users', methods=['GET', 'POST'])
@login_required
def admin_show_users():
    if current_user.status == 'Admin':
        # Если страница не найдена вернет ошибку 404
        # Его купленные игры
        form1 = AdminShowDelete_usersForm()
        form2 = AdminShowDeleteAll_users()
        form3 = AdminShowMoneyAdd_users()
        users = User.query.all()
        username = form1.username.data

        # было form1.submit.data
        if form1.validate_on_submit() and form1.submit.data:
            if not User.query.filter_by(username=username).first():

                flash("Такого пользователя не существует")
            else:
                flash("Пользователь {} успешно удален".format(username))

                User.query.filter_by(username=username).delete()
                db.session.commit()
                return redirect(url_for('admin_show_users'))

        elif form2.submit_all.data:
            flash("Все пользователи успешно удалены")
            User.query.delete()
            db.session.commit()
            return redirect(url_for('admin_show_users'))

        elif form3.submit_money.data:
            username = form3.username.data
            balance_new = form3.money.data
            if not User.query.filter_by(username=username).first():
                flash("Такого пользователя не существует")
            else:
                if type(balance_new) is not int:
                    flash('Введенная сумма не корректна, должно быть число')
                elif int(balance_new) < 0:
                    flash('Сумма должна быть >0')
                elif len(str(balance_new)) > 16:
                    flash('Введена слишком большая сумма?')

                else:
                    u = User.query.filter_by(username=username).first()
                    balance_old= u.balance
                    if u.balance is None:
                        balance_old = 0
                    flash("у пользователя {} сумма {} была изменена на {}".format(u.username, balance_old, balance_new))
                    User.query.filter_by(username=username).update(dict(balance=balance_new))
                    db.session.commit()
                    return redirect(url_for('admin_show_users'))

    else:
        return redirect(url_for('admin_help'))

    return render_template('admin_show_users.html', user=user, users=users, form=form1, form2=form2, form3=form3,
                           lenght=len(User.query.all()))

