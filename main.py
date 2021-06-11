import psycopg2
from flask import Flask, request



app=Flask("Job site")

@app.route("/") #decorator
def hello():
    dbconnect=psycopg2.connect("dbname=naukri")
    cursor=dbconnect.cursor()
    cursor.execute("select title,company_name,jd_text from openings")
    ret=[]
    for title, company_name, jd in cursor.fetchall():
        item=f"{title} :::: {company_name} :::: {jd}"
        ret.append(item)
    l=",".join(ret)
    return f"List of jobs is : {l}"
