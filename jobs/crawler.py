import requests
import bs4

import datetime

import click
from flask.cli import with_appcontext

from . import db

import sys

def fetch_jobs():
    url = "https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&keyword=python&location=bangalore&k=python&l=bangalore&seoKey=python-jobs-in-bangalore&src=jobsearchDesk&latLong="

    headers={"appid" : "109",
            "systemid" : "109"}

    r=requests.get(url,headers=headers)

    data=r.json()
    return data['jobDetails']

def insert_jobs(jobs):
    dbconnect=db.get_db()
    cursor=dbconnect.cursor()

    cursor.execute("select id from job_status where name ='crawled'")
    crawled_id=cursor.fetchone()[0]

    crawled_on=datetime.date.today()
    for i in jobs:
        soup=bs4.BeautifulSoup(i['jobDescription'],features="html.parser")
        cursor.execute("INSERT INTO openings (title, job_id, company_name, jd_url, jd_text, status, crawled_on) values (%s,%s,%s,%s,%s,%s,%s)",(i['title'],i['jobId'],i['companyName'],i['jdURL'],str(soup.text),crawled_id,crawled_on))

    click.echo(f"Added {len(jobs)} jobs.")

    crawled_on=datetime.datetime.now()
    cursor.execute("insert into crawl_status (crawled_on) values (%s)",(crawled_on,))    
    dbconnect.commit()

@click.command('crawl', help="Crawl for jobs")
@with_appcontext
def crawl_command():
    jobs=fetch_jobs()
    insert_jobs(jobs)

def init_app(app):
    app.cli.add_command(crawl_command)