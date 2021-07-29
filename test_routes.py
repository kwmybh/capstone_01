from flask import Flask, redirect, render_template, request, url_for, session 

from unittest import TestCase
from app import app, db
import pytest

from models import User, Favorites, Recipe

class Module_Test(TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///smart_recipe_db_test"
        app.config['TESTING'] = True
        db.drop_all()
        db.create_all()     

        self.app = app.test_client()

    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, name, pwd):

        data = dict(
            name = name,
            pwd = pwd
        )
        return self.app.post('/login', data=data, follow_redirects = True)

    
    def register(self, name, pwd):
        data = dict(
            name = name,
            pwd = pwd
        )
        return self.app.post('/register', data=data, follow_redirects=True)


    def test_logout(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 'userid'
            res = sess.get('/logout', follow_redirects=True)
                      
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/')

    
    def test_login(self):
        result = self.app.get('/login', follow_redirects = True)
        self.assertTrue(b'<h1 class="display-4">Log In</h1>' in result.data)
        


    def test_login_not_in(self):

        data = dict(
            name='adasd',
            pwd='sadgase'
        )

        result = self.app.post('/login', data=data, follow_redirects=True)
        self.assertTrue(b'<h1 class="display-4">Log In</h1>' in result.data)
        

    def test_login_success(self):
        self.register(
            'name',
           'password',
            )

        data =dict(
            name='name',
            pwd='password'
        )

        result = self.app.post('/login', data=data, follow_redirects=True)
        self.assertTrue(b'<h1 class="display-4">Log In</h1>' in result.data)
        

    
    def test_register(self):
        result = self.app.get('/register', follow_redirects=True)
        self.assertTrue(b'<h1 class="display-4">Register</h1>' in result.data)
	
    
    def test_register_account_already_exists(self):
        self.register(
            'name',
            'password'
            )

        data=dict(
            name = 'name',
            email = 'fakemail@mail.com',
            pwd = 'password'
            )

        result = self.app.post('/register', data=data, follow_redirects=True)
        self.assertTrue(b'<h1 class="display-4">Register</h1>' in result.data)


    # def test_logout(self):
    #     test