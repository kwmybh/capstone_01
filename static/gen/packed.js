const searchBtn = document.getElementById('search-btn');
const mealList = document.getElementById('meal');
const mealDetailsContent = document.querySelector('.meal-details-content');
const favoritesBtn = document.getElementById('favorites-btn');
const recipeCloseBtn = document.getElementById('recipe-close-btn');

// event listeners
searchBtn.addEventListener('click', getMealList);
mealList.addEventListener('click', getMealRecipe);
favoritesBtn.addEventListener('click', () => {
	console.log('HITT');
	mealDetailsContent.parentElement.classList.append('recipes');
});
recipeCloseBtn.addEventListener('click', () => {
	console.log('X clicked!');
	mealDetailsContent.parentElement.classList.remove('showRecipe');
});

//document.querySelector(".formFavorite").addEventListener("submit",(e)=>{
//	e.preventDefault();
//	let recipeName=e.target.querySelector("#mealName").value;
//	let recipeText=e.target.querySelector("#mealInstruction").value;
//
//
//})
// get meal list that matches with the ingredients
function getMealList() {
	let searchInputTxt = document.getElementById('search-input').value.trim();
	fetch(
		`https://www.themealdb.com/api/json/v1/1/filter.php?i=${searchInputTxt}`
	)
		.then((response) => response.json())
		.then((data) => {
			let html = '';
			if (data.meals) {
				data.meals.forEach((meal) => {
					html += `
                    <div class = "meal-item text-center" data-id = "${meal.idMeal}">
                        <div class = "meal-img">
                            <img src = "${meal.strMealThumb}" alt = "food">
                        </div>
                        <div class = "meal-name">
                            <h3>${meal.strMeal}</h3>
                            <a href = "#" class = "recipe-btn">Get Recipe</a>
                        </div>
                    </div>
                `;
				});
				mealList.classList.remove('notFound');
			} else {
				html = "Sorry, we didn't find any meal!";
				mealList.classList.add('notFound');
			}

			mealList.innerHTML = html;
		});
}

// get recipe of the meal
function getMealRecipe(e) {
	e.preventDefault();
	if (e.target.classList.contains('recipe-btn')) {
		let mealItem = e.target.parentElement.parentElement;
		fetch(
			`https://www.themealdb.com/api/json/v1/1/lookup.php?i=${mealItem.dataset.id}`
		)
			.then((response) => response.json())
			.then((data) => mealRecipeModal(data.meals));
	}
}

// create a modal
function mealRecipeModal(meal) {
	console.log(meal);
	meal = meal[0];
	let html = `
        <h2 class = "recipe-title">${meal.strMeal}</h2>
        <p class = "recipe-category">${meal.strCategory}</p>
        <div class = "recipe-instruct">
            <h3>Instructions:</h3>
            <p>${meal.strInstructions}</p>
        </div>
        <div class = "recipe-meal-img">
            <img src = "${meal.strMealThumb}" alt = "">
        </div>
        <div class = "recipe-link">
		
			<ul>
				<a class="btn" href = "${meal.strYoutube}" target = "_blank"> Watch on YouTube
				<form method="post" action="/favorites" class="formFavorite">
					<input type="hidden" name="mealName" value="${meal.strMeal}"/>
					<input type="hidden" name="mealInstruction" value="${meal.strInstructions}"/>
					<input type="hidden" name="mealVid" value="${meal.strYoutube}"/>
					<input type="hidden" name="mealImg" value="${meal.strMealThumb}"/>
					<button class="btn" type="submit">Save To Favorites</button>
				</form>
			</ul>
        </div>
    `;
	mealDetailsContent.innerHTML = html;
	mealDetailsContent.parentElement.classList.add('showRecipe');
}
