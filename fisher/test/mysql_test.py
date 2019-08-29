import MySQLdb
try:
    conn = MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        passwd='12345678',
        db='news',
        port=3306,
        charset='utf8'
        )

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM `news`;')
    rest = cursor.fetchone()
    print(rest)
    conn.close
except MySQLdb.Error as e:
    print('Error: %s' % e)
