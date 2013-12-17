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
from datetime import datetime

def main(args):
	authors = {} 
	userFile = open('parsed/parsedProfiles.tsv', 'r')
	recipeFile = open('parsed/parsedRecipes.tsv','r')
	userIDs = {}
	recipeIDs = {}
	for line in userFile:
		userData = line.split("\t")
		siteid = userData[2]
		userid = userData[0]
		userIDs[siteid] = userid
	userFile.close()
	for line in recipeFile:
		recipeData = line.split("\t")
		recipeid = recipeData[0]
		recipeurl = recipeData[8].rstrip('\n')
		recipeIDs[recipeurl] = recipeid	
	recipeFile.close()

	ratingFile = open("parsed/parsedRatings.tsv", 'w')
	file = open("input/all-user-recipe.tsv", "r")
	rating = 0
	for line in file:
		try:
			rating = rating + 1
			[userID, url, recipeType, avg_rating, user_rating, rated, timestamp] = line.rstrip('\n').split("\t")
			if url in recipeIDs:
				recipeID = recipeIDs.get(url)
			else:
				continue

			if userID in userIDs:
				userid = userIDs.get(userID)
			else:
				print line
				continue
			ratingDate = str(datetime.strptime(rated, '%b %d, %Y')).split(' ')[0]
			timestamp = int(timestamp)/1000

			output = userID + "\t" + recipeID + "\t" + user_rating + "\t" + avg_rating + "\t" + ratingDate + "\t" +  str(timestamp) + "\n"
			#print output
			ratingFile.write(output)
			#if rating == 200:
			#	sys.exit()
		except ValueError:
			print len(line.split("\t"))
			print sys.exc_info()[0]
			print traceback.format_exc()
			sys.exit()
			#pass
	ratingFile.close()
	return True

def usage():
	print __doc__

if __name__ == "__main__":
	sys.exit(not main(sys.argv))

