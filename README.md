Instructions for working with this repo

PURPOSE: to scrape data from various sites and also to upload the data to mongodb / parse backend

Steps
# pip install virtualenv
# source bin/activate
# pip install Scrapy
# pip install pymongo


To download data from assyrianlanguages.org while logged in to the site
# scrapy crawl assyrianlanguagesloggedin
This will scrape the entire repository and download it to a file called output.json

To update mongodb / parse backend with various data-points
# python updater.py


