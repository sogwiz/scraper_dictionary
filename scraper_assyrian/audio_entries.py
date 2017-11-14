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

with open('/Users/sargonbenjamin/Downloads/sargonsays.csv', 'r') as csvfile:
    csvfile = csv.reader(csvfile)
    count = 0
    for row in csvfile:
        count += 1
        if count != 1:
            searchkeynumber = row[1]
            searchkeynumber = int(searchkeynumber)
            try:
                document = collection.find_one({'searchkeynum': searchkeynumber})
                print ("document is " + str(document))
                if document is not None:
                    print ("found stuff for " + str(searchkeynumber))
                    document['audio'] = "https://assyrianaudio.blob.core.windows.net/audioblobs/e_entry" + \
                        str(searchkeynumber) + ".mp3"
                    document['audio_west'] = "https://assyrianaudio.blob.core.windows.net/audioblobs/w_entry" + \
                        str(searchkeynumber) + ".mp3"
                    collection.save(document)
                    print ("tried this once. we are good")
                    #exit(0)
                    # dictionaryDefinition.save()
                else:
                    print ("couldn't find searchkeynum " + searchkeynumber)
            except Exception as inst:
                print ("in exception")
                print (inst)
