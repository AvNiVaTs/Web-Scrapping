import sqlite3

def connect(dbname):
    conn = sqlite3.connect(dbname)

    conn.execute("CREATE TABLE IF NOT EXISTS TRIVAGO_HOTELS (NAME TEXT, ADDRESS TEXT, PRICE INT, DISCOUNT TEXT, RATING TEXT)")

    print("Table created successfully!")

    conn.close()

def insert_into_table(dbname, values):
    conn = sqlite3.connect(dbname)
    print("Inserted into table: " + str(values))
    insert_sql = "INSERT INTO TRIVAGO_HOTELS (NAME, ADDRESS, PRICE, DISCOUNT, RATING) VALUES (?, ?, ?, ?, ?)"

    conn.execute(insert_sql, values)

    conn.commit()
    conn.close()

def get_hotel_info(dbname):
    conn = sqlite3.connect(dbname)

    cur = conn.cursor()

    cur.execute("SELECT * FROM TRIVAGO_HOTELS")

    table_data = cur.fetchall()

    for record in table_data:
        print(record)