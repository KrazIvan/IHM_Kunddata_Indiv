from kunddata_imports import få_hubspot_companies, få_hubspot_deals, få_hubspot_kunder, få_newsletters_kunder, få_payments, få_credits_kunder
import mariadb
import sys


def import_hubspot_kunder(hubspot_contacts):
    try:
        conn = mariadb.connect(
        user="root",
        password="i",
        host="localhost",
        database="hubspot_contacts")
    except mariadb.Error as fel:
        print(f"Error connecting to MariaDB: {fel}")
        sys.exit(1)

    cur = conn.cursor()

    cur.execute("CREATE DATABASE IF NOT EXISTS hubspot_contacts")
    cur.execute("USE hubspot_contacts")
    cur.execute("CREATE TABLE IF NOT EXISTS customers (id INT PRIMARY KEY, email VARCHAR(255), firstname VARCHAR(255), lastname VARCHAR(255))")

    for kund in hubspot_contacts:
        id = int(kund["id"])
        email = kund["properties"]["email"]
        firstname = kund["properties"]["firstname"]
        lastname = kund["properties"]["lastname"]

        cur.execute("INSERT INTO customers (id, email, firstname, lastname) VALUES (?, ?, ?, ?)", (id, email, firstname, lastname))

    conn.commit()
    conn.close()


def import_newsletters_data(newsletters_data):
    try:
        conn = mariadb.connect(
        user="root",
        password="i",
        host="localhost",
        database="newsletters_data")

        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                Id VARCHAR(36) PRIMARY KEY,
                Email VARCHAR(255),
                FirstName VARCHAR(255),
                LastName VARCHAR(255),
                Country VARCHAR(255),
                Zip VARCHAR(10),
                Street VARCHAR(255)
            )
        """)
        
        for kund in newsletters_data:
            cur.execute("""
                INSERT INTO customers (Id, Email, FirstName, LastName, Country, Zip, Street)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                kund["Id"],
                kund["Email"],
                kund["FirstName"],
                kund["LastName"],
                kund["Country"],
                kund["Zip"],
                kund["Street"]
            ))
        
        conn.commit()
        
    except mariadb.Error as fel:
        print(f"Ett fel uppstog: {fel}")
        sys.exit(1)
        
    finally:
        if conn:
            conn.close()

def import_payments(payments_data):
    try:
        conn = mariadb.connect(
            user="root",
            password="i",
            host="localhost",
            database="payments_data")

        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_number VARCHAR(255),
                amount INT,
                currency VARCHAR(255),
                method VARCHAR(255),
                status VARCHAR(255)
            )
        """)

        for payment in payments_data:
            cur.execute("""
                INSERT INTO payments (order_number, amount, currency, method, status)
                VALUES (?, ?, ?, ?, ?)
            """, (payment["orderNumber"], payment["amount"], payment["currency"], payment["method"], payment["status"]))

        conn.commit()
        cur.close()
        conn.close()

    except mariadb.Error as fel:
        print(f"Ett fel uppstog: {fel}")
        sys.exit(1)


if __name__ == "__main__":
    import_newsletters_data(få_newsletters_kunder())
    import_hubspot_kunder(få_hubspot_kunder())
    import_payments((få_payments(order_numbers=["330495", "330496", "123456", "330497", "330498", "999999"])))

