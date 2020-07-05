import pymysql


# 插入内部人员信息
def insert():
    ID_number = input('身份证号:')
    full_name = input('姓名:')

    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root",
                           password="166384", database="library", charset="utf8")

    cursor = conn.cursor()

    SQL = 'INSERT INTO internal_staff (ID_number,full_name) VALUES (%s,%s);'
    data = [ID_number, full_name]

    cursor.execute(SQL, data)

    conn.commit()

    cursor.close()

    conn.close()


# 删除内部人员信息
def delete():
    ID_number = input('身份证号:')

    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root",
                           password="166384", database="library", charset="utf8")

    cursor = conn.cursor()

    SQL = 'DELETE FROM internal_staff WHERE ID_number=%s;'
    data = [ID_number]

    cursor.execute(SQL, data)

    conn.commit()

    cursor.close()

    conn.close()


# 登记外部人员信息
def register():
    # 内部人员标志
    internal = False
    ID_number = input('身份证号:')
    full_name = input('姓名:')

    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root",
                           password="166384", database="library", charset="utf8")

    cursor = conn.cursor()
    # 判断登记的是否为内部人员
    SQL = 'SELECT * FROM internal_staff WHERE ID_number=%s;'
    data = [ID_number]

    result = cursor.execute(SQL, data)
    # 如果是内部人员,则无需交押金
    if result != 0:
        internal = True
        return internal, ID_number
    else:
        # 判断外部人员是否已交押金
        SQL = 'SELECT * FROM external_staff WHERE ID_number=%s;'
        data = [ID_number]

        result = cursor.execute(SQL, data)
        # 如果已交押金,则无需再交
        if result != 0:
            return internal, ID_number
        else:
            # 交押金
            deposit = input('按Y键交押金,按N键不交\n>')
            # 如果交押金,则登记成功
            if deposit == 'y' or deposit == 'Y':
                print('已交押金')

                SQL = 'INSERT INTO external_staff (ID_number,full_name) VALUES (%s,%s)'
                data = [ID_number, full_name]

                cursor.execute(SQL, data)

                conn.commit()

                cursor.close()

                conn.close()
                return internal, ID_number
            # 如果不交押金,则必须交押金
            elif deposit == 'n' or deposit == 'N':
                while deposit != 'y' and deposit != 'Y':
                    deposit = input('未交押金,请按Y键交押金\n>')
                    if deposit == 'y' or deposit == 'Y':
                        print('已交押金')
                        
                        SQL = 'INSERT INTO external_staff (ID_number,full_name) VALUES (%s,%s)'
                        data = [ID_number, full_name]

                        cursor.execute(SQL, data)

                        conn.commit()

                        cursor.close()

                        conn.close()
                        return internal, ID_number
