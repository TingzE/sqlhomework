import pymysql
import staff


# 查询借书记录
def select():
    ID_number = staff.register()[-1]

    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root",
                           password="166384", database="library", charset="utf8")

    cursor = conn.cursor()

    SQL = 'SELECT * FROM borrowing WHERE ID_number=%s;'
    data = [ID_number]

    cursor.execute(SQL, data)

    results = cursor.fetchall()
    for result in results:
        print(result)

    cursor.close()

    conn.close()


# 借书
def borrow():
    # 登记
    internal, ID_number = staff.register()

    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root",
                           password="166384", database="library", charset="utf8")

    cursor = conn.cursor()
    # 判断是否有超期书籍
    if internal == True:
        SQL = 'SELECT overdue FROM internal_staff WHERE ID_number=%s;'
    else:
        SQL = 'SELECT overdue FROM external_staff WHERE ID_number=%s;'
    data = [ID_number]

    cursor.execute(SQL, data)
    # 取一条
    result = cursor.fetchone()
    # 如果有,则不让借新的
    if result[-1] > 0:
        print('你有超期书籍,不让借新的')
        return
    # 限制在借数量
    if internal == True:
        SQL = 'SELECT number_of_books_borrowed FROM internal_staff WHERE ID_number=%s;'
        data = [ID_number]

        cursor.execute(SQL, data)

        result = cursor.fetchone()
        # 内部人员限制为5本
        if result[-1] >= 5:
            print('您的借书限制为5本')
            return
    else:
        SQL = 'SELECT number_of_books_borrowed FROM external_staff WHERE ID_number=%s;'
        data = [ID_number]

        cursor.execute(SQL, data)

        result = cursor.fetchone()
        # 外部人员限制为2本
        if result[-1] >= 2:
            print('您的借书限制为2本')
            return
    # 借书
    ISBN = input('ISBN:')
    # 登记到借书记录
    SQL = 'INSERT INTO borrowing (internal,ID_number,ISBN) VALUES (%s,%s,%s);'
    data = [internal, ID_number, ISBN]

    cursor.execute(SQL, data)
    # 修改图书数量
    SQL = 'UPDATE book SET remaining_quantity=book.remaining_quantity-1 WHERE ISBN=%s;'
    data = [ISBN]

    cursor.execute(SQL, data)
    # 修改在借数量
    if internal == True:
        SQL = 'UPDATE internal_staff SET number_of_books_borrowed=internal_staff.number_of_books_borrowed+1 WHERE ID_number=%s'
    else:
        SQL = 'UPDATE external_staff SET number_of_books_borrowed=external_staff.number_of_books_borrowed+1 WHERE ID_number=%s'
    data = [ID_number]

    cursor.execute(SQL, data)

    conn.commit()

    cursor.close()

    conn.close()


# 还书
def back():
    internal, ID_number = staff.register()

    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root",
                           password="166384", database="library", charset="utf8")

    cursor = conn.cursor()

    ISBN = input('ISBN:')
    # 获取还书时间戳
    SQL = 'UPDATE borrowing SET return_time=CURRENT_TIME WHERE ISBN=%s AND ID_number=%s;'
    data = [ISBN, ID_number]

    cursor.execute(SQL, data)

    SQL = 'SELECT borrow_time FROM borrowing WHERE ISBN=%s AND ID_number=%s;'
    data = [ISBN, ID_number]

    cursor.execute(SQL, data)

    borrow_time = cursor.fetchone()

    SQL = 'SELECT return_time FROM borrowing WHERE ISBN=%s AND ID_number=%s;'
    data = [ISBN, ID_number]

    cursor.execute(SQL, data)

    return_time = cursor.fetchone()
    # 计算借书时间
    SQL = 'SELECT TIMESTAMPDIFF(DAY,%s,%s);'
    data = [borrow_time[-1], return_time[-1]]

    cursor.execute(SQL, data)

    result = cursor.fetchone()
    # 超期收取罚金
    # 内部人员1元/天
    if result[-1] > 30:
        overdue = result[-1] - 30
        fine = overdue
        # 外部人员3元/天
        if internal == False:
            fine = overdue * 3
        print(f'超期{overdue}天,罚金{fine}元')
        # 登记到借书记录
        SQL = 'UPDATE borrowing SET fine=%s WHERE ISBN=%s AND ID_number=%s;'
        data = [fine, ISBN, ID_number]

        cursor.execute(SQL, data)
    # 修改图书数量
    SQL = 'UPDATE book SET remaining_quantity=book.remaining_quantity+1 WHERE ISBN=%s;'
    data = [ISBN]

    cursor.execute(SQL, data)
    # 修改在借数量
    if internal == True:
        SQL = 'UPDATE internal_staff SET number_of_books_borrowed=internal_staff.number_of_books_borrowed-1 WHERE ID_number=%s'
    else:
        SQL = 'UPDATE external_staff SET number_of_books_borrowed=external_staff.number_of_books_borrowed-1 WHERE ID_number=%s'
    data = [ID_number]

    cursor.execute(SQL, data)
    # 如果外部人员没有在借书籍,则取消登记
    SQL = 'DELETE FROM external_staff WHERE number_of_books_borrowed=0;'

    cursor.execute(SQL)

    conn.commit()

    cursor.close()

    conn.close()
