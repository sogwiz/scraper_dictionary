import os
import json
import sys
import time
import csv


os.environ["PARSE_API_ROOT"] = "https://assyrian-433.nodechef.com/parse"

from parse_rest.datatypes import Function, Object, GeoPoint
from parse_rest.connection import register
from parse_rest.query import QueryResourceDoesNotExist
from parse_rest.connection import ParseBatcher
from parse_rest.core import ResourceRequestBadRequest, ParseError

APPLICATION_ID = 'bklxBP3HiTmGPhxp066mLQALCB0gltX4iANVYMnU'
REST_API_KEY = 'oUgnEZd0zqKuCc70EYa2a9b9erVab4TDfUdbhLMf'
MASTER_KEY = 'HUWhw3s2Zlm5HBQWSsFyk297ofBYIZvUuqfubInY'

register(APPLICATION_ID, REST_API_KEY, master_key=MASTER_KEY)
class DictionaryDefinition(Object):
    pass

from pymongo import MongoClient

#client = MongoClient(
#    'mongodb://assyrian-433:PASSWORD@db-assyrian-433.nodechef.com:5414/assyrian?ssl=true')
client = MongoClient(
    'mongodb://assyrian-433:Sd4})9Hk@db-assyrian-433.nodechef.com:5414/assyrian?ssl=true')
db = client['assyrian']
collection = db['DictionaryDefinition']
input_file = sys.argv[1]

def returnArray(originalString):
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

with open(input_file) as data_file:
    data = json.load(data_file)
    index = 0
    for i in data:
        index += 1
        searchkeynum = int(i.get("searchkeynum"))
        
        #print str(i.get("searchkeynum")) + " " + str(index)
        #print "\n" + str(i.get("searchkeynum"))
        try:
            documentSearched = collection.find_one({'searchkeynum': searchkeynum})
            if documentSearched is None:
                print ("DIDN'T FIND stuff for " + str(searchkeynum))
                cfArr = returnArray(i.get("cf"))
                seeAlsoArr = returnArray(i.get("seealso"))
                
                document = DictionaryDefinition(
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
                    searchkeynum = int(i.get("searchkeynum")),
                    searchkey = str(i.get("searchkeynum")),
                    searchkeystr = int(i.get("searchkeynum")),
                    definition_arr = i.get("english"),
                    english = (", ").join(i.get("english"))
                    )

                print document
                document.save()
                #collection.insert_one(document)
                #print "\nnew document is "
                #print document
                #collection.save(document)
                #print "saved successfully :" + str(searchkeynum)
                time.sleep(.2)
                #sys.exit()
                #print str(i.get("searchkeynum")) + ",T"
            else:
                #print ("couldn't find searchkeynum " + str(searchkeynum))
                print str(i.get("searchkeynum")) + ",F"
        except Exception as inst:
            print ("in exception")
            print (inst)



