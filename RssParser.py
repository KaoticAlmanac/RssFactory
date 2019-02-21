# from typing import Union
import time
import xml.etree.ElementTree as ET
from lxml import etree
import datetime


class RssParser(object):
    """This class takes in rss and parsers it to a dictionary with only needed items"""

    def __init__(self, rss):
        """Makes sure that rss is valid"""
        ET_Holder = ET
        self.language = "na"
        if "co.jp" in rss:
            ET_Holder = etree
            self.language = "jn"
        try:
            print("Creating RssParser")
            parser = ET_Holder.XMLParser(encoding='utf-8')
            tree = ET_Holder.fromstring(rss, parser=parser)
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
            date_name = "pubDate"
            list_of_items.append({"title": item.find('title').text,
                                  "link": item.find('link'),
                                  "pubDate": item.find(date_name)})

        self.items = list_of_items
        return list_of_items

    def parse_until_point(self, recent_item, rss_link):
        # type: (dict,str) -> list[dict[str, str]]
        """Parses through the xml until it matches a title or the publish date is less than or equal"""
        # todo: check to see if the title changed of an article
        if "jn" in self.language:
            return self.parse_until_point_jp(recent_item, rss_link)
        list_of_items = []
        root = self.tree

        for item in root.iter('item'):  # Only gets the item elements because that's all that matters
            date_name = "pubDate"  # Dont need this anymore, this was to help identify jap pages and its different style
            if item.find('title').text.strip() == recent_item['title'].strip():
                print("Found last article breaking-----")
                break
            if isinstance(recent_item["pubDate"], basestring):
                recent_item[date_name] = self.convert_time(recent_item['pubDate'])
            if self.convert_time(item.find(date_name).text, date_name) < recent_item['pubDate']:
                # alert this should only happen if something was deleted
                # todo: create alert system to email me or something...
                # todo: create validation system so that everything is reset and it is set to this
                break
            item_formated = {"title": item.find('title').text,
                             "link": item.find('link').text,
                             "pubDate": RssParser.convert_time(item.find(date_name).text),
                             "rss_link": rss_link}
            print (item_formated)
            list_of_items.append(item_formated)
        self.items = list_of_items
        return list_of_items

    def parse_until_point_jp(self, recent_item, rss_link):
        # type: (dict,str) -> list[dict[str, str]]
        """Parses through the xml until it matches a title or the publish date is less than or equal"""
        # todo: check to see if the title changed of an article
        list_of_items = []
        root = self.tree

        for item in root.findall('item', root.nsmap):  # Only gets the item elements because that's all that matters
            date_name = "dc:date"
            if item.find('title', root.nsmap).text.strip() == recent_item['title'].strip():
                print("Found last article breaking-----")
                break
            if isinstance(recent_item["pubDate"], basestring):
                recent_item[date_name] = self.convert_time(recent_item['pubDate'])
            if self.convert_time(item.find(date_name, root.nsmap).text, date_name) < recent_item['pubDate']:
                # alert this should only happen if something was deleted
                # todo: create alert system to email me or something...
                # todo: create validation system so that everything is reset and it is set to this
                break
            item_formated = {"title": item.find('title', root.nsmap).text,
                             "link": item.find('link', root.nsmap).text,
                             "pubDate": RssParser.convert_time(item.find(date_name, root.nsmap).text),
                             "rss_link": rss_link}
            print (item_formated)
            list_of_items.append(item_formated)
        self.items = list_of_items
        return list_of_items

    def get_item_values(self):
        return self.items

    def get_xml(self):
        return self.tree

    @staticmethod
    def convert_time(pubDate, pubDateName="pubDate"):
        # type: (str,str) -> datetime
        """Each of these attempts are different date formats of different languages"""
        try:
            return datetime.datetime.strptime(pubDate, "%a, %d %b %Y %H:%M:%S %Z")
        except ValueError as e:
            try:
                return datetime.datetime.strptime(pubDate, "%a, %d %b %Y %H:%M:%S +0000")
            except ValueError as ee:
                return datetime.datetime.strptime(pubDate, "%Y-%m-%dT%H:%M:%S+09:00")
