'''from mysql_test.base import MysqlSearch
MysqlSearch = MysqlSearch()

def get_more():
    # sql = 'SELECT *  FROM `news` WHERE `types` = %s;'
    sql = 'SELECT id  FROM `news` WHERE `types` = %s ORDER BY `id` DESC LIMIT 2,3;'
    cursor = MysqlSearch.conn.cursor()
    cursor.execute(sql, ('小说',))
    # 打印行数
    # print(cursor.rowcount)
    # print(cursor.description)
    # print(type(cursor.fetchall()))

    rest = [dict(zip([k[0] for k in cursor.description], row))
            for row in cursor.fetchall()]

    # k = [ for k in cursor.description]
    # print(type(k))

    # print(k[0])
    # rest = cursor.fetchone()
    # print(rest['title'])
    # print(rest)
    cursor.close()
    MysqlSearch.closer_conn()
    return rest


def main():
    # result = obj.get_one()
    # print(result['title'])
    result = get_more()
    print(result)


if __name__ == '__main__':
    main()'''