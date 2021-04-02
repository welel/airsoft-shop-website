"""Creation of ``Customer`` and ``Cart`` fot superuser.

After creation of a superuser with manage.py you must to a cart
in database to use admin CRUD.

    (!) IMPORTANT: Module haven't end yet. Create cart for superuser manually.

"""
import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            dbname=os.getenv('DATABASE_NAME'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            host=os.getenv('DATABASE_HOST'),
            port=os.getenv('DATABASE_PORT')
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    return conn


def get_user_id(cursor, superusername):
    """Gets user's id by superusername."""
    SQL = """SELECT id FROM auth_user WHERE username=%d"""

def insert_customer(cursor):
    """Inserts a customer for superuser in the database."""
    SQL = """INSERT INTO user_customer(user_id) VALUES(%d);"""


if __name__ == '__main__':
    conn = connect()
    cur = conn.cursor()

    username = input('\nInput superuser name: ')
