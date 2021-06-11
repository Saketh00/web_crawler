import requests
import bs4
import psycopg2

import sys

def fetch_jobs():
    url = "https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&keyword=python&location=bangalore&k=python&l=bangalore&seoKey=python-jobs-in-bangalore&src=jobsearchDesk&latLong="

    headers={"appid" : "109",
            "systemid" : "109"}

    r=requests.get(url,headers=headers)

    data=r.json()
    return data['jobDetails']

def insert_jobs(jobs):
    dbconnect=psycopg2.connect("dbname=naukri")
    cursor=dbconnect.cursor()
    for i in jobs:
        soup=bs4.BeautifulSoup(i['jobDescription'],features="html.parser")
        cursor.execute("INSERT INTO openings (title, job_id, company_name, jd_url, jd_text) values (%s,%s,%s,%s,%s)",(i['title'],i['jobId'],i['companyName'],i['jdURL'],soup.text))
    
    dbconnect.commit()

def create_db():
    dbconnect=psycopg2.connect("dbname=naukri")
    cursor=dbconnect.cursor()
    f=open("jobs.sql")
    sql_code=f.read()
    f.close()
    cursor.execute(sql_code)
    dbconnect.commit()

def main(arg):
    if arg=="create":
        #print("create")
        create_db()
    elif arg=="crawl":
        #print("crawl")
        jobs=fetch_jobs()
        insert_jobs(jobs)
    else:   
        print(f"unknowm command {arg}")

if __name__=="__main__":
    main(sys.argv[1]) 