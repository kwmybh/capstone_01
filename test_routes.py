from werkzeug.utils import html
from models import User, Favorites, Recipe
from app import app, db
from unittest import TestCase

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['DEBUG'] = False

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///smart_recipe_db_test"
app.config['TESTING'] = True

db.drop_all()
db.create_all()

USER_DATA = {
    "username":"testuser",
    "pwd":"HASHED_PASSWORD"
}

class RouteTest(TestCase):
    def setUp(self):
        User.query.delete()
        Recipe.query.delete()
        Favorites.query.delete()

        u1 = User.register(**USER_DATA)
        r1= Recipe(name="r1",img="bla1",vid="bla11")
        f1= Favorites(user_id=u1.id,recipe_id=r1.id)
        db.session.add(u1)

        self.u1 = u1

    def test_register(self):
        with app.test_client() as client:
            res = client.post('/register', data = dict(
                                username = 'username',
                                email = 'test@mail.com',
                                pwd = 'password'),
                                follow_redirects = True
                                )
            
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<div class="pricing-header p-3 pb-md-4 mx-auto text-center">', html)


    def test_homepage(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)

            self.assertIn('<div class="pricing-header p-3 pb-md-4 mx-auto text-center">', html)


    # def test_login(self):
    #     with app.test_client() as client:
    #         response = self.client.post('/login', data = dict(
    #                             username = 'username',
    #                             pwd = 'password'),
    #                             follow_redirects = True
    #                             )
    #         self.assertIn(b'Start Here!')


    # def test_logout(self):
    #     with app.test_client() as client:
    #         self.client.post('/login', data = dict(
    #                                 username = 'username',
    #                                 pwd = 'password'),
    #                                 follow_redirects = True
    #                                 )
    #         res = self.client.get('/logout', follow_redirects = True)
    #         html = res.get_data(as_text = True)

    #         self.assertEqual(res.status_code, 200)
    #         self.assertEquals('<h3>Start Here!</h3>', html)
        
     
    #  test_register
    #  test_homepage
    #  test_logout
    #  test_favorites       