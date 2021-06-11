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
        item=f"<b>{title}</b> :::: {company_name} <br/> {jd}"
        ret.append(item)
    l="<hr/>".join(ret)
    return f"<b>List of jobs is:</b><br/> {l}"

if __name__=="__main__":
    app.run()
