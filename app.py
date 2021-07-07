"""Example flask app that stores passwords hashed with Bcrypt. Yay!"""

from flask import Flask, render_template, redirect, session, flash,request
from flask_assets import Environment, Bundle
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Favorites, Recipe
from forms import RegisterForm, LoginForm


app = Flask(__name__)
assets = Environment(app)

js= Bundle('script.js', output='gen/packed.js')
assets.register('js_all', js)


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///smart_recipe_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"



connect_db(app)
db.drop_all()
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route("/")
def homepage():
    """Show homepage with links to site areas."""
    if "user_id" in session:
        userid = session["user_id"]
        return redirect(f"/homepage/{userid}")
    else:
        return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: produce form & handle form submission."""

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        user = User.register(name, pwd)
        
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id

        # on successful login, redirect to recipe_search page
        return redirect(f"/homepage/{user.id}")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, pwd)

        if user:
            session["user_id"] = user.id  # keep logged in
            return redirect(f"/homepage/{user.id}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)
# end-login  
  

@app.route("/homepage/<int:id>")
def userpage(id):
    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    return render_template("recipe_search.html")


@app.route("/favorites", methods=["GET"])
def favorites():
    """Example hidden page for logged-in users only."""

    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    userid=session["user_id"]
    user=User.query.get_or_404(userid)

    recipe_name=request.form.get("mealName")
    recipe_instructions=request.form.get("mealInstruction")
    # SEARCH IF THE RECIPE NAME IS ALREADY IN THE TABLE AND DON'T ADD IT IN THIS CASE, JUST USE IT
    recipe=Recipe(name=recipe_name,
                text=recipe_instructions)

    # ADD THIS NEWLY CREATE RECIPE TO THE USERS recipes array the user class
    
    return redirect(f"/favorites/{userid}")


@app.route("/favorites/<int:id>")
def userfavorites(id):
    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    user=User.query.get_or_404(id)
    # IN favorites html render the recipes array that is in the user object to the screen and offer the possibility to remove a favorited recipe
    return render_template("favorites.html",user=user)


@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("user_id")

    return redirect("/")




