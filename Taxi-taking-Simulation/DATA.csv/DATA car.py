import MySQLdb
import csv

db=MySQLdb.connect

fp="C:/Users/user/Desktop/大作业/滴答打车/DATA.csv/DATA car.csv"
datacsv=csv.reader(open(fp,encoding='gbk'))
db=MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        password='region123',
        db='dida',
        charset='gbk')
cursor = db.cursor()
cursor.execute("use dida;")

format_str="""INSERT INTO car(carno,cartype,carcol)
              VALUES('{carno}','{cartype}','{carcol}')"""
for p in datacsv:
        sql_command = format_str.format(carno=p[0],cartype=p[1],carcol=p[2])
        try:
            cursor.execute(sql_command)
            db.commit()
        except:
            db.rollback()

sql = """SELECT* FROM car;"""
try:
    cursor.execute(sql)
    results=cursor.fetchall()
    for row in results:
        carno = row[0]
        cartype = row[1]
        carcol = row[2]
        print(carno,cartype,carcol)
except:
    print("Error:unable to fetch data")

db.close()