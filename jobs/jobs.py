from flask import Blueprint, g, render_template
from . import db

bp=Blueprint("jobs","jobs", url_prefix="/")

@bp.route("/")
def all_jobs():
    conn=db.get_db()
    cursor=conn.cursor()
    cursor.execute("select id,title,company_name from openings")
    jobs_list=cursor.fetchall()
    return render_template("jobs/jobslist.html",jobs=jobs_list)

@bp.route("/<jid>")
def jobdetails(jid):
    conn=db.get_db()
    cursor=conn.cursor()
    cursor.execute(f"select title, company_name, jd_text from openings where id={jid}")
    title, company ,info=cursor.fetchone()
    jid=int(jid)
    if jid==1:
        prev=None
    else:
        prev=jid-1
    nxt=jid+1
    return render_template("jobs/jobdetails.html", title=title, company=company, info=info,prev=prev,nxt=nxt)
