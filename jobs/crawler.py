import requests
import bs4

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
    for i in jobs:
        soup=bs4.BeautifulSoup(i['jobDescription'],features="html.parser")
        cursor.execute("INSERT INTO openings (title, job_id, company_name, jd_url, jd_text) values (%s,%s,%s,%s,%s)",(i['title'],i['jobId'],i['companyName'],i['jdURL'],soup.text))

    click.echo(f"Added {len(jobs)} jobs.")
    
    dbconnect.commit()

@click.command('crawl', help="Crawl for jobs")
@with_appcontext
def crawl_command():
    jobs=fetch_jobs()
    insert_jobs(jobs)

def init_app(app):
    app.cli.add_command(crawl_command)