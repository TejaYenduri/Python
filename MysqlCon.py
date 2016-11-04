import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='Employee')

cur = conn.cursor()

cur.execute("SELECT * from Employee")

for row in cur:
    print(row)

cur.close()
conn.close()