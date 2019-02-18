from RssParser import RssParser
import requests


def get_rss_list():
    """This will call mongo to grab the RSS list that will likely be populated by hand.
       In the future I plan to have an alert if a new rss becomes available.
       Although for now I will just have a couple for testing"""
    return ""


def get_last_article(rss_feed):
    # type: (str) -> dict
    return {}


def factory_start():
    rss_list = get_rss_list()
    parsed_rss_list= []
    for rss in rss_list:
        response = requests.get(rss)
        parser = RssParser(response.content)
        last_article=get_last_article(rss)
        parsed_rss_list.append(parser.parse_until_point({}))
