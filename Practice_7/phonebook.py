import csv
from connect import get_connection, create_table


def insert_from_csv(filename):
    conn = get_connection()
    cur = conn.cursor()

    with open(filename, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                cur.execute(
                    "INSERT INTO contacts (username, phone) VALUES (%s, %s)",
                    (row["username"], row["phone"])
                )
                conn.commit()
            except Exception as e:
                conn.rollback()
                print("Error:", e)

    cur.close()
    conn.close()


def insert_from_console():
    username = input("Username: ")
    phone = input("Phone: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO contacts (username, phone) VALUES (%s, %s)",
        (username, phone)
    )
    conn.commit()
    cur.close()
    conn.close()


def update_contact(old_value, new_value, field):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE contacts SET {field} = %s WHERE {field} = %s",
        (new_value, old_value)
    )
    conn.commit()
    cur.close()
    conn.close()


def query_contacts(value=None):
    conn = get_connection()
    cur = conn.cursor()

    if value:
        cur.execute(
            "SELECT * FROM contacts WHERE username ILIKE %s OR phone LIKE %s",
            (f"%{value}%", f"{value}%")
        )
    else:
        cur.execute("SELECT * FROM contacts")

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def delete_contact(value):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM contacts WHERE username = %s OR phone = %s",
        (value, value)
    )
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    print("PROGRAM STARTED")

    create_table()

    while True:
        print("""
1. Insert from CSV
2. Insert from console
3. Update contact
4. Query contacts
5. Delete contact
0. Exit
""")

        choice = input("Choose option: ")

        if choice == "1":
            insert_from_csv("contacts.csv")
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            field = input("username or phone: ")
            old = input("Old value: ")
            new = input("New value: ")
            update_contact(old, new, field)
        elif choice == "4":
            value = input("Filter (Enter = all): ")
            query_contacts(value if value else None)
        elif choice == "5":
            value = input("Username or phone: ")
            delete_contact(value)
        elif choice == "0":
            break
        else:
            print("Invalid option")
            