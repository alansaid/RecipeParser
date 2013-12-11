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
	userFile = open('parsed/parsedProfiles.tsv', 'r')	
	userIds = {}
	for line in userFile:
		userData = line.split("\t")
		siteid = userData[2]
		userid = userData[0]
		userIds[siteid] = userid
	
	
	
	recipeFile = open("parsed/parsedRecipes.tsv", 'w')
	lines = 0
	file = open("recipes.tsv", "r")
	for line in file:
		try:
			line = line.rstrip('\n')
			if "\t404" in line:
				continue
			lines = lines + 1
			[url, title, servings, username, userID, cookingTime] = line.split("\t")
			#print "url: " + url
			#print "title: " + title
			#print "servings: " + servings
			#print "username: " + username
			#print "userID: " + userID
			#print "cookingTime: " + cookingTime
			myUserID = ""
			if userID in userIds:
				myUserID = userIds.get(userID)

			cookingTime = cookingTime.strip()
			if len(cookingTime) > 1:
				num = 0
				mins = 0
				[no, unit] = cookingTime.split(" ")
				no = no.strip("+")
				if unit == "day" or unit == "days":
					mins = 1560
				elif unit == "hr" or unit == "hrs":
					mins = 60
				elif unit == "min" or unit == "mins":
					mins = 1
				if "¼" in no:
					no = no.strip("¼").strip() + ".25"
				elif "½" in no:
					no = no.strip("½").strip() + ".5"
				elif "¾" in no:
					no = no.strip("¾").strip() + ".75"
				cookingTimeInMinutes = int(float(no) * int(mins))

			output = url + "\t" + title + "\t" + servings + "\t" + username + "\t" + userID + "\t" + myUserID + "\t" + cookingTime + "\t" + str(cookingTimeInMinutes) + "\n"
			recipeFile.write(output)
#			if lines == 200:
#				sys.exit()
		except ValueError:
			print line
			print len(cookingTime)
			print len(line.split("\t"))
			print sys.exc_info()[0]
			print traceback.format_exc()
			sys.exit()
			#pass
	file.close()
	recipeFile.close()
	return True

def usage():
	print __doc__

if __name__ == "__main__":
	sys.exit(not main(sys.argv))

