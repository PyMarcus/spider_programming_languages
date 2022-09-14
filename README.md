### Spider crawler programming language

A spider that crawler wikipedia page to get
programming languages content

PS: Its create a SQLite.

Install dependencies:

    pip install -r requirements

RUN:
    
    scrapy crawl spider

RUN AND SAVE JSON FILE:

    scrapy crawl spider -o spider.json

RUN TO SAVE JSON DATA INTO DATABASE (SQLite)

    python spider_language.py

Python version:
    
    3.10

Operational System:

    Windows 10 - 64bits
