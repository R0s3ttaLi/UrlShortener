import pymysql
import click
from flask import current_app, g
from flask.cli import with_appcontext

# Set the database credentials
host = "test-database.cpmd3cwyvujs.ap-southeast-2.rds.amazonaws.com"
port = 3306
user = "Admin"
password = "test2023"
database = "users_db"

def get_db():
    if 'db' not in g:
        
        g.db = pymysql.connect(
            host=host, port=port, user=user, password=password, database=database
        )
        
    return g.db


def close_db(e = None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db() 
    f = open("/home/ec2-user/url_shortener/backend/schema.sql", "r")
    with db.cursor() as cursor:
        for command in f.readlines():
            cursor.execute(command)
    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
