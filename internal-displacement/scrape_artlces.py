from bs4 import BeautifulSoup
import pandas as pd
from urllib import request

def get_urls(df, index=None, sample=None):
	pass


def remove_newline(text):
	text = text.replace('\n', ' ')
	text = text.replace('\xa0', ' ')
	return text

def text_from_url(url):
	html = request.urlopen(url).read()
	soup = BeautifulSoup(html, 'html.parser')
	_extracted = [s.extract() for s in soup(['script', 'link', 'style', 'id', 'class', 'li', 'head', 'a'])]
	text = remove_newline(soup.get_text())

