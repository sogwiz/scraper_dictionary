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
# docker run -v $(pwd):/usr/src/app -it sogwiz/assyrian_spider /bin/bash
