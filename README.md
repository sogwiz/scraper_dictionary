Instructions for working with this repo

PURPOSE: to scrape data from various sites and also to upload the data to mongodb / parse backend

Steps
# pip install virtualenv
# source bin/activate
# pip install Scrapy
# pip install pymongo
# pip install git+https://github.com/milesrichardson/ParsePy.git


To download data from assyrianlanguages.org while logged in to the site
# scrapy crawl assyrianlanguagesloggedin
This will scrape the entire repository and download it to a file called output.json

To update mongodb / parse backend with various data-points
# cd scraper_assyrian
# python updater.py

Examples of running with docker
# docker build -t sogwiz/assyrian_spider .
# docker run -v $(pwd):/usr/src/app -it sogwiz/assyrian_spider scrapy crawl assyrianlanguagesloggedin -a searchkey=1232,12,501 -o out3.json
# docker run -v $(pwd):/usr/src/app -it sogwiz/assyrian_spider scrapy crawl assyrianlanguagesloggedin -a searchkeys=39000-39050 -o out3.json
# docker run -v $(pwd):/usr/src/app -it sogwiz/assyrian_spider /bin/bash

1. Run the scraper to download a json file
2. Run the java dictionary generator to generate the index and subsequent dictionary folder
3. run the uploader using the following cmd
python scraper_assyrian/uploader.py --dir_east=<DIR_DICTIONARY_GENERATED_AT> --id_app=<PARSE_APP_ID> --key_rest=<PARSE_REST_KEY> --key_master=<PARSE_MASTER_KEY> -file_scrape=<FILE_GENERATED_BY_SCRAPE_STEP>

Alternately, instead of step 3, one can perform the following two steps
- create DictionaryDefinition using updaternewentries.py by pointing to dictionary folder
- create DictionaryWordDefinitionList using uploader_newentries.py by pointing to dictionary folder
//TODO: what we really need to do is to update the uploader.py to read the english and dictionaryArr fields from the original scraped file. Everything else loads from the indexed dictionary generated files. the reason english and dicationaryArr must be collated with the original scrape file is because the format of those fields in the original scrape file is much cleaner and i can't seem to clean the data. So, what we can do in the meantime is load the scraped file into memory and use the english and dictionaryArr fields from that structure