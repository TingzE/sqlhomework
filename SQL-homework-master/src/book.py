# 导入pymysql模块
import pymysql


# 插入图书信息
def insert():
    ISBN = input('ISBN:')
    book_name = input('图书名:')
    press = input('出版社:')
    author = input('作者:')
    book_classification = input('图书分类:')
    year_of_publication = input('出版年份:')
    remaining_quantity = input('剩余数量:')
    # 连接数据库
    conn = pymysql.connect(host="127.0.0.1",    # IP地址
                           port=3306,  # 端口(不是字符串,不需要加引号)
                           user="root",    # 用户名
                           password="166384",   # 密码
                           database="library",  # 数据库名
                           charset="utf8")
    # 得到一个可以执行SQL语句的光标对象
    # 执行完毕返回的结果集默认以元组显示
    cursor = conn.cursor()
    # 定义要执行的SQL语句
    SQL = 'INSERT INTO book (ISBN,book_name,press,author,book_classification,year_of_publication,remaining_quantity) VALUES (%s,%s,%s,%s,%s,%s,%s);'
    data = [ISBN, book_name, press, author, book_classification,
            year_of_publication, remaining_quantity]
    # 执行SQL语句
    cursor.execute(SQL, data)
    # 涉及写操作要注意提交
    conn.commit()
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()


# 修改图书信息
def update():
    ISBN = input('ISBN:')
    remaining_quantity = input('剩余数量:')

    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root",
                           password="166384", database="library", charset="utf8")

    cursor = conn.cursor()

    SQL = 'UPDATE book SET remaining_quantity=%s WHERE ISBN=%s;'
    data = [remaining_quantity, ISBN]

    cursor.execute(SQL, data)

    conn.commit()

    cursor.close()

    conn.close()


# 删除图书信息
def delete():
    ISBN = input('ISBN:')

    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root",
                           password="166384", database="library", charset="utf8")

    cursor = conn.cursor()

    SQL = 'DELETE FROM book WHERE ISBN=%s;'
    data = [ISBN]

    cursor.execute(SQL, data)

    conn.commit()

    cursor.close()

    conn.close()


# 查询图书信息
def select():
    info = input('请查询图书信息:')

    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root",
                           password="166384", database="library", charset="utf8")

    cursor = conn.cursor()

    SQL = 'SELECT * FROM book WHERE ISBN=%s OR book_name=%s OR press=%s OR author=%s OR book_classification=%s OR year_of_publication=%s;'
    data = [info, info, info, info, info, info]

    cursor.execute(SQL, data)
    # 取出所有查询结果
    results = cursor.fetchall()
    for result in results:
        print(result)

    cursor.close()

    conn.close()
