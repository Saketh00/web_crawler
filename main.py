import psycopg2
from flask import Flask, request

app=Flask("Job site")

dbconnect=psycopg2.connect("dbname=naukri")

@app.route("/")
def initial():
    cursor=dbconnect.cursor()
    cursor.execute("select count(*) from openings")
    njobs=cursor.fetchall()[0][0]

    return f"""
    <html>
    <head>
    <title> Jobs Page</title>
    </head>

    <body>
    <h1>Welcome to jobs page</h1>
    There are currently <a href="/jobs">{njobs}</a> available.
    </body>
    </html>
    """


@app.route("/jobs") #decorator
def hello():
    cursor=dbconnect.cursor()
    cursor.execute("select title,company_name,jd_text from openings")
    ret=[]
    for title, company_name, jd in cursor.fetchall():
        item=f"<b>{title}</b> :::: {company_name} <br/> {jd}"
        ret.append(item)
    l="<hr/>".join(ret)
    return f"<h1>List of jobs is:</h1><br/> {l}"

if __name__=="__main__":
    app.run()
