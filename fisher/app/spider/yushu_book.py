# str.format(): 参数字符串填充str里的{}.详情见test.format_test
# list.append() 将参数填充到列表中
# 代码需要提供良好的接口，对于外部需要使用的类的属性，可以编写一个函数在类里面封装好
from app.libs.httper import HTTP
from flask import current_app

class YushuBook:
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)

    def __fill_single(self, data):
         if data:
             self.total = 1
             self.books.append(data)

    def __fill_collection(self,data):
        self.total = data['total']
        self.books = data['books']

    def search_by_keyword(self, keyword, page = 1):
        url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'],
                                     self.calculate_start(page))
        result = HTTP.get(url)
        self.__fill_collection(result)

    def calculate_start(self, page):
        return (page - 1) * current_app.config['PER_PAGE']

    @property
    def first(self):
        return self.book[0] if self.total > 0 else None
