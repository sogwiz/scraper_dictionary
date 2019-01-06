import os
import json
import sys
import time
import getopt

os.environ["PARSE_API_ROOT"] = "https://assyrian-433.nodechef.com/parse"

from parse_rest.datatypes import Function, Object, GeoPoint
from parse_rest.connection import register
from parse_rest.query import QueryResourceDoesNotExist
from parse_rest.connection import ParseBatcher
from parse_rest.core import ResourceRequestBadRequest, ParseError

APPLICATION_ID = ''
REST_API_KEY = ''
MASTER_KEY = ''
dir_east = ''


def printUsage():
	print("Usage: uploader.py --id_ap <PARSE_APPLICATION_ID> --key_rest <PARSE_REST_API_KEY> --key_master <PARSE_MASTER_KEY> --dir_east </path/to/eastern/terms>")

def returnArray(originalString):
	if isinstance (originalString,list):
		return originalString
	if originalString is None:
		return None
	if not originalString:
		return None
	arr = originalString.split(",")
	return arr

def getCleanString(originalString):
    if originalString is None:
        return None
    if not originalString:
        return None
    if originalString == "(Undefined)":
        return None
    return originalString

unixOptions = "i:r:m:d:h"
gnuOptions = ["id_app=","key_rest=","key_master=","dir_east=","help"]
try:
	opts, args = getopt.getopt(sys.argv[1:], unixOptions, gnuOptions)
except getopt.GetoptError:
	print("ERROR")
	printUsage()
	sys.exit(2)

for opt, arg in opts:
	if opt in ("-i", "--id_app"):
		APPLICATION_ID = arg
	elif opt in ("-r", "--key_rest"):
		REST_API_KEY = arg
	elif opt in ("-m", "--key_master"):
		MASTER_KEY = arg
	elif opt in ("-d", "--dir_east"):
		dir_east = arg
	elif opt in ("-h", "--help"):
		printUsage()
		sys.exit(2)

if APPLICATION_ID =='' or REST_API_KEY == '' or MASTER_KEY == '' or dir_east == '':
	print(str(opts))
	printUsage()
	sys.exit(2)

print("\n====Using config====")
print("APPLICATION_ID = " + APPLICATION_ID)
print("REST_API_KEY = " + REST_API_KEY)
print("MASTER_KEY = " + MASTER_KEY)
print("dir_east = " + dir_east + "\n====Config End====\n")

register(APPLICATION_ID, REST_API_KEY, master_key=MASTER_KEY)

class DictionaryDefinition(Object):
    pass

class DictionaryWordDefinitionList(Object):
	pass

files = os.listdir(dir_east)

for file in files:
	if file.endswith(".json"):
		with open(dir_east+'/'+file) as data_file:
			try:
				term = file.replace(".json","")
				data = json.load(data_file)
				index = 0
				for i in data:
					index += 1
				
					print str(i.get("searchkey")) + " " + term + " " + str(index)
					if int(i.get("searchkey")) >= 100000:
						print("greater than 100000. Skipping term " + term)
						continue

					cfArr = returnArray(i.get("cf"))
					seeAlsoArr = returnArray(i.get("seealso"))
					#phonetic_str = i["phonetic"].replace("<td>","").replace("</td>","")
					#english_str = i["english"].replace("<td>","").replace("</td>","")
					
					audio = i.get('audio')
					if audio is not None:
						if len(audio)>0:
							audio = audio
					
					dictionaryDefinition = DictionaryDefinition(
						cf=cfArr,
						seealso = seeAlsoArr,
						east = getCleanString(i.get("east")),
						west = getCleanString(i.get("west_western")),
						origin = getCleanString(i.get("origin")),
						dialect = getCleanString(i.get("dialect")),
						semantics = getCleanString(i.get("semantics")),
						root = getCleanString(i.get("root")),
						source = i.get("sourceref"),
						west_western = i.get("west_western"),
						phonetic = getCleanString(i.get("phonetic")),
						phonetic_west = getCleanString(i.get("phonetic_west")),
						partofspeech = getCleanString(i.get("partofspeech")),
						searchkeynum = int(i.get("searchkey")),
						searchkey = str(i.get("searchkey")),
						searchkeystr = int(i.get("searchkey")),
						definition_arr = returnArray(i.get("english_orig")),
						english = (", ").join(i.get("english_orig")),
						english_short = i.get("english_short")

                    )

					#dictionaryDefinition = DictionaryDefinition(searchkey=i.get("searchkey"), searchkeynum=int(i.get("searchkey")), definition_arr = i.get("definition_arr"), east=i.get('east'), west=i.get('west'), west_western=i.get("west_western"), english=i.get("english"), english_short=i.get("english_short"), phonetic=i.get("phonetic"), phonetic_west=i.get("phonetic_west"), audio = audio, audio_west=i.get('audio_west'), cf=i.get('cf'), partofspeech = i["partofspeech"])
					print ("dictionaryDefinition is " + str((dictionaryDefinition)))
					
					print ("i is " + str(i))
					
					try:
						dictionaryDefinition.save()
						print("just saved " + str(dictionaryDefinition))
					except Exception as inst:
						print "Found a dup "
						print str(inst)
						print(type(inst))
						dictionaryDefinition = DictionaryDefinition.Query.get(searchkey=i["searchkey"])

					dictionary_word_definition_list = DictionaryWordDefinitionList(searchkey=i["searchkey"], searchkeynum=int(i["searchkey"]), word=term, dictionary_definition_obj = dictionaryDefinition, boost=i.get('score'))
					time.sleep(1.10)
					try:
						dictionary_word_definition_list.save()
						print("hi " + str(i))
					except Exception as inst:
						print "May have found a dup DictionaryWordDefinitionList"

					#sys.exit(0)
			except ValueError:  # includes simplejson.decoder.JSONDecodeError
				print file
			except Exception as inst:
				print "found exception when saving to parse"
				print type(inst)
				print file
				print inst
