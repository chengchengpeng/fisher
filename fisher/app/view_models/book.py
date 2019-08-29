# filter:第一个参数为函数，传入一个参数，函数返回结果为真，保留该参数，filter第二个参数为集合，为函数提供参数
# reuce:第一个参数，传入一个函数，函数有两个参数，将这两个参数执行函数操作，两个参数来源于第二个reduce参数，第二个参数为集合，函数的结果和下一个列表元素为函数的两个参数
# map:将第二个参数集合的元素通过第一个参数的函数映射到一个新的集合中
# @property 将函数转为能用属性方式调用的函数
# join函数'符号'.join(列表),用符号连接集合内的元素
# 如果是单页面，就将数据结果返回客服端在处理
# 对于前端代码不好处理的，可以在后台编写一个函数


class BookViewModel:
    def __init__(self, book):
        self.title = book['title']
        self.publisher = ['publisher']
        self.author = '-'.join(book['author'])
        self.image = book['image']
        self.price = book['price']
        self.isbn = book['isbn']
        self.summary = book['summary']
        self.pages = book['page']
        self.pubdate = book['pubdate']
        self.binding = book['binging']

    @property
    def intor(self):
        intors = filter(lambda x: True if x else False, [self.author, self.price, self.publisher])
        return '/'.join(intors)


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]


class _BookViewModel:
    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'book': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = 1
        returned['book'] = [cls._cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'book': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = data['total']
            returned['book'] = [cls._cut_book_data(book) for book in data['books']]

    @classmethod
    def __cut__book__data(cls, data):
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'page': data['page'] or '',
            'author': '-'.join(data['author']),
            'price': data['price'],
            'summary': data['summary'] or ' ',
            'image': data['image']
        }
        return book