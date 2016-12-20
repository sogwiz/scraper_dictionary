import os
import json
import sys
import time


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
		with open(dir_east+'/'+file) as data_file:
			try:
				term = file.replace(".json","")
				data = json.load(data_file)
				index = 0
				for i in data:
					index += 1
				
					print i.get("searchkey") + " " + term + " " + str(index)
					#phonetic_str = i["phonetic"].replace("<td>","").replace("</td>","")
					#english_str = i["english"].replace("<td>","").replace("</td>","")
					
					audio = i.get('audio')
					if audio is not None:
						if len(audio)>0:
							audio = audio
							
					dictionaryDefinition = DictionaryDefinition(searchkey=i.get("searchkey"), definition_arr = i.get("definition_arr"), east=i.get('east'), west=i.get('west'), west_western=i.get("west_western"), english=i.get("english"), english_short=i.get("english_short"), phonetic=i.get("phonetic"), phonetic_west=i.get("phonetic_west"), audio = audio, audio_west=i.get('audio_west'), cf=i.get('cf'), partofspeech = i["partofspeech"])
					
					time.sleep(.10)
					
					try:
						dictionaryDefinition.save()
					except Exception as inst:
						print "Found a dup "
						dictionaryDefinition = DictionaryDefinition.Query.get(searchkey=i["searchkey"])

					dictionary_word_definition_list = DictionaryWordDefinitionList(searchkey=i["searchkey"], word=term, dictionary_definition_obj = dictionaryDefinition, boost=i.get('score'))

					try:
						dictionary_word_definition_list.save()
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
