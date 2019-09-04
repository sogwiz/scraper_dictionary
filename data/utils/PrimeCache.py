from Configurator import Configurator
import sys
from pymongo import MongoClient
from pymongo import UpdateOne
from concurrent.futures import ThreadPoolExecutor
import requests

def main():
    config = Configurator(sys.argv[1:])
    client = MongoClient(config.db_conn_string)
    db = client['assyrian']
    collection = db['SearchStat']

    words = list()
    try:
        for doc in collection.find().limit(10000).sort("queries",-1):
            wordStr = doc['word']
            if wordStr:
                words.append(doc['word'])
    except Exception as inst:
        print ("in exception")
        print (inst)

    with ThreadPoolExecutor(max_workers=8) as executor:
        for wordStr in words:
            executor.submit(primeCache,wordStr, "http://sargonsays.com")

def primeCache(wordStr, host):
    urlStr = host + "/api/word/search/" + wordStr
    headers = {'user-agent': "curl",'Accept': "*/*",'Cache-Control': "no-cache",'Accept-Encoding': "gzip, deflate",'Connection': "keep-alive",'cache-control': "no-cache"}
    print(urlStr)
    try:
        response = requests.request("GET", urlStr, headers=headers, params='')
    except Exception as inst:
        print ("in request exception")
        print (inst)

    print(response)
    

if __name__ == '__main__':
    main()