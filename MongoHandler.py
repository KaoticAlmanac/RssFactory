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
        """client = MongoClient()
        rss_collection = client['TT']['rss_list']
        rss = rss_collection.find({})  # This finds all of the documents in the collection rss_list
        client.close()"""
        # I realized it would be easier to do this using languages.txt
        rss=[]
        with open("languages.txt",'r') as f:
            for line in f.readlines():
                line = line.strip()
                rss.append({'link':line.split(",")[0].strip(),'language':line.split(',')[1].strip()})
        return rss

    @staticmethod
    def get_last_article_from_rss(rss):
        # type: (str) -> dict
        """Takes in the link and queries the server for the last article"""
        client = MongoClient()
        # Grabs all the links that match and orders it the newest first
        # If I was worried that there would be too many articles I would set up a fast ordering
        try:
            #article = client['TT']['articles'].find({'rss_link':rss}).sort([('pubDate',-1),]).limit(1)[0]
            article = {}
            if not article:
                return {'title': '', 'pubDate': datetime.datetime.min, 'link': "", "rss_link": rss}
            return article
        except Exception as e:
            print("Error getting first article, returning null set")
            return {'title': '', 'pubDate': datetime.datetime.min, 'link': "", "rss_link": rss}
        #article={}

    @staticmethod
    def get_articles_from_rss(rss):
        # type: (str) -> list
        client= MongoClient()
        articles = client['TT']['articles'].find({'rss_link': rss}).sort([('pubDate', -1), ])

        list_of_articles =[]
        for page in articles:
            list_of_articles.append(page)
        return list_of_articles

    @staticmethod
    def insert_new_articles(list_of_articles):
        # type: (list[list[dict[str,str]]]) -> None
        """This firsts gets a language list, should be stored in the db but since its only needed for this
           I will just write a file."""
        print "in insert new articles"
        links_to_languages = MongoHandler.get_language_list()
        links_of_articles = set()  # This exists to make sure no duplicates are entered
        inserts=[]
        for articles in list_of_articles:
            print(articles)
            if articles:
                for art in articles:
                    if art['link'] not in links_of_articles:
                        links_of_articles.add(art['link'])
                        inserts.append({'title':art['title'],  # title of article
                                        'pubDate':art['pubDate'],  # date article was published
                                        'link':art['link'],  # link to specific article
                                        'rss_link':art['rss_link'],  # rss link for article, don't think I need?
                                        'language':links_to_languages[art['rss_link']]})  # Gets language of rss link
        print("__________________")
        print(inserts)
        print("__________________")
        client = MongoClient()
        client['TT']['articles'].insert_many(inserts)
        #print(client['TT'].count())
        return

    @staticmethod
    def get_language_list():
        """This returns a dict in the format link:language so that I can put in a link and get back its language to insert
        into the db"""
        languages={}
        with open("languages.txt","r") as f:
            for line in f.readlines():
                languages[line.split(",")[0]] = line.split(",")[1].strip()  # link: language
        return languages
