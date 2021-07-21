"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_favorites_model.py


import os
from unittest import TestCase

from models import db, User, Favorites, Recipe
from sqlalchemy.exc import IntegrityError


# set an environmental variable
# to use a different database for tests (do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///smart_recipe_test"

# Now we can import app

from app import app, favorites_post

# Create tables (do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# TODO: make a firle _test_util.py and store user data and message data there
USER_DATA = {
    "email":"test@test.com",
    "username":"testuser",
    "password":"HASHED_PASSWORD"
}



class FavoritesModelTestCase(TestCase):
    """ Tests for message model """

    def setUp(self):
        """ create test client """

        User.query.delete()
        Favorites.query.delete()
        Recipe.query.delete()
        
        self.client = app.test_client()

        user = User(**USER_DATA)

        db.session.add(user)
        db.session.commit()
        # TODO: again, store user_id not user instance
        self.user = user

        favorites_data = {
            "user_id":self.user.id,
            "text":"test"
        }

        favorites = Favorites(**favorites_data)
        db.session.add(favorites)
        db.session.commit()

        self.favorites = favorites
        
    def tearDown(self):
        """ Clean up fouled transactions """

        db.session.rollback()

