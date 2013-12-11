#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Convert JSON data to human-readable form.

Usage:
  prettyJSON.py domain team
"""

import sys
import glob
import traceback

def main(args):
	authors = {} 
	parsedIngredientsFile = open("parsed/parsedIngredients.tsv", 'w')
	recipeFile = open("parsed/parsedRecipes.tsv", 'r')
	ingredientsFile = open("ingredients.tsv", 'r') 
	ingredient = 0

	recipes = {}

	for line in recipeFile:
		recipeData = line.split("\t")
		recipeURL = recipeData[1] 
		recipeID = recipeData[0]
		recipes[recipeURL] = recipeID
	recipeFile.close()

	ings = {}
	for line in ingredientsFile:
		try:
			line = line.rstrip('\n')
			[url, name, siteID, amount] = line.split("\t")
			if name == "" or int(siteID) == 0 or name == 0:
				continue
			if name[len(name)-1] == ":":
				continue
			rId = recipes.get(url)
			tmpID = str(name.lower())+str(siteID.lower())
			if tmpID in ings:
				ingredient = ings.get(tmpID)
			else:
				ingredient = len(ings) + 1
				ings[tmpID] = ingredient
			output =  rId + "\t" + str(ingredient) + "\t" + siteID + "\t" + name + "\t" + amount + "\n"
			
			parsedIngredientsFile.write(output)
		except ValueError:
			print sys.exc_info()[0]
			print traceback.format_exc()
			sys.exit()
			#pass
	parsedIngredientsFile.close()
	ingredientsFile.close()
	return True


def usage():
	print __doc__

if __name__ == "__main__":
	sys.exit(not main(sys.argv))

