import scrapy
import re
import sys
import os
from dotenv import load_dotenv


class AssyrianLanguagesLoggedIn(scrapy.Spider):
    name = "assyrianlanguagesloggedin"
    start_urls = ['http://assyrianlanguages.org/sureth/dologin.php']
    search_key_list = None
     # Load environment variables from .env file
    load_dotenv()
    
    # def start_requests(self):
    #	searchTerm = getattr(self, 'tag', None)
    #	urls = [
    #		'http://assyrianlanguages.org/sureth/dosearch.php?searchkey='+searchTerm+'&language=english',
    #		'http://assyrianlanguages.org/sureth/dosearch.php?searchkey=sargon&language=english',
    #	]
    #	for url in urls:
    #       yield scrapy.Request(url=url, callback=self.parse)

    def start_requests(self):
        search_key_param = getattr(self, 'searchkey', None)
        search_key_range_param = getattr(self, 'searchkeys', None)
        if search_key_param is not None:
            self.search_key_list = search_key_param.split(",")
        else:
            if search_key_range_param is not None:
                searchkeyrange = search_key_range_param.split("-")
                start = int(searchkeyrange[0])
                end = int(searchkeyrange[1])
                self.search_key_list = range(start, end+1, 1)
            else:
                self.search_key_list = None

        return [scrapy.FormRequest(url=self.start_urls[0], formdata={'user': os.getenv("ALUSER"), 'clearpassword': '', 'submitbtn': 'Login', 'password': os.getenv("ALPASS")},
                                   callback=self.startEditrequests)]

    def startEditrequests(self, response):
        url_list = []
        # for x in range(1,36051):
        if self.search_key_list is not None:
            for x in self.search_key_list:
                urlStr = 'http://assyrianlanguages.org/sureth/editframe.php?entryid=' + str(x) + '&bookmark=0'
                yield scrapy.Request(url=urlStr, callback=self.parseEditPage, meta={'key': x})
        else:
            for x in range(1, 38015):
                urlStr = 'http://assyrianlanguages.org/sureth/editframe.php?entryid=' + str(x) + '&bookmark=0'
                yield scrapy.Request(url=urlStr, callback=self.parseEditPage, meta={'key': x})

    def parseEditPage(self, response):
        print("\ntest after details\n")
        print(response.body)
        try:
            cf = response.xpath(
                "//textarea[@name='crossref']/text()").extract_first()
            seealso = response.xpath(
                "//textarea[@name='seealso']/text()").extract_first()
            sourceref = response.xpath(
                "//input[@id='sourceText']/@value").extract_first()
            origin = response.xpath(
                "//select[@name='origin']/option[@selected]/text()").extract_first()
            dialect = response.xpath(
                "//input[@id='dialectText']/@value").extract_first()
            semantics = response.xpath(
                "//select[@name='semantics']/option[@selected]/text()").extract_first()
            english = response.xpath(
                "//textarea[@name='english']/text()").extract_first()
            if english is None:
                english = ""
            east = response.xpath(
                    "//input[@name='syriac']/@value").extract_first()
            root = response.xpath(
                    "//input[@name='root']/@value").extract_first()
            phonetic = response.xpath(
                    "//input[@name='phonetic']/@value").extract_first()
            phonetic_west = response.xpath(
                    "//input[@name='western_phonetic']/@value").extract_first()
            partofspeech = response.xpath(
                    "//input[@id='categoryText']/@value").extract_first()
            # print "phonetic is " + phonetic[1]
        except Exception as e:
            print("found error at word " + str(response.meta['key']))
            print(e)

        yield {
            'searchkeynum': response.meta['key'],
            'seealso': seealso,
            'cf': cf,
            'sourceref': sourceref,
            'origin': origin,
            'dialect': dialect,
            'semantics': semantics,
            'english': english.split(";"),
            'east': east,
            'west_western': east,
			'root': root,
            'phonetic': phonetic,
            'phonetic_west': phonetic_west,
            'partofspeech': partofspeech,

        }
