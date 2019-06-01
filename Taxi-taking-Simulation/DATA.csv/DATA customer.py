import MySQLdb
import csv

db=MySQLdb.connect

fp="C:/Users/user/Desktop/大作业/滴答打车/DATA.csv/DATA customer.csv"
datacsv=csv.reader(open(fp,encoding='gbk'))
db=MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        password='region123',
        db='dida',
        charset='gbk')
cursor = db.cursor()
cursor.execute("use dida;")

format_str="""INSERT INTO customer(name,phone,acctbal, log,lat,stat)
              VALUES('{name}','{phone}',100,{log},{lat},0)"""
for p in datacsv:
        sql_command = format_str.format(name=p[0],phone=p[1],log=p[2],lat=p[3])
        try:
            cursor.execute(sql_command)
            db.commit()
        except:
            db.rollback()

sql = """SELECT* FROM customer;"""
try:
    cursor.execute(sql)
    results=cursor.fetchall()
    for row in results:
        name = row[0]
        phone = row[1]
        acctbal = row[2]
        log = row[3]
        lat = row[4]
        stat = row[5]
        print(name,phone,acctbal,log,lat,stat)
except:
    print("Error:unable to fetch data")

db.close()