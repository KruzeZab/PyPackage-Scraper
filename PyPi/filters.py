"""
Filters.py 
For filtering the scraped items before we store it.
"""
from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):
    """
    Filter Duplicate Items
    """
    def __init__(self):
        """
        Initialize an empty set
        """
        self.ids_seen = set()

    def process_item(self, item, spider):
        """
        If duplicate item found, drop it else add it to the set.
        """
        if item['name'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['name'])
            return item #return the item


class HtmlFilter(object):
    """
    Filter html tags and content
    """
    def process_item(self, item, spider):
        """
        Strip the item
        """
        if item.get('lastReleaseDate'):
            item['lastReleaseDate'] = item['lastReleaseDate'].strip()

        if item.get('maintainers'):
            item['maintainers'] = item['maintainers'].strip() 
                    
        return item  # Return the item
