from flask import Flask, redirect, render_template, request, url_for, session 

from unittest import TestCase
from app import app, db
import pytest

from models import User, Favorites, Recipe

USER_DATA = {
    "username":"name",
    "pwd":"password"
}

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:H%40L!M@localhost:5432/smart_recipe_db_test"
#app.config['TESTING'] = True
db.drop_all()
db.create_all()     

class Module_Test(TestCase):
    def setUp(self):
        
        User.query.delete()
        Recipe.query.delete()
        Favorites.query.delete()

        self.app = app.test_client()
        
        u1= User.register(**USER_DATA)
        r1= Recipe(name="r1",img="bla1",vid="bla11")
        r2= Recipe(name="r2",img="bla2",vid="bla22")
        u1.recipe.append(r1)
        db.session.add(u1)
        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()
    
        self.u1=u1
        self.r1=r1
        self.r2=r2
    
    def tearDown(self):
        db.session.rollback()

    #def login(self, name, pwd):

    #    data = dict(
    #        name = name,
    #        pwd = pwd
    #    )
    #    return self.app.post('/login', data=data, follow_redirects = True)

    #
    #def register(self, name, pwd):
    #    data = dict(
    #        name = name,
    #        pwd = pwd
    #    )
    #    return self.app.post('/register', data=data, follow_redirects=True)


    def test_logout(self):
        with self.app as c:    
            with c.session_transaction() as sess:
                sess['user_id'] = 'userid'

        res = c.get('/logout', follow_redirects=True)
                      
        html = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('Sign up', html)

    
    def test_login(self):
        result = self.app.get('/login', follow_redirects = True)
        html = result.get_data(as_text=True)

        self.assertIn('<h1 class="display-4">Log In</h1>', html)
        


    def test_login_not_in(self):

        data = dict(
            name='adasd',
            pwd='sadgase'
        )

        result = self.app.post('/login', data=data, follow_redirects=True)
        html = result.get_data(as_text=True)
        self.assertIn('Log In', html)
        

    def test_login_success(self):

        data =dict(
            name='name',
            pwd='password'
        )
        with self.app as c:    
            with c.session_transaction() as sess:
                sess["user_id"]=self.u1.id
            result = c.get('/homepage', follow_redirects=True)
            html = result.get_data(as_text=True)
            self.assertIn('<h2 class="title">Your Search Results:</h2>', html)
        

    
    def test_register(self):
        result = self.app.get('/register', follow_redirects=True)
        html = result.get_data(as_text=True)
        self.assertIn('<h1 class="display-4">Register</h1>', html)
	
    
    def test_register_account_already_exists(self):


        data=dict(
            name = 'name',
            pwd = 'password'
            )

        result = self.app.post('/register', data=data, follow_redirects=True)
        html = result.get_data(as_text=True)
        self.assertIn('Register', html)

    def test_adding_to_favorites_existing_recipe(self):
        with self.app as c:
            data=dict(mealName=self.r2.name,mealImg=self.r2.img,mealVid=self.r2.vid)
            with c.session_transaction() as sess:
                sess['user_id'] = self.u1.id

            # once this is reached the session was stored
            result = c.post('/favorites',data=data, follow_redirects=True)
            html = result.get_data(as_text=True)
            u1_recipe=User.query.get_or_404(sess['user_id']).recipe
            r2=Recipe.query.get_or_404(self.r2.id)

            self.assertTrue(r2 in u1_recipe)

    def test_adding_to_favorites_non_existing_recipe(self):
        with self.app as c:    
            data=dict(mealName="r3",mealImg="r3img",mealVid="r3vid")
            with c.session_transaction() as sess:
                sess['user_id'] = self.u1.id

            # once this is reached the session was stored
            result = c.post('/favorites',data=data, follow_redirects=True)
            html = result.get_data(as_text=True)

            u1_recipe=User.query.get_or_404(sess['user_id']).recipe
            self.assertTrue(Recipe.query.filter_by(name = "r3").first().name == 'r3')

            r3=Recipe.query.filter_by(name = "r3").first()
            self.assertTrue(r3 in u1_recipe)

    def test_adding_to_favorites_already_favorited_recipe(self):
        with self.app as c:    
            data=dict(mealName=self.r1.name,mealImg=self.r1.img,mealVid=self.r1.vid)
            u1_recipe_old=self.u1.recipe
            with c.session_transaction() as sess:
                sess['user_id'] = self.u1.id

            # once this is reached the session was stored
            result = c.post('/favorites',data=data, follow_redirects=True)
            html = result.get_data(as_text=True)

            u1_recipe=User.query.get_or_404(sess['user_id']).recipe
            self.assertEqual(u1_recipe[0].id,u1_recipe_old[0].id)
    
    # def test_favorite_add(self):
