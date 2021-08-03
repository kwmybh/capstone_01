# Smart Recipe

All you have is a tomato and looking for possible meal recipes? Look no further!

## Description

A simple site where users sign up to access a free recipe application with detailed instructions and video tutorials(via YouTube). All you need is one ingredient and an appetite.

This app provides additional ingredients to compliment what you already have and with an account, you are able to save recipes for future reference.

## Design

This is a full-stack app that uses the following frameworks/libraries/APIs:

- (FRONTEND)

* HTML+CSS with Jinja2 templating
* Javacript
* Bootstrap
* Font Awesome
* Heroku (deployment)

- (BACKEND)

* Python
* Flask
* SQLAlchemy
* WTForms

## API

- MealDB API (https://www.themealdb.com/api.php)
  TheMealDB was built in 2016 to provide a free data source api for recipes online
  in the hope that developers would build applications and cool projects ontop of it.
  TheMealDB originated on the Kodi forums as a way to browse recpies on your TV.

  Requests are sent to the API with a response of JSON. Developers can sign up for free but with limited features.

  Example:

      	`https://www.themealdb.com/api/json/v1/1/filter.php?i=${searchInputTxt}`

        {
            "meals":
            [
                {
                    "idMeal":"52771",
                    "strMeal":"Spicy Arrabiata Penne",
                    "strDrinkAlternate":null,
                    "strCategory":"Vegetarian",
                    "strArea":"Italian",
                    "strInstructions":"Bring a large pot of water to a boil...",
                    "strMealThumb":"https:\/\/www.themealdb.com\/images\/media\/meals\/ustsqw1468250014.jpg",
                    "strTags":"Pasta,Curry",
                    "strYoutube":"https:\/\/www.youtube.com\/watch?v=1IszT_guI08"
                }
            ]
        }

* Database Structure

![picturemessage_cpgquqi5 ien](https://user-images.githubusercontent.com/46819089/127821104-a482ebb9-1fbd-4a8b-b51a-19157f1d4d75.png)

## Getting Started

### Installing Dependencies

    pip install -r requirements.txt

### Executing App

    flask run

### Acknoledgments

- Halim Tannous
- Springboard
- YouTube
- Stack...
