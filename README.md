# RssFactory
Rss handler for a project for TechTarget
◦ Purpose
    ▪ This program is meant for the express purpose of getting articles from the Rss Feed
◦ Requirements
    ▪ One of the requirements to effectively use this program is a list of the Rss Feeds TechTarget uses
    ▪ Another requirement is that the Rss Feeds have to be the TechTarget feeds or formatted in the same manner.
    ▪ MongoDB 
        • This version was specifically tested on an old version of Mongodb as that was all I had access to. It should theoretically still run fine regardless of newer version. 
◦ Classes/Methods
    ▪ Global Variable – VALIDATION
        • This variable is meant to reset all the articles in the database. This is called once a day and is meant to make sure that if any articles changed their data, the Rss Feed won’t permanently be incorrect. 
            ◦ In a future release I would create a communication channel between RssParser which would notice this type of change and RssFactory.py which controls VALIDATION
    ▪ RssFactory
        • This file is all the methods to control the program. 
        • Methods
            ◦ factory_start
                ▪ This method is the main method for the program, it grabs the Rss site listings, sends them to get parsed and then sends the parsed Rss into the database
            ◦ insert_new_xml
                ▪ Param
                    • The new articles to be inserted into the database
                    • For each Rss link, it returns a dictionary for each new article in a list, then it creates a list of those lists to encompass every Rss link
                    • list[list[dict[str,str]]]
                ▪ This just sends the articles into MongoHandler
            ◦ get_new_xml
                ▪ Param
                    • This is just a list of dictionaries for every Rss link in the format of: {link:link, language:language} 
                ▪ This method iterates through the list of dictionaries uses requests to access the links and return the xml file. It sends the raw xml to handle_xml along with the file name and that returns a list of each of the articles from the xml. This method then appends the list of xml articles to the variable parsed_rss_list
                ▪ There is a lot of error handling and it looks very off. This is mainly because of the older version of python on the server causing issues on handling links. It tries to get the link, if there is an issue (the main one likely being that there is an issue getting its SSL verification) it tries to get the link ignoring SSL verification. It tries that 5 times in case of any timeout issues. There are libraries to handle that in Python but the server I was using has such an older version of python that I couldn’t use a lot of those libraries or if it did work, it failed to consistently get the data. I can’t update the python on the server since it isn’t my server. 
                ▪ An extra piece of error handling is if the parsing of xml ever returns an error, it will add those links to a file for human review. All the times it has returned this error it was because of a no access policy. 
            ◦ handle_xml
                ▪ Param
                    • the raw xml file obtained from response
                    • the rss link
                ▪ Creates the parser class RssParser, feeds it the raw xml. Then it gets the last article saved on the database for the rss link in dictionary format, if there is nothing then it returns a dictionary with no title, the minimum date possible in python and no link to an article. It then asks the RssParser to parse until it can find the the last article or it gets to the end of the file.
                ▪ Returns the parsed xml in a list of dictionaries
            ◦ get_last_article_handler
                ▪ param
                    • The Rss link
                ▪ Asks the database for the last article that it has saved for that link
                ▪ Returns the last article saved on the database in the format: {title, link, rss_link,pubDate}
            ◦ get_rss_list
                ▪ Gets all the rss list from a file
    ▪ RssParser
        • This class handles the raw XML and converts it to a workable format in the form of: {title,link,pubDate,rss_link}
        • Methods
            ◦ __init__
                ▪ Checks to see if the rss link is from a Japanese site, if so it uses a different xml parser than the rest of the sites use. 
                    • This is because the Japanese links use rdf descriptors on the xml and the library I found to handle that doesn’t work with the rest of the rss
            ◦ parse_until_point
                ▪ Checks to see if it needs the Japanese parsing
                    • If so sends it to parse_until_point_jn
                ▪ Iterates through all the <item> in the tree
                ▪ If there are none it returns an empty set
                ▪ If there are
                    • It checks to see if the date of the current article is past the date of the most recent item (this is if an article was deleted)
                        ◦ It stops the loop and sends all the data it currently has to RssFactory
                    • It checks to see if the titles match
                        ◦ Although it might be better to check if the links match? Todo?
                    • It then adds the article to the list because it is a new article
            ◦ Convert_time
                ▪ Converts the rss time to a datetime of Python
    ▪ MongoHandler
        • A static class that handles all the reads and writes in the database
           Classes
            ◦ get_rss_list_from_db
                ▪ Iterates through the file languages.txt which hold all the rss links and the language for the link and returns it in dictionary format: {link,language}
            ◦ get_empty_article
                ▪ This is if there is no article for the rss link or if a validation is happening
            ◦ get_last_article_from_rss
                ▪ Queries the server for the last article from a specific link and returns get_empty_article if there is nothing
            ◦ insert_new_articles
                ▪ Inserts the list of lists of dictionaries that hold all the articles into the database. If its validation then it deletes all the stored articles right before inserting the new ones
            ◦ get_language_list
                ▪ Gets all the languages to Rss links because I forgot about keeping the language with the rss link until it was almost complete
                    • This can definitely be optimized
