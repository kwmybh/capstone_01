from flask import Flask, render_template, redirect, session, flash, request, g, url_for
from flask_assets import Environment, Bundle
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.sql.operators import exists
from models import connect_db, db, User, Favorites, Recipe
from forms import RegisterForm, LoginForm
import os


app = Flask(__name__)
assets = Environment(app)

js = Bundle('script.js', output='gen/packed.js')
assets.register('js_all', js)


app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL',"postgresql://postgres:H%40L!M@localhost:5432/smart_recipe_db")
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL',"postgresql:///smart_recipe_db")
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'topsecret')



connect_db(app)
# db.drop_all()
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route("/")
def homepage():
    """Show homepage with links to site areas."""
    if "user_id" in session:
        userid = session["user_id"]
        return redirect(f"/homepage")
    else:
        return render_template("index.html")
        

@app.route("/homepage")
def userpage():
    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/")
    userid = session["user_id"]
    user= User.query.get_or_404(userid)
    return render_template("recipe_search.html",recipes=user.recipe)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: produce form & handle form submission."""

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        user_exists=User.query.filter_by(username = name).first()
        if user_exists:
            flash("User Exists", "danger")
            return render_template("register.html", form=form)
        user = User.register(name, pwd)
        
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id

        # on successful login, redirect to recipe_search page
        return redirect(f"/homepage")

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
            return redirect(f"/homepage")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)
# end-login

@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("user_id")

    return redirect("/")





##############################################################################
# Favorites routes:



@app.route("/favorites",methods=["POST"])
def favorites_post():

    if "user_id" not in session:
        flash("You must be logged in to view!", "danger")
        return redirect("/")

    userid = session["user_id"]
    user = User.query.get_or_404(userid)
    
    recipe_name = request.form.get("mealName")
    recipe_instructions = request.form.get("mealInstruction")
    recipe_img = request.form.get("mealImg")
    recipe_vid = request.form.get("mealVid")

    recipe_exists = db.session.query(Recipe.name).filter_by(name = recipe_name).first() is not None
    if  recipe_exists:
        #flash('Recipe already favorited','danger')  
        user.recipe.append(Recipe.query.filter_by(name = recipe_name).first())  
        db.session.commit()   
    else:
        post_favorite = Recipe(name=recipe_name, img=recipe_img, text=recipe_instructions, vid = recipe_vid) 
        user.recipe.append(post_favorite)    
        db.session.add(post_favorite)
        db.session.commit()
        flash("A new recipe has been added to Favorites!", "success")
    return redirect(url_for("homepage"))
    

@app.route("/favorites", methods=["GET"])
def favorites_view():
    """display favorites."""

    if "user_id" not in session:
        flash("You must be logged in to view!", "danger")
        return redirect("/")
    
    userid = session["user_id"]
    user = User.query.get_or_404(userid)

    # CORRECTLY RENDER RECIPES IN FAVORITES HTML
    #post_favorite = Recipe.query.filter_by(id=userid).one()
    return render_template("favorites.html", user=user)
    # return render_template("favorites.html", values=user.query.all())


# End of Favorites routes:
##############################################################################




