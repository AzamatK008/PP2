import csv
import json
from connect import get_connection

def run_schema():
    conn = get_connection()
    cur = conn.cursor()

    with open("c:\\Users\\user\\Desktop\\PP2\\PP2\\TSIS1\\schema.sql", "r") as f:
        cur.execute(f.read())

    conn.commit()
    cur.close()
    conn.close()

    print("Schema created.")

def get_group_id(cur, group_name):
    cur.execute("""
        INSERT INTO groups(name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
    """, (group_name,))

    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    return cur.fetchone()[0]


def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday YYYY-MM-DD: ")
    group_name = input("Group: ")
    phone = input("Phone: ")
    phone_type = input("Phone type home/work/mobile: ")

    conn = get_connection()
    cur = conn.cursor()

    group_id = get_group_id(cur, group_name)

    cur.execute("""
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (name, email, birthday, group_id))

    contact_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO phones(contact_id, phone, type)
        VALUES (%s, %s, %s)
    """, (contact_id, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact added.")


def add_phone():
    name = input("Contact name: ")
    phone = input("New phone: ")
    phone_type = input("Type home/work/mobile: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()

    print("Phone added.")


def move_to_group():
    name = input("Contact name: ")
    group = input("New group: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s, %s)", (name, group))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact moved.")


def search_contacts():
    query = input("Search: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def filter_by_group():
    group = input("Group name: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name ILIKE %s
    """, (group,))

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def sort_contacts():
    print("Sort by: name / birthday / date_added")
    sort_by = input("Choice: ")

    allowed = ["name", "birthday", "date_added"]

    if sort_by not in allowed:
        print("Wrong sort field.")
        return

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.{sort_by}
    """)

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def paginated_navigation():
    limit = int(input("Limit per page: "))
    offset = 0

    conn = get_connection()
    cur = conn.cursor()

    while True:
        cur.execute("""
            SELECT c.id, c.name, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.id
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()

        print("\n--- Page ---")
        for row in rows:
            print(row)

        command = input("next / prev / quit: ")

        if command == "next":
            offset += limit
        elif command == "prev":
            offset = max(0, offset - limit)
        elif command == "quit":
            break
        else:
            print("Wrong command.")

    cur.close()
    conn.close()


def export_json():
    filename = input("JSON filename: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            c.id, c.name, c.email, c.birthday, c.date_added,
            g.name AS group_name,
            p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY c.id
    """)

    rows = cur.fetchall()
    contacts = {}

    for row in rows:
        contact_id, name, email, birthday, date_added, group_name, phone, phone_type = row

        if contact_id not in contacts:
            contacts[contact_id] = {
                "name": name,
                "email": email,
                "birthday": str(birthday) if birthday else None,
                "date_added": str(date_added),
                "group": group_name,
                "phones": []
            }

        if phone:
            contacts[contact_id]["phones"].append({
                "phone": phone,
                "type": phone_type
            })

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(list(contacts.values()), file, indent=4, ensure_ascii=False)

    cur.close()
    conn.close()

    print("Export finished.")


def import_json():
    filename = input("JSON filename: ")

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    conn = get_connection()
    cur = conn.cursor()

    for item in data:
        name = item["name"]

        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        existing = cur.fetchone()

        if existing:
            choice = input(f"{name} exists. skip/overwrite: ")

            if choice == "skip":
                continue

            if choice == "overwrite":
                contact_id = existing[0]
                group_id = get_group_id(cur, item.get("group", "Other"))

                cur.execute("""
                    UPDATE contacts
                    SET email = %s, birthday = %s, group_id = %s
                    WHERE id = %s
                """, (
                    item.get("email"),
                    item.get("birthday"),
                    group_id,
                    contact_id
                ))

                cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))

        else:
            group_id = get_group_id(cur, item.get("group", "Other"))

            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (
                item.get("name"),
                item.get("email"),
                item.get("birthday"),
                group_id
            ))

            contact_id = cur.fetchone()[0]

        for phone in item.get("phones", []):
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (
                contact_id,
                phone["phone"],
                phone["type"]
            ))

    conn.commit()
    cur.close()
    conn.close()

    print("Import finished.")


def import_csv():
    filename = input("CSV filename: ")

    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            group_id = get_group_id(cur, row["group"])

            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (
                row["name"],
                row["email"],
                row["birthday"],
                group_id
            ))

            contact_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (
                contact_id,
                row["phone"],
                row["phone_type"]
            ))

    conn.commit()
    cur.close()
    conn.close()

    print("CSV import finished.")


def menu():
    while True:
        print("""
1. Add contact
2. Add phone
3. Move to group
4. Search contacts
5. Filter by group
6. Sort contacts
7. Paginated navigation
8. Export JSON
9. Import JSON
10. Import CSV
0. Exit
""")

        choice = input("Choose: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            add_phone()
        elif choice == "3":
            move_to_group()
        elif choice == "4":
            search_contacts()
        elif choice == "5":
            filter_by_group()
        elif choice == "6":
            sort_contacts()
        elif choice == "7":
            paginated_navigation()
        elif choice == "8":
            export_json()
        elif choice == "9":
            import_json()
        elif choice == "10":
            import_csv()
        elif choice == "0":
            break
        else:
            print("Wrong choice.")


if __name__ == "__main__":
    run_schema()
    menu()