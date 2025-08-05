import scrapy
import re
import sys


class AssyrianLanguagesDump(scrapy.Spider):
    name = "assyrianlanguagesdump"

    #def start_requests(self):
    #	searchTerm = getattr(self, 'tag', None)
    #	urls = [
    #		'http://assyrianlanguages.org/sureth/dosearch.php?searchkey='+searchTerm+'&language=english',
    #		'http://assyrianlanguages.org/sureth/dosearch.php?searchkey=sargon&language=english',
    #	]
    #	for url in urls:
     #       yield scrapy.Request(url=url, callback=self.parse)


    def start_requests(self):
    	url_list = []
    	for x in range(1,36051):
    		urlStr = 'http://assyrianlanguages.org/sureth/dosearch.php?searchkey='+str(x)+'&language=id'
    		yield scrapy.Request(url=urlStr, callback=self.parse, meta={'key':x})

    def parse(self, response):
    	#print "\nafter details\n"
    	try:
			east = response.css('span.eastsyriac::text').extract_first()
			west = response.css('span.westsyriac::text').extract_first()
			cf = response.css('span.wordlink').extract()
			phonetic = response.xpath("/html/body/table/tr/td[text()='Eastern phonetic :']/following-sibling::td[1]").extract()
			english = response.xpath("/html/body/table/tr/td[text()='English :']/following-sibling::td[1]").extract()
			audio = response.xpath("//embed[contains(@src,'.mp3')]/@src").extract()
			partofspeech = response.xpath("/html/body/table/tr/td[text()='Category :']/following-sibling::td[1]").extract_first()
			if partofspeech is not None:
				partofspeech = partofspeech.replace("<td>","").replace("</td>","")

			m = re.search('searchkey=(.+?)&', response.url)
			if m:
				searchkey = m.group(1)
			#print "phonetic is " + phonetic[1]
    	except Exception as e:
    		print "found error at word " + str(response.meta['key'])
    		print e

    	yield {
    		'east': east,
    		'west': west,
    		'audio':audio,
    		'phonetic': phonetic[0],
    		'searchkey': searchkey,
    		'key':response.meta['key'],
    		'english':english[0],
    		'cf': cf,
			'partofspeech': partofspeech,
    	}
