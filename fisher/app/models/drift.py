# 对于信息的记录，不要模型的关联
# 对于状态的表示。可以用枚举
from sqlalchemy import Integer, Column, String, SmallInteger

from app.libs.enums import PendingStatus
from app.models.base import Base


class Drift(Base):
    id = Column(Integer, primary_key=True)

    # 邮寄信息
    recipient_name = Column(String(20), nallable=False)
    address = Column(String(100), nullable=False)
    message =   Column(String(200))
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # 请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    # 赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifer_nickname = Column(String(20))

    _pending = Column('pending', SmallInteger, default=1)

    @property
    def pending(self):
        return PendingStatus(self._pending)

    # 写入属性
    @pending.setter
    def pending(self, status):
        self._pending = status.value
