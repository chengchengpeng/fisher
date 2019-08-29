# Boolean 但一个元素是False或者True时用这个类型
# 当两个模型是多对多的关系，需要第三个模型
# relationship()这个函数提供引用关系
# ForeignKey()这个函数可以表明此表的属性是关联表的哪一个属性
"""从数据库中取有序的限定数量的不重复数据，先分组，分组用函数group_by()，然后排序，再限定,排序用函数order_by()接受一个可用于排序的参数，desc()决定顺序还是逆序，
限定用函数limit()接受限定数目为参数，最后使用distinct()函数去重
"""
# current_user.id 是使用了插件flask_login后用来取登录用户id的
# 在数据表中查询出模型用filter_by()
"""需要跨表查询使用db.session方便，在这里，用到了数据表中查寻模型的数量用db,session.query(),query()传入两个参数，第一个为对应的数量，第二个为那个属性对应的数量，
sqlalchemy里面有个func,func下面有个函数count(),函数借收一个参数，表示用该参数有多少个不同的，就返回整数多少
用filter查询数据库接受的参数是一组表达式，Wish.isbn.in_(isbn_list)表示只要Wish.isbn在列表isbn_list中，就将这个isbn的模型全部查询出来，in_是关键字
"""
# group_by()与func.count()连用在数据库中叫分组统计
from flask import current_app

from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship


from app.spider.yushu_book import YushuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey(user.id))
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey(book.id))
    launched = Column(Boolean, default=False)

    @classmethod
    def resent(cls):
        recent_gift = Gift.query.filter_by(
            launched=False).group_by(Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift

    @property
    def book(self):
        yushu_book = YushuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).oreder_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    def is_youself_gift(self, uid):
        return True if uid == self.uid else False
    #
    #     # @property
    #     # def summary(self):
    #     #     return dict(
    #     #         nickname=self.nickname,
    #     #         beans=self.beans,
    #     #         email=self.email,
    #     #         send_receive=str(self.seng_counter)
    #     #     )