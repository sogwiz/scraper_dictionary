"""
designed to migrate or backfill a specific field within a MongoDB collection that was 
originally managed by Parse Platform. It identifies documents lacking a dictionary_definition field and 
populates it using a value extracted from a Parse-specific pointer field

Usage: 
python3 PostProcessor.py --db_conn_string="mongodb://user:pass@host.com:port/db?ssl=true"

Notes:

"""


from Configurator import Configurator
import sys
import traceback
from pymongo import MongoClient
from pymongo import UpdateOne

def main():
    config = Configurator(sys.argv[1:])
    client = MongoClient(config.db_conn_string)
    db = client['assyrian']
    collection = db['DictionaryWordDefinitionList']

    shouldContinue = True
    try:
        while shouldContinue:
            limit = 10000
            counter=0
            requests = list()
            #This is the core query. It iterates through documents in the DictionaryWordDefinitionList collection where the dictionary_definition field does not exist.
            for doc in collection.find({"dictionary_definition":{'$exists':False}}):
                #Parse Platform metadata
                objRef = doc['_p_dictionary_definition_obj']

                #It then splits the value of _p_dictionary_definition_obj by the $ character and 
                # takes the second part (index 1). This is a common pattern for extracting 
                # the objectId from Parse Platform's internal pointer string representation
                idValue = objRef.split('$')[1]
                print(doc['_id'] + " : " + idValue + " : " + doc['word'])
                
                #Creates an UpdateOne operation. It targets the current document using its _id and sets the 
                # dictionary_definition field to the idValue extracted earlier
                request = UpdateOne({'_id':doc['_id']},{'$set':{'dictionary_definition':idValue}})
                counter+=1
                requests.append(request)
                if counter>=limit:
                    break
            if len(requests)>0:
                result = collection.bulk_write(requests)
                print(result)
            else:
                print("all DictionaryWordDefinitionList have dictionary_definition values")
                shouldContinue = False
    except Exception as inst:
        print ("in exception")
        print (inst)

if __name__ == '__main__':
    main()