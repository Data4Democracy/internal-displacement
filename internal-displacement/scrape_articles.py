from bs4 import BeautifulSoup
import pandas as pd
from urllib import request
from urllib.error import HTTPError,URLError
import functools
import concurrent
from concurrent import futures
import sys
def removeNewline(text):
    ''' Removes new line and &nbsp characters.
    '''
    text = text.replace('\n', ' ')
    text = text.replace('\xa0', ' ')
    return text

def textFromUrl(url):
    ''' Takes a url and returns a single string of the main text on the web page.
    '''

    try:
        html = request.urlopen(url,timeout=15).read()
        soup = BeautifulSoup(html, 'html.parser')
        _extracted = [s.extract() for s in soup(['script', 'link', 'style', 'id', 'class', 'li', 'head', 'a'])]
        text = removeNewline(soup.get_text())
        print("Parsed - " + url)
        return text
    except HTTPError as e:
        print("Failed - ",url,e)
        return "Nil"
    except URLError as e:
        print("Failed - ",url,e)
        return "Nil"


        
def prepareDataset(df):
    '''
    Extracts the text from all the urls in the provided dataframe, returning the dataframe extended with a 
    column containing the text
    '''
    URLS = df.URL.values

    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(textFromUrl, url): url for url in URLS}
        texts = []
        for future in concurrent.futures.as_completed(future_to_url):
            texts.append(future.result())
    df["Text"] = texts
    df = df[~df.URL.str.contains("pdf")]
    df = df[df.Text != "Nil"]
    return df