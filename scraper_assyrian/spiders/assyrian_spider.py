import scrapy
import re
import sys


class QuotesSpider(scrapy.Spider):
    name = "assyrian"

    #def start_requests(self):
    #	searchTerm = getattr(self, 'tag', None)
    #	urls = [
    #		'http://assyrianlanguages.org/sureth/dosearch.php?searchkey='+searchTerm+'&language=english',
    #		'http://assyrianlanguages.org/sureth/dosearch.php?searchkey=sargon&language=english',
    #	]
    #	for url in urls:
     #       yield scrapy.Request(url=url, callback=self.parse)


    def start_requests(self):
    	searchTerm = getattr(self, 'tag', None)
        search_key = getattr(self, 'searchkey', None)
        if(search_key is not None):
            print "search key is not none"
            sys.exit(0)
        else:
            return [scrapy.FormRequest(url="http://assyrianlanguages.org/sureth/dosearch.php",
                    formdata={'stdkey': searchTerm, 'language': 'english', 'search': 'Search', 'syriackey': ''},
                    callback=self.parse)]

    def parse(self, response):
    	print "\nafter post\n"
    	#print response.body

    	webrank = 0
    	for listElement in response.xpath('//html/body/ol/span/li'):
    		webrank += 1
    		adjustedrank = 0
    		if 'next' in response.meta:
    			adjustedrank = webrank *10
    		else:
    			adjustedrank = webrank

    		#print "webrank is " + str(adjustedrank)
    		#print listElement.xpath('text()')
    		#print listElement.css('span.context')
    		#print listElement.css('span.eastsyriac')

    		print listElement.css('span.eastsyriac::text').extract_first()
    		url = listElement.xpath('a/@href').extract_first()
    		print "url = " + url

    		m = re.search('searchkey=(.+?)&', url)
    		if m:
    			searchkey = m.group(1)
    		print "searchkey is " + searchkey
    		#the yield will get us unicode
    		#to print out the decoded characters, use function decode('unicode_escape')
    		if url is not None:
    			detail_page = response.urljoin(url)
            	print "detail page is " + detail_page
            	yield scrapy.Request(detail_page,callback=self.parse_details,
            	meta={'text':listElement.xpath('text()').extract(), 'key':searchkey,'context':listElement.css('span.context::text').extract(), 'webrank':adjustedrank})

    		#yield {
    		#	'aramaic': listElement.css('span.eastsyriac::text').extract_first(),
            #   'text': listElement.xpath('text()').extract(),
            #	'context': listElement.css('span.context::text').extract(),
            #	'searchkey': searchkey,
            #}
        # follow pagination links
        next_page = response.xpath("//a[text()='Next >']/@href").extract_first()
        if next_page is not None:
        	next_page = response.urljoin(next_page)
        	print "\nnavigating to next page " + next_page
        	yield scrapy.Request(next_page, callback=self.parse, meta={'next':'yes'})

    def parse_details(self, response):
    	print "\nafter details\n"
    	east = response.css('span.eastsyriac::text').extract_first()
    	west = response.css('span.westsyriac::text').extract_first()
    	cf = response.css('span.wordlink').extract()
    	phonetic = response.xpath("/html/body/table/tr/td[text()='Eastern phonetic :']/following-sibling::td[1]").extract()
    	english = response.xpath("/html/body/table/tr/td[text()='English :']/following-sibling::td[1]").extract()
    	audio = response.xpath("//embed[contains(@src,'.mp3')]/@src").extract()
    	#print "phonetic is " + str(phonetic)
    	m = re.search('searchkey=(.+?)&', response.url)
    	if m:
    		searchkey = m.group(1)
    	#print "phonetic is " + phonetic[1]

    	yield {
    		'east': east,
    		'west': west,
    		'audio':audio,
    		'webrank':response.meta['webrank'],
    		'phonetic': phonetic[0],
    		'searchkey': searchkey,
    		'key':response.meta['key'],
    		'text':response.meta['text'],
    		'context':response.meta['context'],
    		'english':english[0],
    		'cf': cf,
    	}
