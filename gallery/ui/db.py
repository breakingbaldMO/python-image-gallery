import psycopg2
import json
from . import secrets
from . import db

connection = None

def close():
    connection.close()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def connect():
    global connection
    connection = psycopg2.connect(host="database-3.cv1n9oljqdta.us-east-1.rds.amazonaws.com", dbname="postgres", user="postgres", password="password")
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
    username = username.strip()
    try:
        execute("""
        INSERT into users (username, password, full_name) VALUES (%s, %s, %s);
        """, (username, password, full_name))


    except Exception as error:
        print("Error: a user with username '" + username + "' already exists\n")


def edit_user(user_to_edit, password, full_name):
    try:
        if password != "-":
                execute("UPDATE users SET password='" + password + "' WHERE username='" + user_to_edit + "';")


    except Exception as error:
                print("Error updating password\n")
    try:
        if full_name != "-":
                execute("UPDATE users SET full_name='" + full_name + "' WHERE username='" + user_to_edit + "';")


    except Exception as error:
                print("Error updating full name\n")


def delete_user(user_to_delete):
    try:
        execute("DELETE FROM users WHERE username='" + user_to_delete + "\';")
        connection.commit()
    except Exception as error:
            print("Error deleting username\n")


def select_all(table):
    res = execute('select * from ' + table).fetchall()
    return res


def select_password(username):
    res = execute("select password from users where username='" + username + "\'").fetchone()
    user = []
    for row in res:
        user[0] = row
    return user


def select_user_info(username, table):
    res = execute("select * from " + table + " where username='" + username + "';").fetchall()
    return res


def select_user_info_string(username, table):
    cursor = execute("select * from " + table + " where username='" + username + "';").fetchall()
    row = cursor.fetchone()
    if row is None:
        return None
    else:
        res = [row[0], row[1], row[2]]
        return res


def select_all_usernames(table):
    res = execute('select username from ' + table).fetchall()
    return res


def main():
    connect()
    res = execute('select * from users')
    for row in res:
        print(row)

if __name__ == '__main__':
    main()
