import os
import psycopg2
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_data = "user={} password={} host={} dbname={}".format(
    db_user, db_pass, db_host, db_name)

try:

    def connect_db(db_info):
        conn = psycopg2.connect(db_info)
        cur = conn.cursor()
        return conn, cur

    conn, cur = connect_db(db_data)

    def create_users_table(cur):
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
        id serial PRIMARY KEY,
        firstname VARCHAR(30) NOT NULL,
        lastname VARCHAR(30) NOT NULL,
        othername VARCHAR(30),
        username VARCHAR(40) NOT NULL,
        email VARCHAR(60) NOT NULL,
        phone VARCHAR(15) NOT NULL,
        password VARCHAR(60) NOT NULL,
        publicId VARCHAR(20) NOT NULL,
        isAdmin BOOLEAN DEFAULT False,
        register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )""")

    def create_meetups_table(cur):
        cur.execute(
            """
          CREATE TABLE IF NOT EXISTS meetups (
          id serial PRIMARY KEY,
          user_id INTEGER NOT NULL,
          topic VARCHAR(100) NOT NULL,
          location VARCHAR(200) NOT NULL,
          happen_on VARCHAR(20) NOT NULL,
          image bytea,
          tags VARCHAR(200) NOT NULL,
          created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          );""")

    def create_questions_table(cur):
        cur.execute(
            """
          CREATE TABLE IF NOT EXISTS questions (
          id serial PRIMARY KEY,
          user_id INTEGER NOT NULL,
          meetup_id INTEGER NOT NULL,
          topic VARCHAR(100) NOT NULL,
          location VARCHAR(200) NOT NULL,
          happen_on VARCHAR(20) NOT NULL,
          image bytea,
          tags VARCHAR(200) NOT NULL,
          created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          );""")

    def create_comment_table(cur):
        cur.execute(
            """
          CREATE TABLE IF NOT EXISTS comments (
          id serial PRIMARY KEY,
          user_id INTEGER NOT NULL,
          question_id INTEGER NOT NULL,
          value VARCHAR(20) NOT NULL,
          comment_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          );""")

    def create_rsvp_table(cur):
        cur.execute(
            """
          CREATE TABLE IF NOT EXISTS rsvp (
          id serial PRIMARY KEY,
          user_id INTEGER NOT NULL,
          meetup_id INTEGER NOT NULL,
          value VARCHAR(20) NOT NULL,
          responded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          );""")

    def create_votes_table(cur):
        cur.execute(
            """
          CREATE TABLE IF NOT EXISTS votes (
          id serial PRIMARY KEY,
          user_id INTEGER NOT NULL,
          question_id INTEGER NOT NULL,
          voted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          );""")

    def drop_table_if_exists(cur):
        """ Removes all tables on app start so as to start working with no data """
        drop_users = """ DROP TABLE IF EXISTS users """
        drop_meetups = """ DROP TABLE IF EXISTS meetups """
        drop_questions = """ DROP TABLE IF EXISTS questions """
        drop_comments = """ DROP TABLE IF EXISTS comments """
        drop_rsvp = """ DROP TABLE IF EXISTS rsvp """
        drop_votes = """ DROP TABLE IF EXISTS votes """

        for d_table in [drop_votes, drop_rsvp, drop_comments, drop_meetups, drop_questions, drop_users]:
            cur.execute(d_table)
            save()

    def perform_query(query):
        cur.execute(query)

    def save():
        conn.commit()

    def close_connection():
        cur.close()
        conn.close()
        print("database action complete")

    def main():
        drop_table_if_exists(cur)
        create_users_table(cur)
        create_meetups_table(cur)
        create_rsvp_table(cur)
        create_questions_table(cur)
        create_comment_table(cur)
        create_votes_table(cur)
        save()
        close_connection()

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
