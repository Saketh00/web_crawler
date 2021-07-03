import psycopg2

from flask import current_app,g

def get_db():
    if 'db' not in g:
        DataBaseName=current_app.config['DATABASE']
        g.db=psycopg2.connect(f"dbname={DataBaseName}")
    return g.db