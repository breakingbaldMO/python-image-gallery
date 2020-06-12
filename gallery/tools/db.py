import psycopg2
from secrets import get_secret_image_gallery

db_host = "database-1.cv1n9oljqdta.us-east-1.rds.amazonaws.com"
db_name = "image_gallery"
db_user = "image_gallery"

password_file = "/home/ec2-user/.image_gallery_config"

connection = None

def get_secret():


def get_password():
    f = open(password_file, "r")
    result = f.readline()
    f.close()
    return result[:-1]


def connect():
    global connection
    connection = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=get_password())
    connection.set_session(autocommit=True)


def execute(query, args=None):
    global connection
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor


def add_user(username, password, full_name):
    cursor = connection.cursor()
    try:
        execute("""
        INSERT into users (username, password, full_name) VALUES (%s, %s, %s);
        """, (username, password, full_name))


    except Exception as error:
        print("Error: a user with username '" + username + "' already exists\n")


def edit_user(user_to_edit, password, full_name):
    try:
        if password:
                execute("UPDATE users SET password='" + password + "' WHERE username='" + user_to_edit + "';")


    except Exception as error:
                print("Error updating password\n")
    try:
        if full_name:
                execute("UPDATE users SET full_name='" + full_name + "' WHERE username='" + user_to_edit + "';")


    except Exception as error:
                print("Error updating full name\n")


def delete_user(user_to_delete):
    try:
        execute("DELETE FROM users WHERE username='" + user_to_delete + "';")

    except Exception as error:
            print("Error deleting username\n")


def select_all(table):
    res = execute('select * from ' + table).fetchall()
    return res