import os
import json
import sys
import time
import csv


os.environ["PARSE_API_ROOT"] = "https://assyrian-433.nodechef.com/parse"


from pymongo import MongoClient

client = MongoClient(
    'mongodb://assyrian-433:PASSWORD@db-assyrian-433.nodechef.com:5414/assyrian?ssl=true')
db = client['assyrian']
collection = db['DictionaryDefinition']


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

with open('output.json') as data_file:
    data = json.load(data_file)
    index = 0
    for i in data:
        index += 1
        searchkeynum = int(i.get("searchkeynum"))
        print str(i.get("searchkeynum")) + " " + str(index)
        try:
            document = collection.find_one({'searchkeynum': searchkeynum})
            if document is not None:
                print ("found stuff for " + str(searchkeynum))
                cfArr = returnArray(i.get("cf"))
                seeAlsoArr = returnArray(i.get("seealso"))
                document['cf'] = cfArr
                document['seealso'] = seeAlsoArr
                document['origin'] = getCleanString(i.get("origin"))
                document['dialect'] = getCleanString(i.get("dialect"))
                document['semantics'] = getCleanString(i.get("semantics"))
                document['root'] = getCleanString(i.get("root"))
                if document.get('source') is None:
                    document['source'] = i.get("sourceref")

                if document.get('west_western') is None:
                    document['west_western'] = i.get("west_western")
                print "\nnew document is "
                print document
                collection.save(document)
                print "saved successfully :" + str(searchkeynum)
                time.sleep(.1)
            else:
                print ("couldn't find searchkeynum " + searchkeynum)
        except Exception as inst:
            print ("in exception")
            print (inst)



