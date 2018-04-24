# coding= utf-8
#MySQL测试

import pymysql
# 打开数据库连接
db = pymysql.connect("localhost", "pandeku", "pandeku", "django_stu_info", charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute() 方法执行 SQL 查询
cursor.execute("SELECT VERSION()")
# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()
print("Database version : %s " % data)
# 关闭数据库连接
db.close()


# #删表与建表
import pymysql
# 打开数据库连接
db = pymysql.connect("localhost", "pandeku", "pandeku", "django_stu_info", charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute() 方法执行 SQL，如果表存在则删除
cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
# 使用预处理语句创建表
sql = """CREATE TABLE EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,
         SEX CHAR(1),
         INCOME FLOAT )"""
cursor.execute(sql)
# 关闭数据库连接
db.close()

# 插入表1
import pymysql
# 打开数据库连接
db = pymysql.connect("localhost", "pandeku", "pandeku", "django_stu_info", charset='utf8')
# 使用cursor()方法获取操作游标
cursor = db.cursor()
# SQL 插入语句
sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
         LAST_NAME, AGE, SEX, INCOME)
         VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
try:
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
except:
    # 如果发生错误则回滚
    db.rollback()
# 关闭数据库连接
db.close()

#插入表2
import pymysql
# 打开数据库连接
db = db = pymysql.connect("localhost", "pandeku", "pandeku", "django_stu_info", charset='utf8')
# 使用cursor()方法获取操作游标
cursor = db.cursor()
# SQL 插入语句
sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
       LAST_NAME, AGE, SEX, INCOME) \
       VALUES ('%s', '%s', '%d', '%c', '%d' )" % \
      ('Mac', 'Mohan', 20, 'M', 2000)
try:
    # 执行sql语句
    cursor.execute(sql)
    # 执行sql语句
    db.commit()
except:
    # 发生错误时回滚
    db.rollback()

# 关闭数据库连接
db.close()


# #查询

# Python查询Mysql使用 fetchone() 方法获取单条数据, 使用fetchall() 方法获取多条数据。
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "pandeku", "pandeku", "django_stu_info", charset='utf8')
# 使用cursor()方法获取操作游标
cursor = db.cursor()
# SQL 查询语句
sql = "SELECT * FROM login_user"
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
        name = row[0]
        # 打印结果
        print("fname=%s" % name)
except:
    print("Error: unable to fetch data")
# 关闭数据库连接
db.close()



#数据库更新操作
import pymysql
# 打开数据库连接
db = pymysql.connect("localhost", "pandeku", "pandeku", "django_stu_info", charset='utf8')
# 使用cursor()方法获取操作游标
cursor = db.cursor()
# SQL 更新语句
sql = "UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = '%c'" % ('M')
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
except:
    # 发生错误时回滚
    db.rollback()
# 关闭数据库连接
db.close()


# #数据库删除操作
import pymysql
# 打开数据库连接
db = pymysql.connect("localhost", "pandeku", "pandeku", "django_stu_info", charset='utf8')
# 使用cursor()方法获取操作游标
cursor = db.cursor()
# SQL 删除语句
sql = "DELETE FROM EMPLOYEE WHERE AGE > '%d'" % (20)
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 提交修改
    db.commit()
except:
    # 发生错误时回滚
    db.rollback()
# 关闭连接
db.close()