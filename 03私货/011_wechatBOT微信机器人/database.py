#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('test.db')
print("数据库打开成功")
c = conn.cursor()
c.execute('''CREATE TABLE COMPANY
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL,
       PASSWORD        CHAR(50));''')
print("数据表创建成功")
conn.commit()
conn.close()
