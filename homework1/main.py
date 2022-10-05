"""
用于实现对dblp上科学家的搜索，获取其所有文章的名称。
已实现基本功能，还需添加每年的数量图表，存入文件，判断搜索出的结果中哪个是需要查找的目标等功能
"""
from utils import *

q = 'Ya-Qin%20Zhang'
articles1 = ScienceArticles(q)
authors_dict = articles1.search_authors()
articles1.get_articles(authors_dict['Ya-Qin Zhang'])
