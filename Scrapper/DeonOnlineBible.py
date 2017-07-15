# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 16:28:21 2017

@author: admin
"""

import numpy as np
import urllib.request
import re

from bs4 import BeautifulSoup

#interface
class Scrapper:
    def get_text(self):
        pass
    
class DeonScrapper(Scrapper):
    def __init__(self, url, filepath):
        self.url = url
        self.filepath = filepath
        
    def get_text(self, verbose=False):
        r = urllib.request.urlopen(self.url)
        parser = BeautifulSoup(r.read().decode('iso-8859-2'), 'html.parser')
        books_tags = parser.find_all('a', class_='ks')
        books_urls = [self.url+str(book['href']) for book in books_tags]
        books = [BookScrapper(url) for url in books_urls]
        
        file = open(self.filepath, 'w', encoding='utf8')
        books_texts = []
        for book in books:
            books_texts.append(book.get_text(verbose))
            file.write(books_texts[-1])
        
        return ' '.join(books_texts)
    
class BookScrapper(Scrapper):
    def __init__(self, book_url):
        self.url = book_url
        
    def get_text(self, verbose=False):
        r = urllib.request.urlopen(self.url)
        page_txt = r.read().decode('iso-8859-2')
        url_begin = re.match(r'.+\?', self.url).group(0)+r'id='
        url_begin = re.sub('ksiega', 'rozdzial', url_begin)
        parser = BeautifulSoup(page_txt, 'html.parser')
        select_chapter = parser.find('select', {'name':'rozdzial'})
        chapters_url = [url_begin+str(child['value']) for child in select_chapter.children]
        pages = [PageScrapper(url) for url in chapters_url]
        return ' '.join([page.get_text(verbose) for page in pages])
        
    
class PageScrapper(Scrapper):
    def __init__(self, page_url):
        self.url = page_url

        
    def get_text(self, verbose=False):
        r = urllib.request.urlopen(self.url)
        page_txt = r.read().decode('iso-8859-2')
        page_txt = re.sub(r'<br>', '', page_txt)
        page_txt = re.sub(r'<br.*/>', '', page_txt)
        parser = BeautifulSoup(page_txt, 'html.parser')
        if(verbose):
            print(self.url)
        
        div_content = parser.find_all('div', class_='tresc')[0]
        [x.extract() for x in div_content.find_all('a')]
        [x.extract() for x in div_content.find_all(['span', 'sup'])]
        [x.extract() for x in div_content.find_all('div', class_='initial-letter')]
        [x.extract() for x in div_content.find_all('div', class_=[re.compile(r'tytul.+'),
                                                                  re.compile(r'miedzytytul.+')])]
        temp_text = div_content.get_text().strip()
        temp_text = re.sub(r'[\n]', '', temp_text)
        temp_text = re.sub(r'[\s]{2,}', ' ', temp_text)
        filter_1 = lambda x: not(x in ['»', '«', '[', ']'])
        temp_text = ''.join(list(filter(filter_1, temp_text)))
        return temp_text

def main():
    deon_scrapper = DeonScrapper("http://www.biblia.deon.pl/", r"bible.txt")
    deon_scrapper.get_text(True)
    
if __name__ == "__main__":
    main()
