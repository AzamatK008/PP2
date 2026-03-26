import csv
from connect import get_connection, create_table


# 2. Insert data from CSV
def insert_from_csv(filename):
    conn = get_connection()
    cur = conn.cursor()

    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                cur.execute(
                    "INSERT INTO contacts (username, phone) VALUES (%s, %s)",
                    (row["username"], row["phone"])
                )
            except Exception:
                conn.rollback()
            else:
                conn.commit()

    cur.close()
    conn.close()


# 3. Insert data from console
def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone number: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (username, phone) VALUES (%s, %s)",
        (username, phone)
    )

    conn.commit()
    cur.close()
    conn.close()


# 4. Update contact
def update_contact(old_value, new_value, field="username"):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        f"UPDATE contacts SET {field} = %s WHERE {field} = %s",
        (new_value, old_value)
    )

    conn.commit()
    cur.close()
    conn.close()


# 5. Query contacts with filters
def query_contacts(filter_value=None):
    conn = get_connection()
    cur = conn.cursor()

    if filter_value:
        cur.execute(
            "SELECT * FROM contacts WHERE username ILIKE %s OR phone LIKE %s",
            (f"%{filter_value}%", f"{filter_value}%")
        )
    else:
        cur.execute("SELECT * FROM contacts")

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()


# 6. Delete contact
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


def menu():
    print("""
1. Insert from CSV
2. Insert from console
3. Update contact
4. Query contacts
5. Delete contact
0. Exit
""")


if __name__ == "__main__":
    create_table()

    while True:
        menu()
        choice = input("Choose option: ")

        if choice == "1":
            insert_from_csv("contacts.csv")
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            field = input("Update username or phone? ")
            old = input("Old value: ")
            new = input("New value: ")
            update_contact(old, new, field)
        elif choice == "4":
            value = input("Filter (press Enter for all): ")
            query_contacts(value if value else None)
        elif choice == "5":
            value = input("Username or phone to delete: ")
            delete_contact(value)
        elif choice == "0":
            break
        else:
            print("Invalid option")