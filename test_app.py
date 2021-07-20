from pdb import set_trace
from app import app 
from unittest import TestCase

class SmartRecipeTest(TestCase):
    def test_register_form(self):
        with app.test_client() as client:
            res=client.get('/')
            html=res.get_data(as_text=True)

            self.assertEqual(res.status_code,200)
            self.assertIn('<h1 class="display-4 fw-normal">Smart Recipe</h1>', html)