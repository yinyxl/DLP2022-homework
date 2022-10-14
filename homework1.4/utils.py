import requests
from bs4 import BeautifulSoup


class ScienceArticles:
    """search scientists and their articles"""

    def __init__(self, authors_info):
        self.info = authors_info

    def search_authors(self,authors_info):
        url = 'https://dblp.org/search?q=' + self.info.replace(' ', '%20')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
        Chrome/55.0.2883.87 Safari/537.36'}
        r = requests.get(url, headers=headers)

        author_dict = {}
        soup = BeautifulSoup(r.text, 'lxml')
        print(soup.title.string)
        results = soup.find('div', id='completesearch-authors')
        for result in results.find_all('ul', class_='result-list'):
            for authors in result.find_all('a'):
                link = authors['href']
                # print(link)
                for author_name in authors.find_all('span', itemprop='name'):
                    author_dict[author_name.text] = link

        # print(author_dict)
        return author_dict

    def get_articles(self, link_author):
        # url = 'https://dblp.org/pid/09/2187.html'
        url = link_author
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
        Chrome/55.0.2883.87 Safari/537.36'}
        r = requests.get(url, headers=headers)
        r.encoding = 'utf-8'

        soup = BeautifulSoup(r.text, 'lxml')
        print(soup.title.string)
        article_title = []
        year_published = []
        link_article = []
        venues = []
        for part in soup.find_all('span', itemprop='isPartOf'):
            for venue_name in part.find_all('span', itemprop='name'):
                venues.append(venue_name.text)

        for button in soup.find_all('nav', class_='publ'):
            link = button.find('a')['href']
            link_article.append(link)
        for year_pub in soup.find_all('span', itemprop='datePublished'):
            year_published.append(year_pub.text)
        pub = soup.find('div', id="publ-section")
        for titles in pub.find_all('div', class_='hideable'):
            print(titles.find('h2').text)
            i = 0
            for title1 in titles.find_all('span', class_='title'):
                i = i + 1
                new_str = str(i) + ':' + title1.get_text()
                article_title.append(new_str)
                print(str(i) + ':' + title1.get_text())

        sum_records = len(article_title)
        print(len(venues))
        print(venues)
        print('The total number of articles is {}'.format(sum_records))
