import psycopg2
from configs import config_db


from dotenv import load_dotenv
from datetime import datetime, timedelta


class DB(object):

    def __init__(self) -> None:
        
        self.user = config_db.user
        self.password = config_db.password
        self.database = config_db.database
        self.host= config_db.host
        self.port = config_db.port
        self.conn = None


    def __enter__(self):
        self.conn = psycopg2.connect(user=self.user ,dbname=self.database, password=self.password, host=self.host, port=self.port)
        self.cur = self.conn.cursor()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    
    def create_tables(self):

        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                         id serial,
                         user_id bigint,
                         username TEXT,
                         date_register DATE

        );""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS technical_work(
                         work_tz TEXT                     
        );""")

        # self.conn.commit()

    def save_user(self, user_id):
        user = self.cur.execute("SELECT * FROM users WHERE user_id= %s;", (user_id, ))
        user = self.cur.fetchone()
        if not user:
            self.cur.execute("INSERT INTO users (user_id) VALUES (%s);", (user_id, ))

    def username_start(self, username_value, user_id):
        username = self.cur.execute("SELECT * FROM users WHERE  username= %s", (username_value,))
        username = self.cur.fetchone()
        if not username :
            self.cur.execute("UPDATE users SET username=%s WHERE user_id=%s", (username_value, user_id))

    
    def get_random_tz(self):
        self.cur.execute("SELECT work_tz FROM technical_work ORDER BY RANDOM() LIMIT 1")
        random_object = self.cur.fetchone()
        return random_object[0]
    
    def save_date(self, user, date):
        self.cur.execute("SELECT date_register FROM users WHERE user_id=%s", (user, ))
        existing_date = self.cur.fetchone()[0]
   
        if not existing_date:
            self.cur.execute("UPDATE users SET date_register=%s WHERE user_id=%s", (date, user))
  
    

    def get_all_users(self, count=0, rassil=0):
        if rassil > 0 :
            self.cur.execute('SELECT * FROM users')
            return self.cur.fetchall()
        elif count > 0 :
            self.cur.execute('SELECT count(*) FROM users')
            return self.cur.fetchone()[0]
    
    def get_count_users_last_day(self):
        today = datetime.now().date()
        yesterday = today - timedelta(days=0)
        self.cur.execute("SELECT COUNT(*) FROM users WHERE date_register = %s", (yesterday,))
        return self.cur.fetchone()[0]

    def get_count_users_last_week(self):
        today = datetime.now().date()
        last_week = today - timedelta(days=7)
        self.cur.execute("SELECT COUNT(*) FROM users WHERE date_register >= %s", (last_week,))
        return self.cur.fetchone()[0]
    
    def get_count_users_last_month(self):
        today = datetime.now().date()
        last_month = today.replace(day=1) - timedelta(days=1)
        self.cur.execute("SELECT COUNT(*) FROM users WHERE date_register >= %s", (last_month,))
        return self.cur.fetchone()[0]
    
    def add_tz(self, tz):
        self.cur.execute("INSERT INTO technical_work (work_tz) VALUES (%s)", (tz,))
        
    

with DB() as db:
    db.create_tables()