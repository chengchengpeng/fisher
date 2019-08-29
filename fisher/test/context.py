
# from flask import Flask, current_app
# app = Flask(__name__)
# # cex = app.app_context()
# # cex.push()
# with app.app_context():
#     a = current_app
#     b = current_app.config['DEBUG']
# with语句用于实现了上下文协议的对象，这样的对象称为上下文管理器，实现了__enter__和__exit__方法的对象称为上下文管理器
from contextlib import contextmanager


class MyResource():
    # def __enter__(self):
    #     print('connect')
    #     return self
    #
    # def __exit__(self, exc_type, exc_value, tb):
    #     print('close')

    def query(self):
        print('data')

#
# with MyResource() as resource:
#     resource.query()

#
# @contextmanager
# def context_test():
#     print('this is starting!')
# yield后面返回的是as 后面的 r
#     yield MyResource()
#     print('this is ending')
#
#
# with context_test() as r:
#     r.query()


@contextmanager
def context_test():
    print('<<', end='')
    yield
    print('>>')


with context_test():
    print('且将生活一饮而尽', end='' )
