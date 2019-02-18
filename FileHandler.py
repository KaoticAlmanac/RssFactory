import datetime

from PyInstaller.compat import FileNotFoundError


class FileHandler:
    """This is now deprecated, it is also incomplete, but leaving it here for posterity
       I thought I wouldn't get access to a server with a db that I was allowed to use
       But I learned I could"""
    def __init__(self, filename):
        self.filename = filename
        self.directory = "saved_rss/"
        try:
            f = open(self.directory + filename, 'a+')
            f.close()
        except FileNotFoundError:
            print("FileNotFoundError in FileHandler.py")
            print("This should never occur because this creates the file if it doesn't exist")
        except Exception as e:
            print("Error making file in FileHandler.py")
            print(e.message)
            raise e

    @staticmethod
    def _convert_file_line_to_dict(rss_line):
        # type: (str) -> dict
        """Format: link,title,date\n"""
        line = [x.strip for x in rss_line.split(',')]  # This removes all white space too
        # Converts the file format to string format to a dict for return
        # pubDate is a string here, it is normally a date, but it converts to a date in RssParser
        return {'link': line[0], 'title': line[1], 'pubDate': line[2]}

    def get_last_article_from_file(self):
        # type: () -> dict
        try:
            f = open(self.directory + self.filename, 'r')
            last_line = f.readline()

            if not last_line:  # This checks if the file is empty then returns the default empty set
                return {'title': '', 'pubDate': datetime.datetime.min, 'link': self.filename}
            f.close()
            return self._convert_file_line_to_dict(last_line)
        except FileNotFoundError:
            print("File Not Found: This should never happen")
            return {'title': '', 'pubDate': datetime.datetime.min, 'link': self.filename}
        except Exception as e:
            print("Error trying to open file")
            print ("Error is not FileNotFoundException")
            print(e.message)
            raise e

    def save_new_rss_to_file(self,rss_feed):
        # type: (list[dict[str, str]]) -> None
        """Format: link,title,date\n"""
        lines = ""
        for data in rss_feed:
            lines += data['link']+","+data['title']+","+data['pubDate']+"\n"
        self.line_prepender(self.directory+self.filename,lines)
        return

    @staticmethod
    def line_prepender(filename, lines):
        """This method opens up a file, reads its content into memory, then prepends the newer content and writes it all
           into a file.
           :param filename This should include the directory, this method will likely be used again in another project
           :param lines This is the new content to be added"""
        # Removes the trailing white space and new line characters
        new_lines = lines.split()
        try:
            f = open(filename,'r')  # to read in file
            originial_text= f.read()
            f.close()

            f = open(filename,'w')  # overwrites file as a new file
            f.write(new_lines+"\n")  # Writes the new lines and adds a new line since I removed the trailing one above
            f.write(originial_text)
            f.close()
        except FileNotFoundError as e:
            print("File Not Found in line_prepender")
            print(e.message)
            raise e
        except Exception as e:
            print("There was an error (not FileNotFound) in line_prepender")
            print(e.message)
            raise e
