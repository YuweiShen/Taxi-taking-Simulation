import MySQLdb as ms
import pandas as pd
from globaliterm import *

global_srcDB_Host = '127.0.0.1'
global_srcDB_User = 'root'
global_srcDB_PWD = ''
global_srcDB_DB = 'dida'


class MySQL:
    """Connection to a MySQL"""

    connection = None
    cursor = None

    # def __init__(self,user='',password='',database='',charset=None,port=3306):
    def __init__(self):
        self.connection = ms.connect(host=global_srcDB_Host,
                                     user=global_srcDB_User,
                                     passwd=global_srcDB_PWD,
                                     db=global_srcDB_DB)
        self.cursor = self.connection.cursor()

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
        except (AttributeError, ms.OperationalError):
            self.connection()
            self.cursor.execute(sql)
        return self.cursor

    def close(self):
        if (self.cursor):
            self.cursor.close()
        self.connection.commit()
        self.connection.close()


def initialization():
    sql = 'SET sql_safe_updates=0; update driver set stat=0; update customer set stat=0 ;' \
            'update customer set acctbal=100;delete from orders; commit;'
    db = MySQL()
    db.execute(sql)


# 从数据库获得司机的所有信息
def get_dlist():
    sql = 'select name,acctbal,stat,phone from driver;'
    db = MySQL()
    db.execute(sql)
    l=db.cursor.fetchall()
    l=list(l)
    l=pd.DataFrame(l)
    l.columns=["name","acctbal","stat","phone"]
    return l


# 从数据库获得乘客的所有信息
def get_clist():
    sql='select name,acctbal,stat,phone from customer;'
    db = MySQL()
    db.execute(sql)
    l=db.cursor.fetchall()
    l=list(l)
    l=pd.DataFrame(l)
    l.columns=["name","acctbal","stat","phone"]
    return l


# 修改mysql和实体的值
def refresh(objectslist, canshu, value, phonenum):
    for x in objectslist:
        if x.phone == phonenum:
            if canshu == 'acctbal':
                x.acctbal = round(value, 1)
            elif canshu == 'state':
                x.state = round(value, 1)

    if objectslist == global_var.objectscust:

        mysql = "update customer set {can}={zhi} where phone='{phone}'"
        sql = mysql.format(can=canshu, zhi=value, phone=phonenum)
        db = MySQL()
        db.execute(sql)
        db.connection.commit()

    elif objectslist == global_var.objectscar:
        mysql = "update driver set {can}={zhi} where phone='{phone}'"
        sql = mysql.format(can=canshu, zhi=value, phone=phonenum)
        db = MySQL()
        db.execute(sql)
        db.connection.commit()


# 10秒钟向数据库传递一下人和车的位置
def transmit():
    for car in global_var.objectscar:
        sql1 = 'update driver set log={x}  where phone={p};'
        sql2 = 'update driver set lat ={y} where phone={p};'
        sql1_command = sql1.format(x=car.log, y=car.lat, p=car.phone)
        sql2_command = sql2.format(x=car.log, y=car.lat, p=car.phone)
        db = MySQL()
        try:
            db.execute(sql1_command)
            db.connection.commit()
            db.execute(sql2_command)
            db.connection.commit()
        except:
            db.connection.rollback()

    for cust in global_var.objectscust:
        sql1 = 'update customer set log={x} where phone={p};'
        sql2 = 'update customer set lat={y} where phone={p};'
        sql1_command = sql1.format(x=cust.log, y=cust.lat, p=cust.phone)
        sql2_command = sql2.format(x=cust.log, y=cust.lat, p=cust.phone)
        db = MySQL()
        try:
            db.execute(sql1_command)
            db.connection.commit()
            db.execute(sql2_command)
            db.connection.commit()
        except:
            db.connection.rollback()