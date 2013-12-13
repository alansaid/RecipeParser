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
	userFile = open("parsed/parsedProfiles.tsv", 'w')
	interestFile = open("parsed/interest.tsv", 'w')
	hobbiesFile = open("parsed/hobbies.tsv",'w')
	user = 0

	file = open("allProfiles.tsv", "r")
	for line in file:
		try:
			line = line.rstrip('\n')
			user = user + 1
			[uid, username, hometown, livingin, joined, level, cookinginterest, hobbies, pro, timestamp] = line.split("\t")

			home = parseLocation(hometown)
			living = parseLocation(livingin)
			if len(joined) > 0 and "." in joined:
				joined = str(datetime.strptime(joined, "%b. %Y"))
			elif len(joined) > 0 and "." not in joined:
				joined = str(datetime.strptime(joined, "%b %Y"))

			timestamp = int(timestamp)/1000
			
			timestamp = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

			if len(cookinginterest) > 0:
				interests = parseInterests(user, cookinginterest)
				interestFile.write(interests)
			if len(hobbies) > 0:
				hobbs = parseInterests(user, hobbies)
				hobbiesFile.write(hobbs)
			profile = str(user) + "\t" + username + "\t" + str(uid) + "\t" + level + "\t" + joined + "\t" + pro + "\t" + home + "\t" + living + "\t" +  str(timestamp) + "\n"
			userFile.write(profile)
		except ValueError:
			print sys.exc_info()[0]
			print traceback.format_exc()
			sys.exit()
			#pass
	file.close()
	userFile.close()
	interestFile.close()
	hobbiesFile.close()
	return True

def parseInterests(user, interests):
	ints = "" 
	if len(interests) == 0:
		return ints
	interest = interests.split(',')
	for i in interest:
		ints = ints + str(user) + "\t" + i.strip() + "\n"
	return ints


def parseLocation(location):
	city = ""
	home = location.split(',')
	if len(home) == 2:
		[city, country] = location.split(',')
		parsedLocation = city + "\t\t" + country 
	elif len(home) == 3:
		[city, state, country] = location.split(',')
		parsedLocation = city + "\t" + state + "\t" + country
	elif len(home) == 4:
		[city, municipality, state, country] = location.split(',')
		parsedLocation = city + ", " + municipality + "\t" + state + "\t" + country
	elif len(home) > 1:
		num = len(home)
		for n in xrange(0, num-2):
			if len(home[n]) > 1:
				if len(city) == 0:
					city = home[n].strip()
				else:
					city = city + ", " + home[n].strip()
		state = home[num-2]
		country = home[num-1]
		parsedLocation = city + "\t" + state + "\t" + country
	else:
		parsedLocation = "\t\t"	
	return parsedLocation

def usage():
	print __doc__

if __name__ == "__main__":
	sys.exit(not main(sys.argv))

