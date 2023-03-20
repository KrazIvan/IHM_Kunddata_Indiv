from kunddata_imports import få_hubspot_kunder, få_newsletters_kunder
import mariadb


def import_hubspot_data(hubspot_data):
    conn = mariadb.connect(
        user="root",
        password="i",
        host="localhost",
        database="ihm_imported_indiv"
    )
    cur = conn.cursor()

    for data in hubspot_data:
        id = data['id']
        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']
        
        cur.execute("INSERT INTO customers (id, email, first_name, last_name) VALUES (?, ?, ?, ?)",
                    (id, email, first_name, last_name))

    conn.commit()
    conn.close()

def import_newsletters_data(newsletters_data):
    conn = mariadb.connect(
        user="root",
        password="i",
        host="localhost",
        database="ihm_imported_indiv"
    )
    cur = conn.cursor()

    for data in newsletters_data:
        id = data["id"]
        email = data["email"]
        first_name = data["first_name"]
        last_name = data["last_name"]
        
        cur.execute("INSERT INTO customers (id, email, first_name, last_name) VALUES (?, ?, ?, ?)",
                    (id, email, first_name, last_name))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    newsletter_kunddata = få_newsletters_kunder()
    import_newsletters_data(newsletter_kunddata)
    #hubspot_kunddata = få_hubspot_kunder()
    #import_hubspot_data(hubspot_kunddata) <----- Fortfarande konstig och ska fixas, förlåt! :(

