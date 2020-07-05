DROP SCHEMA IF EXISTS library;
CREATE SCHEMA IF NOT EXISTS library;

USE library;

CREATE TABLE IF NOT EXISTS book (
    ISBN CHAR(13),
    book_name CHAR(20),
    press CHAR(20),
    author CHAR(20),
    book_classification CHAR(20),
    year_of_publication CHAR(4),
    remaining_quantity INT
);

INSERT INTO book (ISBN,book_name,press,author,book_classification,year_of_publication,remaining_quantity) VALUES ('9787040406641','数据库系统概论','高等教育出版社','萨师煊','数据库','2014',30);
INSERT INTO book (ISBN,book_name,press,author,book_classification,year_of_publication,remaining_quantity) VALUES ('9787040174014','信号与线性系统分析','高等教育出版社','吴大正','信号与系统','2005',50);
INSERT INTO book (ISBN,book_name,press,author,book_classification,year_of_publication,remaining_quantity) VALUES ('9787560605814','微型计算机原理及应用','西安电子科技大学出版社','李伯成','微机原理','2008',40);

CREATE TABLE IF NOT EXISTS borrowing (
    internal BOOLEAN,
    ISBN CHAR(13),
    ID_number CHAR(20),
    borrow_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    return_time TIMESTAMP,
    fine INT DEFAULT 0
);

INSERT INTO borrowing (internal,ISBN,ID_number,borrow_time) VALUES (TRUE,9787040406641,18180100068, 20200520131420);

CREATE TABLE IF NOT EXISTS internal_staff (
    ID_number CHAR(18),
    full_name CHAR(20),
    number_of_books_borrowed INT DEFAULT 0,
    overdue INT DEFAULT 0
);

INSERT INTO internal_staff (ID_number,full_name) VALUES ('18180100068','徐霆泽');
INSERT INTO internal_staff (ID_number,full_name,number_of_books_borrowed) VALUES ('12345','翔哥',5);
INSERT INTO internal_staff (ID_number,full_name,overdue) VALUES ('114514','先辈',1);

CREATE TABLE IF NOT EXISTS external_staff (
    ID_number CHAR(18),
    full_name CHAR(20),
    number_of_books_borrowed INT DEFAULT 0,
    overdue INT DEFAULT 0
);
