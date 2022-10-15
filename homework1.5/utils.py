from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from functools import partial
import csv
import requests
from bs4 import BeautifulSoup


class CrawlWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(600, 400)
        self.layout = QGridLayout()
        self.layout.setSpacing(5)

        self.lb = QLabel(self)
        self.lb.setText('Scientist name：')
        self.lb.setFont(QFont("Roman times", 12, QFont.Bold))
        self.layout.addWidget(self.lb, 0, 0, 1, 1)

        self.textbox = QLineEdit(self)
        self.textbox.setMaximumSize(250, 40)
        self.layout.addWidget(self.textbox, 0, 1, 1, 1)

        self.findButton = QPushButton('search', self)
        self.findButton.setMaximumSize(150, 40)
        self.findButton.setFont(QFont("Roman times", 10, QFont.Bold))
        self.findButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.findButton, 1, 0, 1, 1)

        self.quitButton = QPushButton('exit', self)
        self.quitButton.setMaximumSize(150, 40)
        self.quitButton.setFont(QFont("Roman times", 10, QFont.Bold))
        self.quitButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.quitButton, 1, 1, 1, 1)

        self.findButton.clicked.connect(self.search_authors)
        self.quitButton.clicked.connect(self.close)

        self.picture = QPixmap("DBLP_Logo_320x120.png")
        self.lb1 = QLabel(self)
        self.lb1.setPixmap(self.picture)
        self.layout.addWidget(self.lb1, 2, 0, 1, 2)

        self.setWindowTitle('Icon')
        self.setWindowTitle('search for scientists')
        self.setLayout(self.layout)

        self.show()

    def search_authors(self):
        url = 'https://dblp.org/search?q=' + self.textbox.text().replace(' ', '%20')
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
                for author_name in authors.find_all('span', itemprop='name'):
                    author_dict[author_name.text] = link

        show_authors = Show_authors_list()
        show_authors.show1(author_dict)


class Show_authors_list(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 500)
        self.layout = QGridLayout()
        self.palette = QPalette()
        self.pix = QPixmap("background_1.png")
        self.pix = self.pix.scaled(self.width(), self.height())
        self.palette.setBrush(QPalette.Background, QBrush(self.pix))
        self.setPalette(self.palette)

    def show1(self, author_dict):
        self.layout.setSpacing(len(author_dict))
        self.author_dict = author_dict
        self.setWindowTitle('select the right one')

        self.lb = QLabel(self)
        self.lb.setText('possible results:')
        self.lb.setFont(QFont("Roman times", 12, QFont.Bold))
        self.lb.setMaximumSize(250, 40)
        self.layout.addWidget(self.lb, 0, 0, 1, 2)
        hh = 1

        for key, value in author_dict.items():
            self.showButton = QPushButton(key, self)
            self.showButton.setMaximumSize(200, 40)
            self.showButton.setFont(QFont("Roman times", 11, QFont.Bold))
            self.showButton.clicked.connect(partial(self.get_articles, value))  # lambda->partial
            self.layout.addWidget(self.showButton, hh, 0, 1, 1)

            self.saveButton = QPushButton("save to file", self)
            self.saveButton.setMaximumSize(200, 40)
            self.saveButton.setFont(QFont("Roman times", 11, QFont.Bold))
            self.saveButton.clicked.connect(partial(self.save_csv, value))
            self.layout.addWidget(self.saveButton, hh, 1, 1, 1)
            hh = hh+1

        self.setLayout(self.layout)

        self.show()

    def get_basic_info(self, link_author):
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
                article_title.append(title1.get_text())

        self.sum_records = len(article_title)
        self.article_title = article_title
        self.year_published = year_published
        self.link_article = link_article
        self.venues = venues

    def get_articles(self, link_author):
        self.get_basic_info(link_author)
        print('The total number of articles is {}'.format(self.sum_records))

        # avoid crashing
        self.table = Table()
        self.table.show2(article_title=self.article_title, sum_records=self.sum_records,
                         year_published=self.year_published, link_article=self.link_article, venues=self.venues)

    def save_csv(self, link_author):
        self.get_basic_info(link_author)

        filepath, type = QFileDialog.getSaveFileName(self, "save file", "/", 'csv(*.csv)')
        print(filepath)
        with open(filepath, "a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')

            for i in range(self.sum_records):
                info_sum = []
                info_sum.append(self.article_title[i])
                info_sum.append(self.year_published[i])
                info_sum.append(self.link_article[i])
                info_sum.append(self.venues[i])

                writer.writerow(info_sum)


class Table(QWidget):
    def __init__(self):
        super().__init__()
        self.palette = QPalette()
        self.pix = QPixmap("ligt_green.jpg")
        self.pix = self.pix.scaled(self.width(), self.height())
        self.palette.setBrush(QPalette.Background, QBrush(self.pix))
        self.setPalette(self.palette)

    def show2(self, article_title, sum_records, year_published, link_article, venues):
        self.setWindowTitle("论文信息")
        self.resize(800, 600)
        self.model = QStandardItemModel(1, 4)
        self.model.setHorizontalHeaderLabels(['论文标题', '发表日期', '下载链接', '发表位置'])
        for row in range(sum_records):
            for column in range(4):
                if column == 0:
                    item = QStandardItem(article_title[row])
                if column == 1:
                    item = QStandardItem(year_published[row])
                if column == 2:
                    item = QStandardItem(link_article[row])
                if column == 3:
                    item = QStandardItem(venues[row])
                self.model.setItem(row, column, item)
        self.tableView = QTableView()
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        dlgLayout = QVBoxLayout()
        dlgLayout.addWidget(self.tableView)
        self.setLayout(dlgLayout)

        self.show()
