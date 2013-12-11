#!/usr/bin/python

"""
Convert JSON data to human-readable form.

Usage:
  prettyJSON.py domain team
"""

import sys
#import simplejson as json
import json 
import glob

def main(args):
	recent="35"
	lucene="48"
	ts="1677"
	mt="13554"
	cfo="2525"
	s="596"
	wg="12935"
	clicks={}
	impressions={}
	files = range(11, 38, 1)
	logfiles = sorted(glob.glob("data.log.*"))
	for inFile in files:
		print str(inFile)
    		try:
    			inputFile = open("data.log."+str(inFile))
			domain = args[1]
			team = args[2]
			outFile = open("_data/" + team + "." + domain + ".log", 'w')
			for line in inputFile:
				toks = line.split("\t")
				try:
					if toks[0] == "MESSAGE":
						j = toks[2]
		    				input = json.loads(j)
						d = toks[3]
						# print json.dumps(input, sort_keys = False, indent = 4)
						try:
							type=input["type"]
							iteam=str(input["context"]["simple"]["41"])
							idomain=str(input["context"]["simple"]["27"])
							day=d.split(" ")[0]
							timestamp=str(input["timestamp"])
							if (type == "impression" or type == "click") and iteam == team and idomain == domain:
								if type=="click":
									if clicks.has_key(day):
										pp=clicks[day]
										pp=pp+1
										clicks[day]=pp
									else:
										clicks[day]=1
								if type=="impression":
									if impressions.has_key(day):
										pp=impressions[day]
										pp=pp+1
										impressions[day]=pp
									else:
										impressions[day]=1
								# type timestamp domain recommender date
								# outFile.write(type + "\t" + str(input["timestamp"]) + "\t" + str(input["context"]["simple"]["27"]) + "\t" + str(input["context"]["simple"]["41"]) + "\t" + d.split(" ")[0] + "\n")
								# outFile.write(type + "\t" + domain + "\t" + team + "\t" + day + "\t" + timestamp + "\n")
						except KeyError:
							pass
				except ValueError:
					pass
					#print inFile
					#print toks
					#print toks[3]
					#print "error: ", ses.exc_info()[0]
	    	
			inputFile.close()
    		except IndexError:
    			usage()
    			return False

	outFile.write("Day \t impressions \t clicks \n")
	for day in impressions:
		outFile.write(str(day) + "\t "  + str(impressions[day])) 
		try:
			outFile.write("\t"  + str(clicks[day]))
		except KeyError:
			pass
		outFile.write("\n")

	outFile.close()
    	return True

def usage():
    print __doc__

if __name__ == "__main__":
    sys.exit(not main(sys.argv))

