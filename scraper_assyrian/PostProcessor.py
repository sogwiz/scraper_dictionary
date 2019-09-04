from Configurator import Configurator
import sys
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
            for doc in collection.find({"dictionary_definition":{'$exists':False}}):
                objRef = doc['_p_dictionary_definition_obj']
                idValue = objRef.split('$')[1]
                print(doc['_id'] + " : " + idValue + " : " + doc['word'])
                
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