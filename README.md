RecipeParser
============
Parses files created by RecipeCrawler.

Order
-----
1. parseProfiles.py
 - input: ./input/allProfiles.tsv
 - creates ./parsed/{parsedProfiles.tsv, hobbies.tsv, interests.tsv}
2. parseRecipes.py
 - input: ./input/recipes.tsv
 - creates ./parsed/parsedRecipes.tsv
 - requires ./parsed/parsedProfiles.tsv
3. parseIngredients.py
 - input: ./input/ingredients.tsv
 - creates ./parsed/parsedIngredients.tsv
 - requires ./parsed/parsedRecipes.tsv
4. parseRatings.py
 - input: ./input/all-user-recipe.tsv
 - creates ./parsed/parsedRatings.tsv
 - requires ./parsed/{parsedProfiles.tsv, parsedRecipes.tsv}

