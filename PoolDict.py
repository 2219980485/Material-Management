import pymysql as mysql
def ConnectionPool():
    #db=mysql.connect(host='localhost',port=3306,user="root",password="123",db="mm")
    db = mysql.connect(host='campusshala.com', port=3306, user="campussh_mm", password="sandeep123@", db="campussh_mm")
    cmd=db.cursor(mysql.cursors.DictCursor)
    return (db,cmd)
