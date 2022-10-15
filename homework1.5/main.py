"""
Author: xinlei yin
date:2022_10_15
function: get some information from dblp
"""
import sys
from utils import *

app = QApplication(sys.argv)
find_authors = CrawlWindow()
sys.exit(app.exec())
