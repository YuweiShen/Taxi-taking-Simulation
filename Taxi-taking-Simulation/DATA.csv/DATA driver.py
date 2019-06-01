import MySQLdb
import csv

db=MySQLdb.connect

fp="C:/Users/user/Desktop/大作业/滴答打车/DATA.csv/DATA driver.csv"
datacsv=csv.reader(open(fp,encoding='gbk'))
db=MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        password='region123',
        db='dida',
        charset='gbk')
cursor = db.cursor()
cursor.execute("use dida;")

format_str="""INSERT INTO driver(name,phone,carno,acctbal, log,lat,stat)
              VALUES('{name}','{phone}','{carno}',100,{log},{lat},0)"""
for p in datacsv:
        sql_command = format_str.format(name=p[0],carno=p[1],phone=p[2],log=p[3],lat=p[4])
        try:
            cursor.execute(sql_command)
            db.commit()
        except:
            db.rollback()

sql = """SELECT* FROM driver;"""
try:
    cursor.execute(sql)
    results=cursor.fetchall()
    for row in results:
        name = row[0]
        phone = row[1]
        carno = row[2]
        acctbal = row[3]
        log = row[4]
        lat = row[5]
        stat = row[6]
        print(name,phone,acctbal,log,lat,stat)
except:
    print("Error:unable to fetch data")

db.close()