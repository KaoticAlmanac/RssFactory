from RssParser import RssParser
import requests


def get_rss_list():
    """This will call mongo to grab the RSS list that will likely be populated by hand.
       In the future I plan to have an alert if a new rss becomes available.
       Although for now I will just have a couple for testing"""
    return ""


def get_last_article(rss_feed):
    # type: (str) -> dict
    # if None return
    return {}


def get_new_xml(rss_list):
    # type: (str) -> list
    parsed_rss_list = []
    for rss in rss_list:
        response = requests.get(rss)  # Gets the rss

        # Creates the parser that will parse the xml. Makes sure that the xml can be parsed, throws error otherwise
        parser = RssParser(response.content)
        last_article=get_last_article(rss)  # Gets the last article saved on the server
        # Parses the xml until I get a past article or I go past the previous time limit for an article
        # The previous time is in case the latest article is deleted
        # todo: Once a day or so validate everything
        parsed_rss_list.append(parser.parse_until_point(last_article))
    return parsed_rss_list


def factory_start():
    rss_list = get_rss_list()
    parsed_rss_list = get_new_xml(rss_list)
    # iterate through list and upload all the new articles


