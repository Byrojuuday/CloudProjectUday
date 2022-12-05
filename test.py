# import pandas as pd
# df = pd.read_csv("D:\\Mohan_Work\\Graduation\CloudComputing\\KrogerData\\400_households.csv")
# df.columns = df.columns.str.replace(' ', '')
# print(df.columns)
# df=df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
# for eachtuple in df.itertuples():
#      print(int(eachtuple.HSHD_NUM),str(eachtuple.L),str(eachtuple.AGE_RANGE),str(eachtuple.MARITAL),str(eachtuple.INCOME_RANGE),str(eachtuple.HOMEOWNER),str(eachtuple.HSHD_COMPOSITION),str(eachtuple.HH_SIZE),str(eachtuple.CHILDREN))
import json
import sqlite3
import pyodbc
import mysql.connector
import pandas as pd
import shutil
import os
from mysql.connector import errorcode
from flask import Flask, request, g, render_template, send_file
from werkzeug.utils import secure_filename
from main import app


def connecttoDataBase():

    config = {
    'host':'cloudprojectuday.mysql.database.azure.com',
    'user':'uday',
    'password':'uday',
    'database':'cloudprojectuday',
    'ssl-mode':'require'
    }
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    return conn;

def executeselectquery(queryString):
    conn = connecttoDataBase()
    # rows=pd.read_sql(queryString,conn)
    # print(rows)
    cursor = conn.cursor()
    cursor.execute(queryString);
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return pd.DataFrame(rows);

@app.route("/")
def displaydashboard():
     title = "Monthly Max and Min Temperature"
     data = executeselectquery("Select SUM(b.SPEND) as spent,a.HH_SIZE as hh from households as a inner join transactions as b on a.HSHD_NUM=b.HSHD_NUM group by a.HH_SIZE;")
     d=data.values.tolist()
     tempdata=json.dumps({'title':title,'data':d})
     render_template("Dashboard.html",tempdata=tempdata);


