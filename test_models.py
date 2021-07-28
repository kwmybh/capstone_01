from models import User, Favorites, Recipe
from app import app, db
from unittest import TestCase

# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:H%40L!M@localhost:5432/smart_recipe_db_test"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///smart_recipe_db_test"
app.config['TESTING'] = True
db.drop_all()
db.create_all()

USER_DATA = {
    "username":"testuser",
    "pwd":"HASHED_PASSWORD"
}

class ModelTest(TestCase):
    def setUp(self):
        User.query.delete()
        Recipe.query.delete()
        Favorites.query.delete()

        u1= User.register(**USER_DATA)
        r1= Recipe(name="r1",img="bla1",vid="bla11")
        r2= Recipe(name="r2",img="bla2",vid="bla22")
        f1= Favorites(user_id=u1.id,recipe_id=r1.id)

        db.session.add(u1)
        db.session.add(r1)
        db.session.add(r2)
        db.session.add(f1)
        db.session.commit()
        
        self.u1=u1
        self.r1=r1
        self.r2=r2
        self.f1=f1

    def test_login_user(self):
        u=User.authenticate(self.u1.username,USER_DATA["pwd"])
        self.assertEqual(self.u1,u)
    
    
    def test_unrecognized_user(self):
        u=User.authenticate("asdad",USER_DATA["pwd"])
        self.assertEqual(False,u)


    def test_user_favorite_recipe(self):
        self.u1.recipe.append(self.r2)
        f2= Favorites.query.filter_by(recipe_id = self.r2.id).first()
        self.assertEqual(f2.user_id,self.u1.id)


    def test_user_already_favorite_recipe(self):
        self.u1.recipe.append(self.r1)
        f= Favorites.query.filter_by(recipe_id = self.r1.id).all()
        self.assertEqual(len(f),1)

        
    def tearDown(self):
        db.session.remove()


