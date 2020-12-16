from datetime import datetime, timedelta
import unittest
from app import app, db
import os, tempfile
from app.models import User, Post, Basket



class UserModelCaseTest(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_check_hashing_susan_not_dog(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))

    def test_password_check_hashing_susan_is_cat(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertTrue(u.check_password('cat'))


    def test_avatar_email_picture_is_user_picture(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_buy_game_balance_is_minus(self):
        # Не связаные
        u1 = User(username='valera', balance=40)
        p1 = Post(cost=20, name='ds')
        expRes = u1.balance - p1.cost
        u1.buy_game(p1)

        self.assertEqual(u1.balance, expRes)

    def test_create_buy_busket_is_not_empty(self):
        u1 = User(username='clown', balance=70)
        p1 = Post(id=1, cost=30, name='warik')
        b1 = Basket(pokypatel_name=u1.username, igra_name=p1.name)
        #b1.create_buy()
        db.session.add(b1)
        self.assertTrue(b1)

    def test_get_admin_user_is_admin(self):
        u1 = User(username='john')
        u1.get_admin()
        expRes = 'Admin'
        self.assertEqual(u1.status, expRes)



class GameModelCaseTest(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar_email_picture_is_post_picture(self):
        p1 = Post(name='ds1', janre='action')

        self.assertEqual(p1.avatar(64), ('https://ru.gravatar.com/userimage/174123252/'
                                         'c82f8fcfee46926a9ce4a54af616a99c.png?size=64'))

    def test_add_all_list_of_posts_lenght(self):
        p1 = Post(name='ds', janre='action')
        p2 = Post(name='ds2', pegi='18+')
        p3 = Post(name='ds3', body='diferent_text')
        p4 = Post(name='ds4')

        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        self.assertEqual(len(Post.query.all()),4)


class dbCaseTest(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_get_empty_url_is_none(self):
        rv = self.app.get('/')
        assert b'' in rv.data

    def test_post_url_add_is_text(self):
        rv = self.app.post('/add', data=dict(
            title=b'ds1',
            text=b'text'
        ), follow_redirects=True)
        assert b'text' in rv.data


class RoutesTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        # Disable sending emails during unit testing
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    def test_get_is_get_response(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    #help_method
    def register(self, username, email, password):
        return self.app.post(
            '/register',
            data=dict(username=username, email=email, password=password),
            follow_redirects=True
        )
    #help_method
    def login(self, username, password):
        return self.app.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True)
    #help_method
    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

    def test_check_mail_bad_url_error(self):

        response3 = self.register('name2', 'patkennedaay80@', 'password')

        self.assertIn(b'[Invalid email address.]', response3.data)

    def test_check_password_bad_password_error(self):
        response1 = self.login('name6', 'password1')
        self.assertIn(b'bad name or password', response1.data)



if __name__ == '__main__':
    unittest.main(verbosity=3)
