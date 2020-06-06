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


def menu():
    choice = input("1) List users\n2) Add user\n3) Edit user\n4) Delete user\n5) Quit\nEnter Command>")
    choice = int(choice)
    if choice == 1:
        print("You entered 1\n")
        res = execute('select * from users')
        print("username  password  full name\n-------------------------------")
        for row in res:
            print(row)
        print("\n")
        menu()

    elif choice == 2:
        print("You entered 2")
        menu()
    elif choice == 3:
        print("You entered 3")
        menu()
    elif choice == 4:
        print("You entered 4")
        menu()
    elif choice == 5:
        print("Goodbye")


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
