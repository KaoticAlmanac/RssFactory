from typing import Union
import xml.etree.ElementTree as ET
import datetime


class RssParser(object):
    """This class takes in rss and parsers it to a dictionary with only needed items"""

    def __init__(self, rss):
        """Makes sure that rss is valid"""
        try:
            print("Creating RssParser")
            parser = ET.XMLParser(encoding='utf-8')
            tree = ET.fromstring(rss, parser=parser)
        except Exception as e:
            print("Error trying to parse rss")

            print (e.message)
            raise e

        self.tree = tree
        self.items = []

    def parse_full_tree(self):
        """Fully parses the xml file and saves it to self.items"""
        list_of_items = []
        root = self.tree.getroot()

        for item in root.findall('item'):  # Only gets the item elements because that's all that matters
            list_of_items.append({"title": item.find('title').text,
                                  "link": item.find('link'),
                                  "pubDate": item.find('pubDate')})

        self.items = list_of_items
        return list_of_items

    def parse_until_point(self, recent_item):
        # type: (dict) -> list[dict[str, str]]
        """Parses through the xml until it matches a title or the publish date is less than or equal"""
        # todo: check to see if the title changed of an article
        list_of_items = []
        root = self.tree

        for item in root.iter('item'):  # Only gets the item elements because that's all that matters
            if item.find('title').text == recent_item['title']:
                break
            if isinstance(recent_item['pubDate'],basestring):
                recent_item['pubDate'] = self.convert_time(recent_item['pubDate'])
            if self.convert_time(item.find('pubDate').text) < recent_item['pubDate']:
                # alert this should only happen if something was deleted
                # todo: create alert system to email me or something...
                # todo: create validation system so that everything is reset and it is set to this
                break
            list_of_items.append({"title": item.find('title').text,
                                  "link": item.find('link').text,
                                  "pubDate": item.find('pubDate').text})
        self.items = list_of_items
        return list_of_items

    def get_item_values(self):
        return self.items

    def get_xml(self):
        return self.tree

    @staticmethod
    def convert_time(pubDate):
        # type: (str) -> datetime
        return datetime.datetime.strptime(pubDate, "%a, %d %b %Y %H:%M:%S %Z")
