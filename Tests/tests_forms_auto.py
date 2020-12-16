import unittest
from app import app, db
from app.models import User

from parameterized import parameterized


class RegisterFormsTests(unittest.TestCase):

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

    # help_method register
    def register(self, username, email, password):
        return self.app.post(
            '/register',
            data=dict(username=username, email=email, password=password),
            follow_redirects=True
        )

    # неверные
    @parameterized.expand([
        ["first_gran", "a" * 2],
        ["last_gran", "a" * 16],
        ["first_ekv", "a" * 1],
        ["last_ekv", "a" * 5000],
    ])
    def test_znach_username_not_correct_data_error(self, name, bad_string):
        response3 = self.register(bad_string, 'patkennedaay80@mail.com', 'password')
        self.assertIn(b'[Field must be between 3 and 15 characters long.]', response3.data)

    def test_znach_username_not_correct_data(self):
        response3 = self.register("",'patkennedaay80@mail.com', 'password')
        self.assertIn(b'[This field is required.]', response3.data)
    # верные
    @parameterized.expand([
        ["first_gran", "a" * 3],
        ["last_gran", "a" * 15],
        ["first_ekv", "a" * 5],
        ["last_ekv", "a" * 13],
    ])
    # Граничные верные
    def test_znach_username_correct_data_not_error(self, name, bad_string):
        response3 = self.register(bad_string, 'patkennedaay80@mail.com', 'password')
        self.assertNotIn(b'[Field must be between 3 and 15 characters long.]', response3.data)


class EditProfileFormsTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['LOGIN_DISABLED'] = False

        self.app = app.test_client()

        app.login_manager.init_app(app)

        db.drop_all()
        db.create_all()
        self.client = User(username='TestGuy', email='testMail@gmail.com')
        self.client.set_password('1234')
        db.session.add(self.client)
        db.session.commit()
        self.login(username='TestGuy', password='1234')
        # Disable sending emails during unit testing
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    def login(self, username, password):
        return self.app.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True)

    # help_method edit_profile
    def edit_profile(self, username):
        return self.app.post(
            '/edit_profile',
            data=dict(username=username, about_me="none"),
            follow_redirects=True
        )

    # help_method edit_profile
    def edit_profile_about_me(self, about_me):
        return self.app.post(
            '/edit_profile',
            data=dict(username='none', about_me=about_me),
            follow_redirects=True
        )

    # неверные
    @parameterized.expand([
        ["first_gran", "a" * 2],
        ["last_gran", "a" * 16],
        ["first_ekv", "a" * 1],
        ["last_ekv", "a" * 5000]
    ])
    def test_firsts_gran_znach_username_not_correct_data_error(self, name, bad_string):
        response3 = self.edit_profile(bad_string)
        self.assertIn(b'[Field must be between 3 and 15 characters long.]', response3.data)

    def test_znach_username_not_correct_data(self):
        response3 = self.edit_profile("")
        self.assertIn(b'[This field is required.]', response3.data)
    # верные
    @parameterized.expand([
        ["first_gran", "a" * 3],
        ["last_gran", "a" * 15],
        ["first_ekv", "a" * 5],
        ["last_ekv", "a" * 13]
    ])
    def test_firsts_gran_znach_username_correct_data_error(self, name, bad_string):
        response3 = self.edit_profile(bad_string)
        self.assertNotIn(b'[Field must be between 3 and 15 characters long.]', response3.data)

   # неверные
    @parameterized.expand([
        ["first_gran", "a" * 141],
        ["last_gran", "a" * 5000]
    ])
    def test_lasts_gran_znach_about_me_not_correct_data_error(self,name,bad_string):
        response3 = self.edit_profile_about_me(bad_string)
        self.assertIn(b'[Field must be between 0 and 140 characters long.]', response3.data)


    # верные
    @parameterized.expand([
        ["first_gran", "a" * 140],
        ["last_gran", "a" * 100],
        ["last_gran", "a" * 25],
        ["last_gran", "a" * 1]
    ])
    def test_firsts_gran_znach_about_me_correct_data_error(self,name,bad_string):
        response3 = self.edit_profile_about_me(bad_string)
        self.assertNotIn(b'[Field must be between 0 and 140 characters long.]', response3.data)


class AdminAddPostForm(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['LOGIN_DISABLED'] = False

        self.app = app.test_client()

        app.login_manager.init_app(app)

        db.drop_all()
        db.create_all()
        self.client = User(username='TestGuy', email='testMail@gmail.com', status='Admin')
        self.client.set_password('1234')
        db.session.add(self.client)
        db.session.commit()
        self.login(username='TestGuy', password='1234')
        # Disable sending emails during unit testing
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    def login(self, username, password):
        return self.app.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True)

    # help_method create_post
    def create_post(self, name):
        return self.app.post(
            '/admin_create_post',
            data=dict(name=name, body='none'),
            follow_redirects=True
        )

    # help_method create_post
    def create_post_body(self, body):
        return self.app.post(
            '/admin_create_post',
            data=dict(name='none', body=body),
            follow_redirects=True
        )

        # неверные

    @parameterized.expand([
        ["first_gran", "a" * 2],
        ["last_gran", "a" * 16],
        ["first_ekv", "a" * 1],
        ["last_ekv", "a" * 5000]
    ])
    def test_firsts_gran_znach_username_not_correct_data_error(self, name, bad_string):
        response3 = self.create_post(bad_string)
        self.assertIn(b'[Field must be between 3 and 15 characters long.]', response3.data)

    def test_znach_username_not_correct_data_(self):
        response3 = self.create_post("")
        self.assertIn(b'[This field is required.]', response3.data)
    # верные
    @parameterized.expand([
        ["first_gran", "a" * 3],
        ["last_gran", "a" * 15],
        ["first_ekv", "a" * 5],
        ["last_ekv", "a" * 13]
    ])
    def test_firsts_gran_znach_username_correct_data_error(self, name, bad_string):
        response3 = self.create_post(bad_string)
        self.assertNotIn(b'[Field must be between 3 and 15 characters long.]', response3.data)

    # неверные
    @parameterized.expand([
        ["first_gran", "a" * 141],
        ["last_gran", "a" * 5000]
    ])
    def test_lasts_gran_znach_about_me_not_correct_data_error(self, name, bad_string):
        response3 = self.create_post_body(bad_string)
        self.assertIn(b'[Field must be between 0 and 140 characters long.]', response3.data)

    # верные
    @parameterized.expand([
        ["first_gran", "a" * 140],
        ["last_gran", "a" * 100],
        ["last_gran", "a" * 25],
        ["last_gran", "a" * 1]
    ])
    def test_firsts_gran_znach_about_me_correct_data_error(self, name, bad_string):
        response3 = self.create_post_body(bad_string)
        self.assertNotIn(b'[Field must be between 0 and 140 characters long.]', response3.data)


class AdminShowDeleteForm(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['LOGIN_DISABLED'] = False

        self.app = app.test_client()

        app.login_manager.init_app(app)

        db.drop_all()
        db.create_all()
        self.client = User(username='TestGuy', email='testMail@gmail.com', status='Admin')
        self.client.set_password('1234')
        db.session.add(self.client)
        db.session.commit()
        self.login(username='TestGuy', password='1234')
        # Disable sending emails during unit testing
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    def login(self, username, password):
        return self.app.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True)

    # help_method create_post
    def create_post(self, name):
        return self.app.post(
            '/admin_show_posts',
            data=dict(name=name),
            follow_redirects=True
        )


 # неверные
    @parameterized.expand([
        ["first_gran", "a"*2 ],
        ["last_gran", "a" * 16],
        ["first_ekv", "a" * 1],
        ["last_ekv", "a" * 5000],
    ])
    def test_znach_username_not_correct_data_error(self, name, bad_string):
        response3 = self.create_post(bad_string)
        self.assertIn(b'[Field must be between 3 and 15 characters long.]', response3.data)

    def test_znach_username_not_correct_data_(self):
        response3 = self.create_post("")
        self.assertIn(b'[This field is required.]', response3.data)
    # верные
    @parameterized.expand([
        ["first_gran", "a" ],
        ["last_gran", "a" * 15],
        ["first_ekv", "a" * 5],
        ["last_ekv", "a" * 13],
    ])
    # Граничные верные
    def test_znach_username_correct_data_not_error(self, name, bad_string):
        response3 = self.create_post(bad_string)
        self.assertNotIn(b'[Field must be between 3 and 15 characters long.]', response3.data)




class AdminShowUsersForm(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['LOGIN_DISABLED'] = False

        self.app = app.test_client()

        app.login_manager.init_app(app)

        db.drop_all()
        db.create_all()
        self.client = User(username='TestGuy', email='testMail@gmail.com', status='Admin')
        self.client.set_password('1234')
        db.session.add(self.client)
        db.session.commit()
        self.login(username='TestGuy', password='1234')
        # Disable sending emails during unit testing
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    def login(self, username, password):
        return self.app.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True)

    # help_method create_post
    def show_users(self, username):
        return self.app.post(
            '/admin_show_users',
            data=dict(username=username),
            follow_redirects=True
        )

        # неверные
    @parameterized.expand([
        ["first_gran", "a" ],
        ["last_gran", "a" * 16],
        ["first_ekv", "a" * 1],
        ["last_ekv", "a" * 5000],
    ])
    def test_znach_username_not_correct_data_error(self, name, bad_string):
        response3 = self.show_users(bad_string)
        self.assertIn(b'[Field must be between 3 and 15 characters long.]', response3.data)

    def test_znach_username_not_correct_data_(self):
        response3 = self.show_users("")
        self.assertIn(b'[This field is required.]', response3.data)
    # верные
    @parameterized.expand([
        ["first_gran", "a" * 3],
        ["last_gran", "a" * 15],
        ["first_ekv", "a" * 5],
        ["last_ekv", "a" * 13],
    ])
    def test_znach_username_correct_data_not_error(self, name, bad_string):
        response3 = self.show_users(bad_string)
        self.assertNotIn(b'[Field must be between 3 and 15 characters long.]', response3.data)


if __name__ == '__main__':
    unittest.main(verbosity=4)
