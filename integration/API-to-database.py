from kunddata_imports import få_hubspot_deals, få_hubspot_companies, få_hubspot_kunder, få_newsletters_kunder, få_payments, få_credits_kunder
import mariadb
from datetime import datetime
import sys

# Hubspot -----------------------------------------------------------

def import_hubspot_deals(hubspot_deals):
    try:
        conn = mariadb.connect(
        user="root",
        password="i",
        host="localhost",
        database="hubspot_deals")
    except mariadb.Error as fel:
        print(f"Error connecting to MariaDB: {fel}")
        sys.exit(1)

    cur = conn.cursor()

    cur.execute("CREATE DATABASE IF NOT EXISTS hubspot_deals")
    cur.execute("USE hubspot_deals")
    cur.execute("""CREATE TABLE IF NOT EXISTS deals (id BIGINT PRIMARY KEY, 
    dealname VARCHAR(255), 
    amount INT,
    createdate VARCHAR(255),
    closedate VARCHAR(255),
    dealstage VARCHAR(255), 
    pipeline VARCHAR(255))""")

    for deal in hubspot_deals:
        id = int(deal["id"])
        amount = int(deal["properties"]["amount"])
        createdate = deal["properties"]["createdate"]
        closedate = deal["properties"]["closedate"]
        dealname = deal["properties"]["dealname"]
        dealstage = deal["properties"]["dealstage"]
        pipeline = deal["properties"]["pipeline"]

        cur.execute("INSERT INTO deals (id, dealname, amount, createdate, closedate, dealstage, pipeline) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                    (id, dealname, amount, createdate, closedate, dealstage, pipeline))

    conn.commit()
    conn.close()

def import_hubspot_companies(hubspot_companies):
    try:
        conn = mariadb.connect(
        user="root",
        password="i",
        host="localhost",
        database="hubspot_companies")
    except mariadb.Error as fel:
        print(f"Error connecting to MariaDB: {fel}")
        sys.exit(1)

    cur = conn.cursor()

    cur.execute("CREATE DATABASE IF NOT EXISTS hubspot_companies")
    cur.execute("USE hubspot_companies")
    cur.execute("CREATE TABLE IF NOT EXISTS companies (id BIGINT PRIMARY KEY, name VARCHAR(255), domain VARCHAR(255))")

    for company in hubspot_companies:
        id = int(company["id"])
        domain = company["properties"]["domain"]
        name = company["properties"]["name"]
    
        cur.execute("INSERT INTO companies (id, name, domain) VALUES (?, ?, ?)", (id, name, domain))

    conn.commit()
    conn.close()

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
    cur.execute("CREATE TABLE IF NOT EXISTS customers (id INT PRIMARY KEY, firstname VARCHAR(255), lastname VARCHAR(255), email VARCHAR(255))")

    for kund in hubspot_contacts:
        id = int(kund["id"])
        email = kund["properties"]["email"]
        firstname = kund["properties"]["firstname"]
        lastname = kund["properties"]["lastname"]

        cur.execute("INSERT INTO customers (id, email, firstname, lastname) VALUES (?, ?, ?, ?)", (id, firstname, lastname, email))

    conn.commit()
    conn.close()


# Newsletters ---------------------------------------------------------

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
                INSERT INTO customers (Id, FirstName, LastName, Email, Country, Zip, Street)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                kund["Id"],
                kund["FirstName"],
                kund["LastName"],
                kund["Email"],
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


# Zeep ----------------------------------------------

def import_credits(credits_data):
    try:
        conn = mariadb.connect(
            user="root",
            password="i",
            host="localhost",
            database="credits_data")

        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS credits (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_number VARCHAR(255),
                amount INT,
                currency VARCHAR(255)
            )
        """)

        for credit in credits_data:
            cur.execute("""
                INSERT INTO credits (customer_number, amount, currency)
                VALUES (?, ?, ?)
            """, (credit["customerNumber"], int(credit["amount"]), credit["currency"]))

        conn.commit()
        cur.close()
        conn.close()

    except mariadb.Error as fel:
        print(f"Ett fel uppstog: {fel}")
        sys.exit(1)

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
            """, (payment["orderNumber"], int(payment["amount"]), payment["currency"], payment["method"], payment["status"]))

        conn.commit()
        cur.close()
        conn.close()

    except mariadb.Error as fel:
        print(f"Ett fel uppstog: {fel}")
        sys.exit(1)


if __name__ == "__main__":
    import_hubspot_deals(få_hubspot_deals())
    import_hubspot_companies(få_hubspot_companies())
    import_hubspot_kunder(få_hubspot_kunder())
    import_newsletters_data(få_newsletters_kunder())
    import_credits(få_credits_kunder(customer_numbers=["10001", "10002", "10003", "10004", "330495", "10005", "330496", "10006", "123456", "10007","330497", "10008", "330498", "999999"]))
    import_payments((få_payments(order_numbers=["330495", "330496", "123456", "330497", "330498", "999999"])))