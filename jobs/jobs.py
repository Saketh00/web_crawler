from flask import Blueprint, g, render_template
from . import db

bp=Blueprint("jobs","jobs", url_prefix="/jobs")

@bp.route("/")
def all_jobs():
    conn=db.get_db()
    cursor=conn.cursor()
    cursor.execute("select o.id, o.title, o.company_name, s.name from openings o, job_status s where o.status=s.id order by s.name")
    jobs_list=cursor.fetchall()

    cursor.execute("select crawled_on from crawl_status order by crawled_on desc limit 1")
    crawl_date=cursor.fetchone()[0]
    return render_template("jobs/jobslist.html",jobs=jobs_list, count=len(jobs_list), date=crawl_date)

@bp.route("/<jid>")
def jobdetails(jid):
    conn=db.get_db()
    cursor=conn.cursor()
    cursor.execute("select o.title, o.company_name, s.name, o.jd_text, o.crawled_on from openings o, job_status s where o.id= %s and s.id=o.status",(jid,))
    job=cursor.fetchone()
    if not job:
        return render_template("jobs/jobdetails.html"),404
    
    title, company, status, info, crawled_on=job
    jid=int(jid)
    if jid==1:
        prev=None
    else:
        prev=jid-1
    nxt=jid+1

    classes={"crawled" : "primary",
            "applied" : "secondary",
            "ignored" : "dark",
            "selected" : "success",
            "rejected" : "danger"}
    return render_template("jobs/jobdetails.html", jid=jid, info=info, title=title, company=company, prev=prev, nxt=nxt, status=status, cls=classes[status], crawled_on=crawled_on)
