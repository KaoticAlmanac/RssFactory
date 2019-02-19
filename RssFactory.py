import requests
#from typing import Union

from FileHandler import FileHandler
from RssParser import RssParser

# This exists in case I can't use the database on the server, if false it saves the rss to a file
# If true it saves the rss to a database
DATABASE = False


def get_rss_list():
    """This will call mongo to grab the RSS list that will likely be populated by hand.
       In the future I plan to have an alert if a new rss becomes available.
       Although for now I will just have a couple for testing"""
    return "https://searchdatacenter.techtarget.com/rss/IT-infrastructure-news.xml\n" \
           "https://searchdatacenter.techtarget.com/es/editorspicks\n" \
           "https://www.lemagit.fr/rss/ContentSyndication.xml\n" \
           "https://www.searchnetworking.de/rss/Alle-Artikel-und-News-von-SearchNetworkingDE.xml\n" \
           "https://searchwindevelopment.techtarget.com/rss/NET-Architecture-Essentials-Channel.xml"


def get_last_article(rss_feed):
    # type: (str) -> Union[dict,FileHandler]
    # if None return {'title':'','pubDate':datetime.datetime.min,'link':rss_feed}
    # until I get access to server, save it to files
    # todo create FileHandler.py and MongoHandler.py to handle all of this
    if not DATABASE:  # For use before setting up database or if server I can access won't have a db for me to use
        return FileHandler(rss_feed)
    return {}


def get_new_xml(rss_list):
    # type: (str) -> list[list[dict[str, str]]]
    """Gets the new articles from the xml links
       :param rss_list link to rss page
       :return list of new articles"""
    parsed_rss_list = []
    for rss in rss_list.splitlines():  # Splitlines is because each link will be delineated by it
        print(rss)
        # todo: error handle response and maybe validate its code 200?
        response = requests.get(rss)  # Gets the rss

        # Creates the parser that will parse the xml. Makes sure that the xml can be parsed, throws error otherwise
        parser = RssParser(response.content)
        handler = get_last_article(rss)  # Gets the last article saved on the server
        # Parses the xml until I get a past article or I go past the previous time limit for an article
        # The previous time is in case the latest article is deleted
        last_article = handler.get_last_article_from_file()

        # todo: check to see if there is any data, if not no need to
        # todo: Once a day or so validate everything
        parsed_rss_list.append(parser.parse_until_point(last_article))
    return parsed_rss_list


def insert_new_xml(parsed_rss_list):
    # type: (list[RssParser]) -> None
    """Inserts the parsed rss into the database"""
    print(parsed_rss_list)

    return


def factory_start():
    rss_list = get_rss_list()
    parsed_rss_list = get_new_xml(rss_list)
    insert_new_xml(parsed_rss_list)  # iterate through list and upload all the new articles


if __name__ == '__main__':
    # todo: for arg in sys.argv[1]: --gives command to either run regular or validate entire xml
    factory_start()
