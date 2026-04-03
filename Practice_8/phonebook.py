import csv
from connect import get_connection

def insert_from_csv(filename):
    conn = get_connection()
    cur = conn.cursor()
    
    names = []
    phones = []
    
    try:
        with open(filename, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                names.append(row["first_name"].strip())
                phones.append(row["phone"].strip())
                
        # Тапсырма 3: Процедура арқылы жаппай қосу (Мәліметтерді массив түрінде береміз)
        cur.execute("CALL insert_bulk_contacts(%s, %s)", (names, phones))
        conn.commit()
        print("Bulk insert completed using procedure.")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"Error during bulk insert: {e}")
        conn.rollback()
        
    cur.close()
    conn.close()

def insert_from_console():
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n--- Енгізуді тоқтату үшін атына ештеңе жазбай Enter басыңыз ---")
    
    while True:
        name = input("Enter name: ").strip()
        if not name:  # Егер есім жазылмай бос қалса, цикл тоқтайды
            break
            
        phone = input("Enter phone: ").strip()
        
        try:
            # Тапсырма 2: Upsert процедурасын шақыру
            cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
            conn.commit()
            print(f"Contact '{name}' inserted or updated via procedure.")
        except Exception as e:
            print(f"Error during insert: {e}")
            conn.rollback()
            
    cur.close()
    conn.close()
    print("Console input completed.")

def query_by_pattern():
    pattern = input("Enter search pattern (name or phone part): ")
    conn = get_connection()
    cur = conn.cursor()
    
    # Тапсырма 1: Функцияны шақыру
    cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
    rows = cur.fetchall()
    
    if rows:
        print("\n--- Found Contacts ---")
        for row in rows:
            print(row)
    else:
        print("No matching contacts found.")
        
    cur.close()
    conn.close()

def query_with_pagination():
    try:
        limit = int(input("Enter limit (how many rows): "))
        offset = int(input("Enter offset (how many to skip): "))
    except ValueError:
        print("Please enter valid numbers.")
        return
        
    conn = get_connection()
    cur = conn.cursor()
    
    # Тапсырма 4: Пагинация функциясын шақыру
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    
    if rows:
        print("\n--- Paginated Results ---")
        for row in rows:
            print(row)
    else:
        print("No contacts found in this range.")
        
    cur.close()
    conn.close()

def delete_contact():
    value = input("Enter username or phone number to delete: ")
    conn = get_connection()
    cur = conn.cursor()
    
    # Тапсырма 5: Өшіру процедурасын шақыру
    cur.execute("CALL delete_contact_proc(%s)", (value,))
    conn.commit()
    
    cur.close()
    conn.close()
    print("Contact deleted (if it existed) via procedure.")

def menu():
    while True:
        print("\n--- PhoneBook Menu (Practice 8) ---")
        print("1. Insert data from CSV (Bulk)")
        print("2. Insert data from console (Upsert)")
        print("3. Query by pattern (name or phone)")
        print("4. Query with pagination")
        print("5. Delete by username or phone")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            insert_from_csv("contacts.csv")
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            query_by_pattern()
        elif choice == "4":
            query_with_pagination()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    menu()