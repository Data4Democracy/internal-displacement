import json
import os
import hashlib
import datetime
import sqlite3

def date_time_converter(dt):
    if isinstance(dt,datetime.datetime):
        return dt.__str__()


class Article(object):
    """Contains article text, date, extracted information and tag
     Parameters
        ----------
        content:                the text from the article
        publication_date:       the date of publication
        title:                  the title
        authors:                the authors
        domain:                 the domain
        content_type:           the type of content (text,image,video etc)
        url:                    the url of the article

    """

    def __init__(self, content, pub_date, title, content_type,authors,domain,url):
        self.content = content
        self.publication_date = pub_date
        self.title = title
        self.authors = authors
        self.domain = domain
        self.content_type = content_type
        self.url = url

    def tag(self, tag):
        """Use interpreter to tag article
        """
        self.tag = tag

    def parse(self):
        """Use interpreter to parse article
        """
        pass

    def export_to_json(self, storage_dir):
        """Save article to external json file
        :param storage_dir:     a directory in which to write the json file

        returns: The filepath to the newly created json file.
        """
        filename = hashlib.md5((self.domain + self.title + ",".join(self.authors)).encode('utf-8')).hexdigest() + ".json"
        filepath = os.path.join(storage_dir, filename)
        with open(filepath, 'w') as fp:
            json.dump(self.__dict__, fp, ensure_ascii=False,default = date_time_converter)
        return filepath

    def insert_into_sql_table(self,sql_cursor):

        url = self.url
        authors = ",".join(self.authors)
        pub_date = date_time_converter(self.publication_date)
        domain = self.domain
        content = self.content
        content_type = self.content_type
        try:
            sql_cursor.execute("INSERT INTO Articles VALUES (?,?,?,?,?,?)", (url,authors,pub_date,domain,content,content_type))
        except sqlite3.IntegrityError:
            print("URL{url} already exists in article table. Skipping.".format(self.url))
        except Exception as e:
            print("Exception: {}".format(e))

    def get_pub_date_string(self):
        return date_time_converter(self.publication_date)

