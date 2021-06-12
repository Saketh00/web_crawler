import psycopg2
from flask import Flask, request
from flask import render_template

app=Flask("Job site")

dbconnect=psycopg2.connect("dbname=naukri")

@app.route("/")
def initial():
    cursor=dbconnect.cursor()
    cursor.execute("select count(*) from openings")
    count_of_jobs=cursor.fetchall()[0][0]

    return render_template("main.html",njobs=count_of_jobs)


@app.route("/jobs") #decorator
def jobs():
    cursor=dbconnect.cursor()
    cursor.execute("select title,company_name,jd_text from openings")
    jobs_list=cursor.fetchall()
    
    return render_template("jobslist.html",jobs=jobs_list)

if __name__=="__main__":
    app.run()
