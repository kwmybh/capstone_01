from pdb import set_trace
from app import app, db, User

from unittest import TestCase

class SmartRecipeTest(TestCase):
    def test_register_form(self):
        with app.test_client() as client:
            res=client.get('/')
            html=res.get_data(as_text=True)

            self.assertEqual(res.status_code,200)
            self.assertIn('<h1 class="display-4 fw-normal">Smart Recipe</h1>', html)
    
class UserTest(TestCase):
   def setUp(self):
       self.app = app
       self.client = self.app.test_client()
       self._ctx = self.app.test_request_context()
       self._ctx.push()

       db.create_all()

   def tearDown(self):
       if self._ctx is not None:
           self._ctx.pop()

       db.session.remove()
       db.drop_all()

   def test_user_authentication():
       # (the test case is within a test request context)
       user = User(active=True)
       db.session.add(user)
       db.session.commit()
       login_user(user)

       # current_user here is the user
       print(current_user)

       # current_user within this request is an anonymous user
       r = test_client.get('/user')