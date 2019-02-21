import time
import xml.etree.ElementTree
import requests
from MongoHandler import MongoHandler

from FileHandler import FileHandler
from RssParser import RssParser


"""Broad changes, in mongohandler I can remove sending the language or I can remove getting the language at the end
   I should remove getting language at the end and add a piece of RssParser to get the language and include it"""


def get_rss_list():
    """This will call mongo to grab the RSS list that will likely be populated by hand.
       In the future I plan to have an alert if a new rss becomes available.
       Although for now I will just have a couple for testing"""
    return MongoHandler.get_rss_list_from_db()


def get_last_article_handler(rss_feed):
    # type: (str) -> dict
    # if None return {'title':'','pubDate':datetime.datetime.min,'link':rss_feed}

    return MongoHandler.get_last_article_from_rss(rss_feed)


def handle_xml(response, rss):
    # Creates the parser that will parse the xml. Makes sure that the xml can be parsed, throws error otherwise
    parser = RssParser(response.content)
    last_article = get_last_article_handler(rss['link'])  # Gets the last article saved on the server
    # Parses the xml until I get a past article or I go past the previous time limit for an article
    # The previous time is in case the latest article is deleted

    # todo: check to see if there is any data, if not no need to
    # todo: Once a day or so validate everything
    parsed_doc = parser.parse_until_point(last_article, rss['link'])
    if parsed_doc:
        return parsed_doc
    # time.sleep(1)


def get_new_xml(rss_list):
    # type: (dict) -> list[list[dict[str, str]]]
    """Gets the new articles from the xml links
       :param rss_list link to rss page
       :return list of new articles"""
    parsed_rss_list = []
    for rss in rss_list:  # Splitlines is because each link will be delineated by it
        print(rss)
        # todo: error handle response and maybe validate its code 200?
        try:
            try:
                """This attempts the requests, parses the xml and then adds it to a list.
                   Previous versions handled it in function, but issues on the server caused
                   it to have to wait until response finished. Such as I moved it to a function."""
                print("Requesting page")
                response = requests.get(rss['link'])  # Gets the rss

                # Appends the valuable information from the xml file to the list of articles
                parsed_rss_list.append(handle_xml(response, rss))
            except requests.exceptions.SSLError as e:
                print("Error getting response")
                # If I failed to access site with verification, I skip verification
                # I try again skipping verification and try 5 times if it fails
                for x in range(1,5):
                    try:
                        response = requests.get(rss['link'], verify=False)
                        parsed_rss_list.append(handle_xml(response, rss))
                        break
                    except Exception as e:
                        print("Could not access site!")
                        time.sleep(3)
        except xml.etree.ElementTree.ParseError:
            print("Error parsing: " + rss['link'])
            with open('remove_links.txt', "a+") as f:
                f.write(rss['link'] + "\n")
            print("Added link to dead link list")
    return parsed_rss_list


def insert_new_xml(parsed_rss_list):
    # type: (list[RssParser]) -> None
    """Inserts the parsed rss into the database"""
    # print(parsed_rss_list)
    MongoHandler.insert_new_articles(parsed_rss_list)
    return


def factory_start():
    rss_list = get_rss_list()
    parsed_rss_list = get_new_xml(rss_list)
    insert_new_xml(parsed_rss_list)  # iterate through list and upload all the new articles


if __name__ == '__main__':
    # todo: for arg in sys.argv[1]: --gives command to either run regular or validate entire xml
    factory_start()
