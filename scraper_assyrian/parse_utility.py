from parse_rest.datatypes import Function, Object, GeoPoint
from parse_rest.connection import register
from parse_rest.query import QueryResourceDoesNotExist
from parse_rest.connection import ParseBatcher
from parse_rest.core import ResourceRequestBadRequest, ParseError
import json
from pprint import pprint
import os
from difflib import SequenceMatcher

APPLICATION_ID = 'bklxBP3HiTmGPhxp066mLQALCB0gltX4iANVYMnU'
REST_API_KEY = 'oUgnEZd0zqKuCc70EYa2a9b9erVab4TDfUdbhLMf'
MASTER_KEY = 'HUWhw3s2Zlm5HBQWSsFyk297ofBYIZvUuqfubInY'

register(APPLICATION_ID, REST_API_KEY, master_key=MASTER_KEY)

class DictionaryDefinition(Object):
    pass

class DictionaryWordDefinitionList(Object):
    pass

#dictionaryDefinition = DictionaryDefinition(word='home', aramaic='\u323i0', web_ranking=1, boost=1, definition_arr='[stuff]')

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def parse_update(eastern_row, western_row, term, boost_factor):
    #print "in parse_update"
    if(boost_factor>=90):
        dictionaryWordDefinitionList = DictionaryWordDefinitionList.Query.get(searchkey=eastern_row['searchkey'],word=term)
        #print "object is " + str(dictionaryWordDefinitionList)
        dictionaryWordDefinitionList.boost = boost_factor
        #dictionaryDefinition = DictionaryDefinition.Query.get(objectId = dictionaryWordDefinitionList.dictionary_definition_obj.objectId)
        #dictionaryDefinition.phonetic_west = western_row['phonetic_west']
        #dictionaryDefinition.audio_west = western_row['audio_west']
        #dictionaryDefinition.west_western = western_row["west"]
        #dictionaryDefinition.save()
        dictionaryWordDefinitionList.save()

    #print "dictionaryDefinition obj is " + str(dictionaryDefinition)
    #dictionaryWordDefinitionList.save()


dir_syriac = 'syriac20ktest'
dir_eastern = 'target'
files = os.listdir(dir_syriac)

count_matches = 0
count_similar = 0
count_similar_medium = 0
count_similar_low = 0


for file in files:
    if file.endswith(".json"):
        with open(dir_syriac+'/'+file) as western_file:
            term = file.replace(".json","")
            try:
                data_western = json.load(western_file)
                if data_western is not None:
                    with open(dir_eastern+'/'+file) as eastern_file:
                        data_eastern = json.load(eastern_file)
                        index = 0
                        for i in data_eastern:
                            index += 1
                            east_western_unicode = i["west"]
                            for j in data_western:
                                west_western_unicode = j["west"]
                                if east_western_unicode == west_western_unicode:
                                    count_matches+=1
                                    print "\n--Found match---\n" + term + " " + i["searchkey"]
                                    print j["phonetic_west"]+ " " + i["phonetic"]
                                    print east_western_unicode
                                    print west_western_unicode
                                    #print i["webrank"]
                                    #parse_update(i, data_western[0], term, 100)
                                    #write to parse with a big boost
                                    break
                                elif similar(east_western_unicode, west_western_unicode)>0.95:
                                    count_similar+=1
                                    print "\nsimilar\n" + term + " " + i["searchkey"]
                                    print j["phonetic_west"] + " " + i["phonetic"]
                                    print east_western_unicode
                                    print west_western_unicode
                                    #print i["webrank"]
                                    #parse_update(i, data_western[0], term, 95)
                                    #write to parse with a smaller boost based off the similarity score?
                                elif similar(east_western_unicode, west_western_unicode)>0.92:
                                    count_similar_medium+=1
                                    #print "\nsimilar 0.92\n" + term + " " + i["searchkey"]
                                    #print j["phonetic_west"] + " " + i["phonetic"]
                                    #print east_western_unicode
                                    #print west_western_unicode
                                    #print i["webrank"]
                                    #parse_update(i, data_western[0], term, 92)
                                    #write to parse with a smaller boost based off the similarity score?
                                elif similar(east_western_unicode, west_western_unicode)>0.65:
                                    count_similar_low+=1
                                    #print "\nsimilar\n" + term + " " + i["searchkey"]
                                    #print data_western[0]["phonetic_west"]
                                    #print east_western_unicode
                                    #print west_western_unicode
                                    #print i["webrank"]
                                    #parse_update(i, data_western[0], term, 30)


            except Exception as e:
                print e

print "Found matches " + str(count_matches)
print "Found similar " + str(count_similar)
print "Found similar medium " + str(count_similar_medium)
print "Found similar low " + str(count_similar_low)                #print e



                #print term

                #
                #    print term
#
#
