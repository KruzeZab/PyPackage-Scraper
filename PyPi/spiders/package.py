"""
----------------------$ scrapy crawl package---------------------------- on terminal
package.py
-- PackBot
Scrapes pypi package's name, url, description, github link, author, last release date, maintainers, version, etc..........
"""

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import PypiItem

class Package(CrawlSpider):
    """
    Spider to crawl through pypi's packages and scrape information
    """
    name = 'package' 

    allowed_domains = ['pypi.org']

    start_urls = [
        'https://pypi.org/search/?c=Programming+Language+%3A%3A+Python+%3A%3A+3',
    ]

    rules = (
        Rule(LinkExtractor(allow=('page=\d+', ), ),
        callback='parse_list', follow=True),
    )

    # Xpath of the data to scrape
    nameXpath = '//a[@class="package-snippet"]/h3[@class="package-snippet__title"]/span                       [@class="package-snippet__name"]/text()'

    verXpath = '//a[@class="package-snippet"]/h3[@class="package-snippet__title"]/span                       [@class="package-snippet__version"]/text()'

    descXpath = '//a[@class="package-snippet"]/p/text()'

    urlXpath = '//a[@class="package-snippet"]/@href'


    installXpath = '//span[@id="pip-command"]/text()'

    lastReleaseXpath = '//p[@class="package-header__date"]/time/text()'

    authorXpath = '//p/a[contains(@href, "mailto:")]/text()'

    maintainersXpath = '//span[@class="sidebar-section__maintainer"]/a/span                                          [@class="sidebar-section__user-gravatar-text"]/text()'
    
    gitHubLinkXpath = '//a[contains(@rel, "nofollow") and contains(@href, "git")]/@href'


    def parse_list(self, response):
        """
        Parse information through the packages list and then sends meta data and urls to 'parse_final'
        """
        items = PypiItem()

        name = response.xpath(self.nameXpath).get()
        version = response.xpath(self.verXpath).get()
        description = response.xpath(self.descXpath).get()
        url = response.xpath(self.urlXpath).get()
        items['name'] = name
        items['version'] = version
        items['description'] = description
        items['url'] = 'https://pypi.org'+url

        return scrapy.Request(url=items['url'], callback=self.parse_final, 
                             meta={'items': items}) #Sends url and items info to parse_final

    def parse_final(self, response):
        """
        -- Call from parse_list
        Scrapes additional information about the packages
        """
        items = PypiItem()
        installation = response.xpath(self.installXpath).get()
        lastReleaseDate = response.xpath(self.lastReleaseXpath).get()
        author = response.xpath(self.authorXpath).get()
        maintainers = response.xpath(self.maintainersXpath).get()
        githubLink = response.xpath(self.gitHubLinkXpath).get()

        items = response.meta.get('items') # Get data from parse_list
        items['installation'] = installation
        items['lastReleaseDate'] = lastReleaseDate
        items['author'] = author
        items['maintainers'] = maintainers
        items['githubLink'] = githubLink
        
        yield items #return items
