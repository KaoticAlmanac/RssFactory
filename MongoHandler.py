import datetime

from pymongo import MongoClient
import pprint


class MongoHandler:
    def __init__(self):
        pass

    @staticmethod
    def get_rss_list_from_db():
        # type: () -> list[dict[str,str]]
        """Gets the rss list, returns it in the format of {link:link,language:language}"""
        client = MongoClient()
        rss_collection = client['TT']['rss_list']
        rss = rss_collection.find({})  # This finds all of the documents in the collection rss_list
        client.close()
        return rss

    @staticmethod
    def get_last_article_from_rss(rss):
        # type: (str) -> dict
        """Takes in the link and queries the server for the last article"""
        client = MongoClient()
        # Grabs all the links that match and orders it the newest first
        # If I was worried that there would be too many articles I would set up a fast ordering
        article = client['TT']['articles'].find({'link':rss}).sort({'pubDate':-1})[0]
        if not article:
            return {'title': '', 'pubDate': datetime.datetime.min, 'link': rss}
        return article

    @staticmethod
    def get_articles_from_rss(rss):
        # type: (str) -> list
        client= MongoClient()
        articles = client['TT']['articles'].find({'link': rss}).sort({'pubDate': -1})

        list_of_articles =[]
        for page in articles:
            list_of_articles.append(page)
        return list_of_articles

    @staticmethod
    def insert_new_articles(list_of_articles):
        # type: (dict) -> None
        """This firsts gets a language list, should be stored in the db but since its only needed for this
           I will just write a file."""

        return

    @staticmethod
    def get_language_list():
        """"""
        return
