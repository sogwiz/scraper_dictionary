import csv
import os
import subprocess
import sys
import time

with open('dictionary_words.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in spamreader:
		print row[1]
		#stream = os.popen("scrapy crawl assyrian -o " + row[1]+".json -a tag="+row[1])
		subprocess.call("scrapy crawl assyrian -o output/" + row[1]+".json -a tag="+row[1], shell=True) 
		#sys.exit(0)
		time.sleep(.2)