"""
用于实现对dblp上科学家的搜索，获取其所有文章的名称。
已实现基本功能，还需添加每年的数量图表，存入文件，判断搜索出的结果中哪个是需要查找的目标等功能
分开统计年份，作者，论文链接，发表的期刊会议，最后再匹配。
可视化：输入搜索，按键选择，输出信息到表格展示
可通过点击按钮保存
如何美化pyqt做出的界面？添加图片等等？
如何调整函数的布局
"""
import sys
from utils import *
from show import *
"""
# q = 'Ya-Qin%20Zhang'
q = 'houqiang li'
q.replace(' ', '%20')
articles1 = ScienceArticles(q)
authors_dict = articles1.search_authors()
articles1.get_articles(authors_dict['Houqiang Li'])
"""
app = QApplication(sys.argv)
find_authors = CrawlWindow()
sys.exit(app.exec())
