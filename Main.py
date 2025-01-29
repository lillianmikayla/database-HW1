import csv
import os.path
from Database import DB

def main():
    db = DB() #create an instance of the DB class

    #main menu
    while True: 
        print("\nMenu:")
        print("1) Create new database")
        print("2) Open database")
        print("3) Close database")
        print("4) Display record")
        print("5) Update record")
        print("6) Create report")
        print("7) Add record")
        print("8) Delete record")
        print("9) Quit")

        choice = input("Enter choice: ")

        if choice == "1":
            db.create_database()
        elif choice == "2":
            db.open_database()
        elif choice == "3":
            db.close_database()
        elif choice == "4":
            db.display_record()
        elif choice == "5":
            db.update_record()
        elif choice == "6":
            db.create_report()
        elif choice == "7":
            db.add_record()
        elif choice == "8":
            db.delete_record()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
    


