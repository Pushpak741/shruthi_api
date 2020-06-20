from flask import jsonify
import pymysql

def query(querystr,return_json=True):
    connection=pymysql.connect(host='skillup-team-11.cxgok3weok8n.ap-south-1.rds.amazonaws.com',
                               user='admin',
                               password='coscskillup',
                               db='restapi',
                               cursorclass=pymysql.cursors.DictCursor)


    connection.begin()
    cursor=connection.cursor()
    cursor.execute(querystr)
    result=cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    if return_json:
            return jsonify(result)
    else:
        return result
