import scrapy
import re
import sys
import time


class QuotesSpider(scrapy.Spider):
    name = "syriac"
    
    #def start_requests(self):
    #	searchTerm = getattr(self, 'tag', None)
    #	urls = [
    #		'http://assyrianlanguages.org/sureth/dosearch.php?searchkey='+searchTerm+'&language=english',
    #		'http://assyrianlanguages.org/sureth/dosearch.php?searchkey=sargon&language=english',
    #	]
    #	for url in urls:
     #       yield scrapy.Request(url=url, callback=self.parse)
    	

    def start_requests(self):
        time.sleep(0.5)
    	searchTerm = getattr(self, 'tag', None)
        return [scrapy.Request('http://www.sfarmele.de/?eingabe='+searchTerm+'&deviceDesktop=&radio=sfarmele_en&page=main&schriftart=suryoyo',self.parse)]

    def parse(self, response):
        resultDivs = response.css('div.direkte-treffer').extract()
        if resultDivs:
            length = len(resultDivs)
            for x in range (1,length+1):
                west = response.xpath('//div[@class="direkte-treffer"]['+ str(x) +']/span[@class="aram suryoyo"]/text()').extract_first()
                phonetic = response.xpath('//div[@class="direkte-treffer"]['+ str(x) +']/span[3]/text()').extract_first()
    	        phonetic = phonetic.replace("[","").replace("]","")
                #an xpath of this style is returning emptiness even though it renders in browser and xpath checker
                #audio = response.xpath('//div[@class="direkte-treffer"]['+ str(x) +']/span[@class="td_audio"]/audio/source[contains(@src, "mp3")]/@src').extract_first()
                #audio = response.xpath('//div[@class="direkte-treffer"][1]/span[@class="td_audio"]/audio/source[2]/@src').extract_first()
                audio = None
                try:
                    audio = response.css('div.direkte-treffer:nth-child('+str(x)+') source::attr(src)').extract()[1]                
                    if audio:
                        print "audio is not null"
                        audio = 'http://www.sfarmele.de/' + audio
                        print audio
                except Exception as inst:
				    print "found exception when looking at audio " + str(inst)
                
                
                yield {
    		    'west': west,
    		    'phonetic_west': phonetic,
    		    'audio_west' : audio,
    	        }