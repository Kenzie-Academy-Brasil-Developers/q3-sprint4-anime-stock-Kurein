import psycopg2
import os

DB_HOST= os.getenv("DB_HOST")
DB_NAME= os.getenv("DB_NAME")
DB_USER= os.getenv("DB_USER")
DB_PASSWORD= os.getenv("DB_PASSWORD")

class Anime():

    def __init__(self):
        self.fieldnames= ["id", "anime", "released_date", "seasons"]


    def open_connection(self):
        self.conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        self.cur = self.conn.cursor()
        return self.cur

    def commit_and_close(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def table_init(self):
        cur = self.open_connection()

        cur.execute("""
        create table if not exists animes(
	        id BIGSERIAL primary key,
	        anime VARCHAR(100) not null unique,
	        released_date date not null,
	        seasons integer not null
        );
        """)
        
        self.commit_and_close()