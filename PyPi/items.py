"""
items.py
Give a field for the scraped items
"""

import scrapy

class PypiItem(scrapy.Item):
    """
    Declaring fields for the scraped item
    """
    name = scrapy.Field() 
    version = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    
    installation = scrapy.Field()
    lastReleaseDate = scrapy.Field()
    author = scrapy.Field()
    maintainers = scrapy.Field()
    githubLink = scrapy.Field()
