import os
import json
import sys
import time

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


class DictionaryWordDefinitionList(Object):
    pass


dir_east = "/tmp/dictionary"
files = os.listdir(dir_east)

for file in files:
    if file.endswith(".json"):
        with open(dir_east + '/' + file) as data_file:
            try:
                term = file.replace(".json", "")
                data = json.load(data_file)
                index = 0
                for i in data:
                    index += 1

                    print str(i.get("searchkey")) + " " + term + " " + str(index)
                    if int(i.get("searchkey")) >= 100000:
						print("greater than 100000. Skipping term " + term)
						continue
                    # phonetic_str = i["phonetic"].replace("<td>","").replace("</td>","")
                    # english_str = i["english"].replace("<td>","").replace("</td>","")

                    # dictionaryDefinition = DictionaryDefinition(searchkey=i.get("searchkey"), definition_arr = i.get("definition_arr"), east=i.get('east'), west=i.get('west'), west_western=i.get("west_western"), english=i.get("english"), english_short=i.get("english_short"), phonetic=i.get("phonetic"), phonetic_west=i.get("phonetic_west"), audio = audio, audio_west=i.get('audio_west'), cf=i.get('cf'), partofspeech = i["partofspeech"])
                    dictionaryDefinition = DictionaryDefinition.Query.get(
                        searchkey=i.get("searchkey"))
                    
                    print dictionaryDefinition

                    dictionary_word_definition_list = DictionaryWordDefinitionList(searchkey=i["searchkey"], searchkeynum=int(i["searchkey"]), word=term, dictionary_definition_obj = dictionaryDefinition, boost=i.get('score'))
                    print(str(dictionary_word_definition_list))
                    time.sleep(1.1)
                    try:
                        dictionary_word_definition_list.save()
                    except Exception as inst:
                        print "May have found a dup DictionaryWordDefinitionList"
                    time.sleep(0.1)
            except ValueError:  # includes simplejson.decoder.JSONDecodeError
                print file
            except Exception as inst:
                print "found exception when saving to parse"
                print type(inst)
                print file
                print inst
