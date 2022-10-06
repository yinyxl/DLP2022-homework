import requests
from bs4 import BeautifulSoup


class ScienceArticles:
    """search scientists and their articles"""

    def __init__(self, authors_info):
        self.info = authors_info

    def search_authors(self):
        url = 'https://dblp.org/search?q=' + self.info
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
        Chrome/55.0.2883.87 Safari/537.36'}
        r = requests.get(url, headers=headers)

        author_dict = {}
        soup = BeautifulSoup(r.text, 'lxml')
        print(soup.title)
        results = soup.find('div', id='completesearch-authors')
        for result in results.find_all('ul', class_='result-list'):
            for authors in result.find_all('a'):
                link = authors['href']
                # print(link)
                for author_name in authors.find_all('span', itemprop='name'):
                    author_dict[author_name.text] = link

        print(author_dict)
        return author_dict

    def get_articles(self, link_author):
        # url = 'https://dblp.org/pid/09/2187.html'
        url = link_author
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
        Chrome/55.0.2883.87 Safari/537.36'}
        r = requests.get(url, headers=headers)

        soup = BeautifulSoup(r.text, 'lxml')
        print(soup.title)
        i = 0
        article_title = []
        for title1 in soup.find_all('span', class_='title'):
            i = i + 1
            article_title.append(title1.get_text())
            print(str(i) + ':' + article_title[i - 1])
