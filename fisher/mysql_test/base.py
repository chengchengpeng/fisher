# import MySQLdb
# class MysqlSearch(object):
#     def __init__(self):
#         self.get_conn()
#     def get_conn(self):
#         try:
#             self.conn = MySQLdb.connect(
#                 host='127.0.0.1',
#                 user='root',
#                 passwd='12345678',
#                 db='news',
#                 port=3306,
#                 charset='utf8'
#             )
#
#         except MySQLdb.Error as e:
#             print('Error: %s' % e)
#
#     def closer_conn(self):
#         try:
#             if self.conn:
#                 self.conn.close()
#         except MySQLdb.Error as e:
#             print('Error: %s' % e)
