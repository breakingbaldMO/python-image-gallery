import psycopg2

db_host = "database-1.cv1n9oljqdta.us-east-1.rds.amazonaws.com"
db_name = "image_gallery"
db_user = "image_gallery"

password_file = "/home/ec2-user/.image_gallery_config.txt"

connection = None


def get_password():
    f = open(password_file, "r")
    result = f.readline()
    f.close()
    return result[:-1]


def connect():
    global connection
    connection = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=get_password())


def execute(query, args=None):
    global connection
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor


def add_user():
    cursor = connection.cursor()
    username = input("Username>")
    password = input("Password>")
    full_name = input("Full name>")

    try:
        execute("""
        INSERT into users (username, password, full_name) VALUES (%s, %s, %s);
        """, (username, password, full_name))
        connection.commit()

    except Exception as error:
        print("Error: a user with username '" + username + "' already exists\n")


def edit_user():
    cursor = connection.cursor()
    user_to_edit = input("\nUsername to edit>")
    cursor.execute("select * from users where username='" + user_to_edit + "';")
    res = cursor.fetchall()
    if not res:
        print("\nNo such user exists\n")
    else:
        password = input("New password (press enter to keep current)>")
        full_name = input("New full name (press enter to keep current)>")

        try:
            if password:
                execute("UPDATE users SET password='" + password + "' WHERE username='" + user_to_edit + "';")
                connection.commit()

        except Exception as error:
                print("Error updating password\n")
        try:
            if full_name:
                execute("UPDATE users SET full_name='" + full_name + "' WHERE username='" + user_to_edit + "';")
                connection.commit()

        except Exception as error:
                print("Error updating full name\n")


def delete_user():
    user_to_delete = input("\nEnter username to delete>")
    answer = input("\nAre you sure that you want to delete " + user_to_delete + " ?")
    if answer is "Yes" or "Y":
        try:
            execute("DELETE FROM users WHERE username='" + user_to_delete + "';")
            connection.commit()
        except Exception as error:
            print("Error deleting username\n")


def select_all(table):
    res = execute('select * from ' + table).fetchall()
    return res


def menu():
    choice = input("1) List users\n2) Add user\n3) Edit user\n4) Delete user\n5) Quit\nEnter Command>")
    choice = int(choice)
    if choice == 1:
        print("\nList Users\n")
        res = select_all("users")
        print("username  password  full name\n-------------------------------")
        for row in res:
            formatted = str(row).strip('(),\'')
            formatted = formatted.replace("\'", "")
            formatted = formatted.replace(",", "    ")

            print(formatted)
        print("\n")
        menu()

    elif choice == 2:
        print("\nAdd User\n")
        add_user()
        menu()
    elif choice == 3:
        print("\nEdit User\n")
        edit_user()
        menu()
    elif choice == 4:
        print("\nDelete User\n")
        delete_user()
        menu()
    elif choice == 5:
        print("\nGoodbye!\n")


def main():
    connect()
    menu()

    # res = execute('select * from users')
    # for row in res:
    #    print(row)
    # res = execute("update users set password=%s where username='fred'", ('banana',))
    # res = execute('select * from users')
    # for row in res:
    #    print(row)


if __name__ == '__main__':
    main()
