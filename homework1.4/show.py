from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from functools import partial
import csv
from utils import *
from utils import *


class CrawlWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.lb = QLabel(self)
        self.lb.setGeometry(20, 25, 140, 40)
        self.lb.setText('Scientist name：')
        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(160, 30, 130, 30)
        self.findButton = QPushButton('search', self)
        self.findButton.setGeometry(60, 85, 100, 40)
        self.quitButton = QPushButton('exit', self)
        self.quitButton.clicked.connect(self.close)
        self.findButton.clicked.connect(self.search_authors)
        self.quitButton.setGeometry(190, 85, 100, 40)
        self.setGeometry(500, 300, 650, 450)
        self.setWindowTitle('Icon')
        self.setWindowTitle('search for scientists')
        self.setWindowIcon(QIcon('weather.png'))

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
                # print(link)
                for author_name in authors.find_all('span', itemprop='name'):
                    author_dict[author_name.text] = link

        show_authors = Show_authors_list()
        show_authors.show1(author_dict)


class Show_authors_list(QWidget):
    def show1(self, author_dict):
        self.author_dict = author_dict
        self.setWindowTitle('select the right one')
        self.setWindowIcon(QIcon('weather.png'))
        self.setGeometry(500, 300, 650, 550)
        self.lb = QLabel(self)
        self.lb.setGeometry(30, 25, 160, 40)
        self.lb.setText('possible results:')
        pos = 70

        for key, value in author_dict.items():
            self.findButton = QPushButton(key, self)
            self.findButton.setGeometry(100, pos, 150, 40)
            self.findButton.clicked.connect(partial(self.get_articles, value))  # 踩坑，connect用法,lambda->partial

            self.findButton = QPushButton("push to save directly", self)
            self.findButton.setGeometry(280, pos, 250, 40)
            self.findButton.clicked.connect(partial(self.save_csv, value))
            pos = pos+45

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
                # new_str = title1.get_text()
                article_title.append(title1.get_text())
                # print(str(i) + ':' + title1.get_text())

        self.sum_records = len(article_title)
        self.article_title = article_title
        self.year_published = year_published
        self.link_article = link_article
        self.venues = venues

    def get_articles(self, link_author):
        self.get_basic_info(link_author)  # 调用自己类的方法！！
        print('The total number of articles is {}'.format(self.sum_records))

        # 防止窗口闪退，需要成为全局变量
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
    def show2(self, article_title, sum_records, year_published, link_article, venues):
        self.setWindowTitle("论文信息")
        self.resize(800, 600)
        self.model = QStandardItemModel(4, 4)
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


"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    find_authors = CrawlWindow()
    # show_authors = Show_authors_list()
    # article_title = ['a', 'b', 'c', 'd']
    # table = Table()
    # table.show2(article_title, 4)

    sys.exit(app.exec())
"""
