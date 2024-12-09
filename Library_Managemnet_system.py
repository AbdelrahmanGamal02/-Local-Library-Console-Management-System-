
from datetime import datetime
from collections import Counter
import json
# Custom Exception for Duplicated IDs
class DuplicatedIDException(Exception):
    """A simple custom exception."""
    pass

Book_Catalog = {}
borrow_transaction = {}
return_transaction = {}

Members = {}

# For monthly report
Book_Catalog_For_monthly_report = {}
Book_Catalog_Updated_For_monthly_report = []
Book_Catalog_removed_For_monthly_report = []

borrow_transaction_For_monthly_report = {}
return_transaction_For_monthly_report = {}

Members_For_monthly_report = {}
Members_Updated_For_monthly_report = []
Members_removed_For_monthly_report = []


def add_book():
    try:
        book_number = int(input("Enter Book Number: "))
    except ValueError:
        print("only Integer numbers are allowed")
        book_number = int(input("Enter Integer number for Book Number: "))

    Book_Genre = input("Enter Book Genre: ")
    Book_ID = ((Book_Genre[0:2].upper()) + str(book_number))
    # Check for unique ID
    try:
        if Book_ID in Book_Catalog:
            raise DuplicatedIDException("Book ID Already Exists")
    except DuplicatedIDException as e:
        print(e)
        book_number = int(input("you can enter another integer number for book Number (Ensure that book number is valid): "))
        Book_ID = ((Book_Genre[0:2].upper()) + str(book_number))
        try:
            if Book_ID in Members:
                raise DuplicatedIDException("Book ID is also Exist, Information not added")
        except DuplicatedIDException as e:
            print(e)

    Book_Name = input("Enter Book Name: ")
    Book_Author = input("Enter Book Author: ")
    try:
        Book_Availability = int(input("Enter integer number for Book Availability: "))
    except ValueError:
        print("Invalid Input")
        Book_Availability = int(input("Enter integer number for Book Availability: "))

    Book_Catalog[Book_ID] = {
        "Book_Genre" : Book_Genre,
        "Book_Name" : Book_Name,
        "Book_Author" : Book_Author,
        "Book_Availability" : Book_Availability
    }

    Book_Catalog_For_monthly_report[Book_ID] =  Book_Catalog[Book_ID]

    print("Book Added Successfully")


def update_book(book_number, Book_Genre, Book_Name=None , Book_Author =None, Book_Availability=None):
    Book_ID = ((Book_Genre[0:2].upper()) + str(book_number))
    if Book_ID in Book_Catalog:
        if Book_Name:
            Book_Catalog[Book_ID]["Book_Name"] = Book_Name
            Book_Catalog_For_monthly_report[Book_ID]["Book_Name"] = Book_Name

            Book_Catalog_Updated_For_monthly_report.append(Book_Catalog[Book_ID]["Book_Name"])
            Book_Catalog_Updated_For_monthly_report.append("Book Name")
            print("Book Updated Successfully")
        if Book_Author:
            Book_Catalog[Book_ID]["Book_Author"] = Book_Author
            Book_Catalog_For_monthly_report[Book_ID]["Book_Author"] = Book_Author

            Book_Catalog_Updated_For_monthly_report.append(Book_Catalog[Book_ID]["Book_Name"])
            Book_Catalog_Updated_For_monthly_report.append("Book Author")
            print("Book Updated Successfully")

        if Book_Availability:
            try:
                if type(Book_Availability) is int:
                    Book_Catalog[Book_ID]["Book_Availability"] = Book_Availability
                    Book_Catalog_For_monthly_report[Book_ID]["Book_Availability"] = Book_Availability

                    Book_Catalog_Updated_For_monthly_report.append(Book_Catalog[Book_ID]["Book_Name"])
                    Book_Catalog_Updated_For_monthly_report.append("Book_Availability")
                    print("Book Updated Successfully")
                else:
                    raise ValueError("Book Availability is not an Integer Number")
            except ValueError as e:
                print(e)
    else:
        print("Invalid ID")


def remove_book(book_number , Book_Genre):
    Book_ID = ((Book_Genre[0:2].upper()) + str(book_number))
    if Book_ID in Book_Catalog:
        Book_Catalog_removed_For_monthly_report.append(Book_Catalog[Book_ID]["Book_Name"])
        Book_Catalog_removed_For_monthly_report.append(Book_Catalog[Book_ID]["Book_Genre"])
        Book_Catalog.pop(Book_ID)

        print("Book Removed Successfully")
    else:
        print("Book ID Not Found")


def borrow_book(Book_Number , Book_Genre , Member_number , member_name , return_date):
    Book_ID = ((Book_Genre[0:2].upper()) + str(Book_Number))
    Member_ID = ((member_name[0:2].upper()) + str(Member_number))
    if Book_ID in Book_Catalog and Member_ID in Members:
        try:
            if Book_Catalog[Book_ID]["Book_Availability"] != 0:
                Book_Catalog[Book_ID]["Book_Availability"] -= 1
                Members[Member_ID]["Borrowed_books"].append(Book_Catalog[Book_ID]["Book_Name"])
                borrow_transaction_ID = Book_ID + "_" + Member_ID
                # if the same member want to borrow the same book again
                borrow_transaction_counter = 0
                while borrow_transaction_ID in borrow_transaction:
                    borrow_transaction_counter += 1
                    borrow_transaction_ID = Book_ID + "_" + Member_ID + "_" + str(borrow_transaction_counter)

                current_date = datetime.today().date()
                days = (current_date - return_date).days
                while days > 0:
                    print("Invalid Return Date")
                    user_return_date = input("Enter a return date (YYYY-MM-DD): ")
                    return_date = datetime.strptime(user_return_date, "%Y-%m-%d").date()
                    days = (current_date - return_date).days

                borrow_transaction[borrow_transaction_ID] = {
                    "Member_ID" : Member_ID,
                    "Member_Name" : Members[Member_ID]["Member_Name"],
                    "Book_ID" : Book_ID,
                    "Book_Name" : Book_Catalog[Book_ID]["Book_Name"],
                    "return_date" : return_date.strftime('%Y-%m-%d'),
                    "borrow_date" : current_date.strftime('%Y-%m-%d'),
                    "Repeated_borrow_Transaction" : borrow_transaction_counter,
                }

                borrow_transaction_For_monthly_report[borrow_transaction_ID] = borrow_transaction[borrow_transaction_ID]

                if 100 <=  Members[Member_ID]["late_fees"]:
                    print(f"Warning , you have {Members[Member_ID]["late_fees"]} $ late fees")

                print("Book Borrowed Successfully :)")
            else:
                raise Exception("Book is already checked out")
        except Exception as e:
            print(e)

    elif Book_ID not in Book_Catalog:
        print("Book Not Found")
    elif Member_ID not in Members:
        print("Member Not Exist")


def return_book(Book_Number , Book_Genre , Member_number , member_name):
    Book_ID = ((Book_Genre[0:2].upper()) + str(Book_Number))
    Member_ID = ((member_name[0:2].upper()) + str(Member_number))
    transaction_ID = Book_ID + "_" + Member_ID
    if Book_ID in Book_Catalog and Member_ID in Members and transaction_ID in borrow_transaction and transaction_ID not in return_transaction:
        Book_Catalog[Book_ID]["Book_Availability"] += 1
        Members[Member_ID]["Borrowed_books"].remove(Book_Catalog[Book_ID]["Book_Name"])

        current_date = datetime.today().date()
        date_object = datetime.strptime(borrow_transaction[transaction_ID]['return_date'], '%Y-%m-%d').date()
        days = (current_date - date_object).days
        if days <= 0:
            late_fees = 0
        else:
            date_object = datetime.strptime(borrow_transaction[transaction_ID]['return_date'], '%Y-%m-%d').date()
            late_days = current_date - date_object
            late_fees = int(1 * late_days.days)
            Members[Member_ID]["late_fees"] += late_fees

        return_transaction[transaction_ID] = {
            "Member_ID" : Member_ID,
            "Member_Name" : Members[Member_ID]["Member_Name"],
            "Book_ID" : Book_ID,
            "Book_Name" : Book_Catalog[Book_ID]["Book_Name"],
            "Return_date" : current_date.strftime('%Y-%m-%d'),
            "late_fees" : late_fees
        }

        return_transaction_For_monthly_report[transaction_ID] = return_transaction[transaction_ID]
        print("Book Returned Successfully :)")

    elif Book_ID not in Book_Catalog:
        print("Book Not Found")
    elif Member_ID not in Members:
        print("Member Not Exist")
    elif transaction_ID in borrow_transaction and transaction_ID in return_transaction:
        # repeated borrow transaction
        for keys in borrow_transaction.keys():
            if transaction_ID == keys[:7] and keys not in return_transaction.keys():
                transaction_ID = keys

        Repeated_transaction_ID = Book_ID + "_" + Member_ID + "_" + str(borrow_transaction[transaction_ID]['Repeated_borrow_Transaction'])
        if Repeated_transaction_ID in borrow_transaction:
            Book_Catalog[Book_ID]["Book_Availability"] += 1
            Members[Member_ID]["Borrowed_books"].remove(Book_Catalog[Book_ID]["Book_Name"])

            current_date = datetime.today().date()
            date_object = datetime.strptime(borrow_transaction[transaction_ID]['return_date'], '%Y-%m-%d').date()
            days = (current_date - date_object).days
            if days <= 0:
                late_fees = 0
            else:
                late_days = current_date - borrow_transaction[transaction_ID]["return_date"]
                late_fees = int(1 * late_days.days)
                Members[Member_ID]["late_fees"] += late_fees

            return_transaction[Repeated_transaction_ID] = {
                "Member_ID" : Member_ID,
                "Member_Name" : Members[Member_ID]["Member_Name"],
                "Book_ID" : Book_ID,
                "Book_Name" : Book_Catalog[Book_ID]["Book_Name"],
                "Return_date" : current_date.strftime('%Y-%m-%d'),
                "late_fees" : late_fees
            }

            return_transaction_For_monthly_report[Repeated_transaction_ID] = return_transaction[Repeated_transaction_ID]
            print("Book Returned Successfully :)")
        else:
            print("This book is not borrowed to be returned")
    else:
        print("This book is not borrowed to be returned")


def Print_Books_and_their_IDs():
    for Book_ID , Book_value in Book_Catalog.items():
        print(Book_ID ,"       ", Book_value["Book_Name"] , "       " , Book_value["Book_Genre"])


def Search_for_book(Book_genre , Book_name):
    genre_id = Book_genre[0:2].upper()
    for books_keys in Book_Catalog.keys():
        if books_keys[0:2].upper() == genre_id:
            if Book_Catalog[books_keys]["Book_Name"] == Book_name:
                return f"Book ID : {books_keys} \n Book Genre = {Book_Catalog[books_keys]["Book_Genre"]} \n Book Name = {Book_Catalog[books_keys]["Book_Name"]}\nBook Author = {Book_Catalog[books_keys]["Book_Author"]} \n Book Availability = {Book_Catalog[books_keys]["Book_Availability"]}"

    print("Book Not Found")


def list_borrowed_books():
    for i in borrow_transaction.values():
        if return_transaction:
            for j in return_transaction.values():
                if i["Book_Name"] != j["Book_Name"]:
                    print(i["Book_Name"] , "    " , i["return_date"])
        else:
            print(i["Book_Name"] , "    " , i["return_date"])


def list_overdue_books():
    for i in borrow_transaction.values():
        if return_transaction:
            for j in return_transaction.values():
                if i["Book_Name"] != j["Book_Name"]:
                    current_date = datetime.today().date()
                    return_date = datetime.strptime(i["return_date"],'%Y-%m-%d').date()
                    if return_date < current_date:
                        print(i["Book_Name"])
        else:
            current_date = datetime.today().date()
            return_date = datetime.strptime(i["return_date"],'%Y-%m-%d').date()
            if return_date < current_date:
                print(i["Book_Name"])


def most_popular_books(top = None):
    book_list = []
    for i in borrow_transaction.values():
        book_list.append(i["Book_Name"])

    if top:
        # Count occurrences of each book
        book_counts = Counter(book_list)

        # Get the top N most popular books
        most_popular = book_counts.most_common(top)

        print("Most Popular Books :",most_popular)
    else:
        # Use set() to remove duplicates, then count each element
        frquency_of_books = {item: book_list.count(item) for item in set(book_list)}

        for i , j in frquency_of_books.items():
            print(i,"        ",j)

def register_member():
    Borrowed_books = []
    try:
        Member_number = int(input("Enter Member Number: "))
    except TypeError:
        print("Invalid Input")
        Member_number = int(input("Enter Integer Number for Member Number: "))

    Member_Name = input("Enter Member Name: ")

    Member_ID = ((Member_Name[0:2].upper()) + str(Member_number))

    try:
        if Member_ID in Members:
            raise DuplicatedIDException("Member ID Already Exists")
    except DuplicatedIDException as e:
        print(e)
        Member_number = int(input("you can enter another integer number for member Number (Ensure that member number is valid): "))
        Member_ID = ((Member_Name[0:2].upper()) + str(Member_number))
        try:
            if Member_ID in Members:
                raise DuplicatedIDException("Member ID is also Exist, Information not added")
        except DuplicatedIDException as e:
            print(e)


    Members[Member_ID] = {
        "Member_Name" : Member_Name,
        "Borrowed_books" : Borrowed_books,
        "late_fees" : 0,
    }

    Members_For_monthly_report[Member_ID] = Members[Member_ID]
    print("Member Added Successfully")

def update_member(member_number, Member_Name,Add_new_Borrowed_books=None,Return_Borrowed_books =None , late_fees =None):
    Member_ID = ((Member_Name[0:2].upper()) + str(member_number))
    if Member_ID in Members:
        if Add_new_Borrowed_books:
            Members[Member_ID]["Borrowed_books"].append(Add_new_Borrowed_books)
            Members_Updated_For_monthly_report.append(Member_Name)
            Members_Updated_For_monthly_report.append("Add new Borrowed books")
        if Return_Borrowed_books:
            if Return_Borrowed_books in Members[Member_ID]["Borrowed_books"]:
                Members[Member_ID]["Borrowed_books"].remove(Return_Borrowed_books)
                Members_Updated_For_monthly_report.append(Member_Name)
                Members_Updated_For_monthly_report.append("Return Borrowed books")
            else:
                print("Book Not Found")
        if late_fees:
            try:
                if type(late_fees) is int:
                    Members[Member_ID]["late_fees"] = late_fees
                    Members_Updated_For_monthly_report.append(Member_Name)
                    Members_Updated_For_monthly_report.append("Late Fees")
                    print("Member Updated Successfully")
                else:
                    raise TypeError("Invalid late Fees number")
            except TypeError as e:
                print(e)
    else:
        print("Invalid ID")

def remove_member(member_number , Member_Name):
    Member_ID = ((Member_Name[0:2].upper()) + str(member_number))
    if Member_ID in Members:
        Members_removed_For_monthly_report.append(Member_Name)
        Members.pop(Member_ID)
        print("Member Removed Successfully")

    else:
        print("Book ID Not Found")


def Print_Members_and_their_IDs():
    for Member_ID , Member_value in Members.items():
        print(Member_ID ,"       ", Member_value["Member_Name"])


def Search_For_Member(Member_name):
    member_id = Member_name[0:2].upper()
    for members_keys in Members.keys():
        if members_keys[0:2].upper() == member_id:
            if Members[members_keys]["Member_Name"] == Member_name:
                return f"Member ID : {members_keys} \n Member Name = {Members[members_keys]["Member_Name"]} \n Borrowed Books = {Members[members_keys]["Borrowed_books"]} \n Late Fees = {Members[members_keys]["late_fees"]}"

    print("Member Not Found")


def load_data():
    book_counter = 0
    members_counter = 0
    try:
        with open("Book_File_Management.txt" , "r") as Book_File:
            for line in Book_File.readlines():
                if 0 == book_counter:
                    book_id = line[10:].replace("\n","")
                    book_counter = 1
                elif 1 == book_counter:
                    book_genre = line[13:].replace("\n","")
                    book_counter = 2
                elif 2 == book_counter:
                    book_name = line[12:].replace("\n","")
                    book_counter = 3
                elif 3 == book_counter:
                    book_auther = line[14:].replace("\n","")
                    book_counter = 4
                elif 4 == book_counter:
                    book_availability = int(line[20:])
                    Book_Catalog[book_id] = {
                        "Book_Genre" : book_genre,
                        "Book_Name" : book_name,
                        "Book_Author" : book_auther,
                        "Book_Availability" : book_availability
                    }
                    book_counter = 0
    except FileNotFoundError:
        print("Book_File_Management.txt not found")

    try:
        with open("Member_File_Management.txt" , "r") as Member_File:
            for line in Member_File.readlines():
                if 0 == members_counter:
                    member_id = line[12:].replace("\n","")
                    members_counter = 1
                elif 1 == members_counter:
                    member_name = line[14:].replace("\n","")
                    members_counter = 2
                elif 2 == members_counter:
                    borrowed_book = line[17:].replace("\n","")
                    json_value = borrowed_book.replace("'" , '"')
                    borrowed_book = json.loads(json_value)
                    members_counter = 3
                elif 3 == members_counter:
                    late_fees = int(line[12:])
                    Members[member_id] = {
                        "Member_Name" : member_name,
                        "Borrowed_books" : borrowed_book,
                        "late_fees" : late_fees,
                    }
                    members_counter = 0
    except FileNotFoundError:
        print("Member_File_Management.txt not found")

    # monthly report
    try:
        with open("Files_For_Monthly_Report/Book_for_monthly_report.txt" , "r") as Book_for_monthly_report:
            for line in Book_for_monthly_report.readlines():
                counter = 0
                for i in line:
                    if i == " ":
                        break
                    else:
                        counter += 1
                id = line[0:counter]
                value = str(line[counter+3:].replace("\n",""))
                json_value = value.replace("'" ,'"')
                value = json.loads(json_value)
                Book_Catalog_For_monthly_report[id] = value
    except FileNotFoundError:
        print("Book_for_monthly_report.txt not found")

    try:
        with open("Files_For_Monthly_Report/Book_Updated_for_monthly_report.txt" , "r") as Book_Updated_for_monthly_report:
            for line in Book_Updated_for_monthly_report.readlines():
                Book_Catalog_Updated_For_monthly_report.append(line.replace("\n",""))
    except FileNotFoundError:
        print("Book_Updated_for_monthly_report.txt not found")

    try:
        with open("Files_For_Monthly_Report/Book_Removed_for_monthly_report.txt" , "r") as Book_Removed_for_monthly_report:
            for line in Book_Removed_for_monthly_report.readlines():
                Book_Catalog_removed_For_monthly_report.append(line.replace("\n",""))
    except FileNotFoundError:
        print("Book_Removed_for_monthly_report.txt not found")

    try:
        with open("Files_For_Monthly_Report/Members_For_monthly_report.txt" , "r") as Member_For_monthly_report:
            for line in Member_For_monthly_report.readlines():
                counter = 0
                for i in line:
                    if i == " ":
                        break
                    else:
                        counter += 1
                member_2id = line[0:counter]
                value = line[counter+3:].replace("\n","")
                json_value = value.replace("'",'"')
                value = json.loads(json_value)
                Members_For_monthly_report[member_2id] = value
    except FileNotFoundError:
        print("Members_For_monthly_report.txt not found")

    try:
        with open("Files_For_Monthly_Report/Members_Updated_for_monthly_report.txt" , "r") as members_Updated_for_monthly_report:
            for line in members_Updated_for_monthly_report.readlines():
                Members_Updated_For_monthly_report.append(line.replace("\n",""))
    except FileNotFoundError:
        print("members_Updated_for_monthly_report.txt not found")

    try:
        with open("Files_For_Monthly_Report/Members_removed_for_monthly_report.txt" , "r") as members_Removed_for_monthly_report:
            for line in members_Removed_for_monthly_report.readlines():
                Members_removed_For_monthly_report.append(line.replace("\n",""))
    except FileNotFoundError:
        print("members_Removed_for_monthly_report.txt not found")

    try:
        with open("Files_For_Monthly_Report/Borrow_transaction_For_monthly_report.txt" , "r") as file_borrow_transaction:
            for line in file_borrow_transaction.readlines():
                counter = 0
                for i in line:
                    if i == " ":
                        break
                    else:
                        counter += 1
                id = line[0:counter]
                value = line[counter+3:].replace("\n","")
                json_value = value.replace("'",'"')
                value = json.loads(json_value)
                borrow_transaction_For_monthly_report[id] = value
    except FileNotFoundError:
        print("Borrow_transaction_For_monthly_report.txt not found")

    try:
        with open("Borrow_Transactions.txt" , "r") as file_borrow_transaction:
            for line in file_borrow_transaction.readlines():
                counter = 0
                for i in line:
                    if i == " ":
                        break
                    else:
                        counter += 1
                id = line[0:counter]
                value = line[counter+3:].replace("\n","")
                json_value = value.replace("'",'"')
                value = json.loads(json_value)
                borrow_transaction[id] = value
    except FileNotFoundError:
        print("Borrow_Transactions.txt not found")

    try:
        with open("Files_For_Monthly_Report/Return_transaction_for_monthly_report.txt" , "r") as file_return_transaction:
            for line in file_return_transaction.readlines():
                Monthly_counter = 0
                if line:
                    for i in line:
                        if i == " ":
                            break
                        else:
                            Monthly_counter += 1
                    id = line[0:Monthly_counter]
                    value = line[Monthly_counter+3:].replace("\n","")
                    json_value = value.replace("'",'"')
                    value = json.loads(json_value)
                    return_transaction_For_monthly_report[id] = value
    except FileNotFoundError:
        print("Return_transaction_for_monthly_report.txt not found")

    try:
        with open("Return_Transactions.txt" , "r") as file_return_transaction:
            for line in file_return_transaction.readlines():
                counter = 0
                for i in line:
                    if i == " ":
                        break
                    else:
                        counter += 1
                id = line[0:counter]
                value = line[counter+3:].replace("\n","")
                json_value = value.replace("'",'"')
                value = json.loads(json_value)
                return_transaction[id] = value
    except FileNotFoundError:
        print("Return_transaction.txt not found")

def save_data():
    try:
        with open('Book_File_Management.txt' , 'w') as book_file:
            for book_id , book_value in Book_Catalog.items():
                book_file.write(f"Book ID : {book_id}\n")
                book_file.write(f"Book Genre : {book_value['Book_Genre']}\n")
                book_file.write(f"Book Name : {book_value['Book_Name']}\n")
                book_file.write(f"Book Auther : {book_value['Book_Author']}\n")
                book_file.write(f"Book Availability : {book_value['Book_Availability']}\n")
    except FileNotFoundError:
        print("Book_File_Management.txt not found")

    try:
        with open('Member_File_Management.txt' , 'w') as member_file:
            for member_id , member_value in Members.items():
                member_file.write(f"Member ID : {member_id}\n")
                member_file.write(f"Member Name : {member_value['Member_Name']}\n")
                member_file.write(f"Borrowed books : {member_value['Borrowed_books']}\n")
                member_file.write(f"Late Fees : {member_value['late_fees']}\n")
    except FileNotFoundError:
        print("Member_File_Management.txt not found")
    #save data for monthly report
    try:
        with open("Files_For_Monthly_Report/Book_for_monthly_report.txt","w") as Book_for_monthly_report:
            for book_id , book_value in Book_Catalog_For_monthly_report.items():
                Book_for_monthly_report.write(f"{book_id} : {book_value}\n")
    except FileNotFoundError:
        print("Book_for_monthly_report.txt not found")

    try:
        with open("Files_For_Monthly_Report/Book_Updated_for_monthly_report.txt" , "w") as Book_Updated_for_monthly_report:
            for books in Book_Catalog_Updated_For_monthly_report:
                Book_Updated_for_monthly_report.write(f"{books}\n")
    except FileNotFoundError:
        print("Book_Updated_for_monthly_report.txt not found")

    try:
        with open("Files_For_Monthly_Report/Book_Removed_for_monthly_report.txt" , "w") as Book_Removed_for_monthly_report:
            for books in Book_Catalog_removed_For_monthly_report:
                Book_Removed_for_monthly_report.write(f"{books}\n")
    except FileNotFoundError:
        print("Book_Removed_for_monthly_report.txt not found")

    try:
        with open("Files_For_Monthly_Report/Members_for_monthly_report.txt","w") as Members_for_monthly_report:
            for member_id , member_value in Members_For_monthly_report.items():
                Members_for_monthly_report.write(f"{member_id} : {member_value}\n")
    except FileNotFoundError:
        print("Members_for_monthly_report.txt not found")

    try:
        with open("Files_For_Monthly_Report/Members_Updated_for_monthly_report.txt" , "w") as Members_Updated_for_monthly_report:
            for members in Members_Updated_For_monthly_report:
                Members_Updated_for_monthly_report.write(f"{members}\n")
    except FileNotFoundError:
        print("Members_Updated_for_monthly_report.txt not found")

    try:
        with open("Files_For_Monthly_Report/Members_removed_for_monthly_report.txt" , "w") as members_Removed_for_monthly_report:
            for members in Members_removed_For_monthly_report:
                members_Removed_for_monthly_report.write(f"{members}\n")
    except FileNotFoundError:
        print("Members_removed_for_monthly_report.txt not found")

    try:
        with open("Files_For_Monthly_Report/Borrow_transaction_For_monthly_report.txt" , "w") as Borrow_Transaction:
            for Transaction_id , Transaction_value in borrow_transaction_For_monthly_report.items():
                Borrow_Transaction.write(f"{Transaction_id} : {Transaction_value}\n")
    except FileNotFoundError:
        print("Borrow_transaction_For_monthly_report.txt not found")

    try:
        with open("Files_For_Monthly_Report/Return_transaction_for_monthly_report.txt" , "w") as Return_Transaction:
            for Transaction_id , Transaction_value in return_transaction_For_monthly_report.items():
                Return_Transaction.write(f"{Transaction_id} : {Transaction_value}\n")
    except FileNotFoundError:
        print("Return_transaction_for_monthly_report.txt not found")

    try:
        with open("Borrow_Transactions.txt" , "w") as Borrow_Transaction:
            for Transaction_id , Transaction_value in borrow_transaction.items():
                Borrow_Transaction.write(f"{Transaction_id} : {Transaction_value}\n")
    except FileNotFoundError:
        print("Borrow_Transactions.txt not found")

    try:
        with open("Return_Transactions.txt" , "w") as Return_Transaction:
            for Transaction_id , Transaction_value in return_transaction.items():
                Return_Transaction.write(f"{Transaction_id} : {Transaction_value}\n")
    except FileNotFoundError:
        print("Return_Transactions.txt not found")

#Additional Feature
def Monthly_Report():
    print("books has been added in this month is:")
    print("Book IDs    Book Names   Book Genres    Book Authers    Book Availabilities")
    print("-----------------------------------------------------------------------------")
    for Book_ID , Book_value in Book_Catalog_For_monthly_report.items():
        print(Book_ID ,"      ", Book_value["Book_Name"] , "     " , Book_value["Book_Genre"] , "      " , Book_value["Book_Author"] , "       " , Book_value["Book_Availability"])

    print("*****************************************************************************")
    print("Books Updated during this month")
    print("Book Name        Parameter that had been updated")
    print("-------------------------------------------------")
    update_counter = 0
    while update_counter in range(len(Book_Catalog_Updated_For_monthly_report)):
        print(Book_Catalog_Updated_For_monthly_report[update_counter] , end="        ")
        update_counter +=1
        print(Book_Catalog_Updated_For_monthly_report[update_counter])
        update_counter +=1

    remove_counter = 0
    print("*****************************************************************************")
    print("Books Removed during this month")
    print("Book Name        Book Genre")
    print("-------------------------------------------------")
    while remove_counter in range(len(Book_Catalog_removed_For_monthly_report)):
        print(Book_Catalog_removed_For_monthly_report[remove_counter] , end="        ")
        remove_counter += 1
        print(Book_Catalog_removed_For_monthly_report[remove_counter])
        remove_counter += 1
    print("*************************************************************")
    print("Members has been added during this month :")
    print("Member IDs    Member Names      Members Borrowed Books        Late Fees")
    print("-------------------------------------------------------------------------")
    for member_ID , member_value in Members_For_monthly_report.items():
        print(member_ID ,"    ", member_value["Member_Name"] , "      " , member_value["Borrowed_books"] , "        " , member_value["late_fees"] )

    print("*************************************************************")
    print("Members Updated during this month")
    print("Member Name        Parameter that had been updated")
    print("---------------------------------------------------")
    update_members_counter = 0
    while update_members_counter in range(len(Members_Updated_For_monthly_report)):
        print(Members_Updated_For_monthly_report[update_members_counter] , end="        ")
        update_members_counter +=1
        print(Members_Updated_For_monthly_report[update_members_counter])
        update_members_counter +=1

    print("*************************************************************")
    print("Members Removed during this month")
    for members in Members_removed_For_monthly_report:
        print(members)

    print("**********************************************************************")
    print("Borrow Transactions during this month")
    print("Transaction IDs         Transaction_Specifications")
    print("---------------------------------------------------")
    for Transaction_id , Transaction_values in borrow_transaction_For_monthly_report.items():
        print(Transaction_id , "         " , Transaction_values)

    print("**********************************************************************")
    print("Return Transactions during this month")
    print("Transaction IDs         Transaction_Specifications")
    print("---------------------------------------------------")
    for Transaction_id , Transaction_values in return_transaction_For_monthly_report.items():
        print(Transaction_id , "         " , Transaction_values)

    print("**********************************************************************")
    print("All borrowed books and their return date during this month ")
    print("Book Name        return date")
    print("-----------------------------")
    for i in borrow_transaction_For_monthly_report.values():
        if return_transaction_For_monthly_report:
            for j in return_transaction_For_monthly_report.values():
                if i["Book_Name"] != j["Book_Name"]:
                    print(i["Book_Name"] , "    " , i["return_date"])
        else:
            print(i["Book_Name"] , "    " , i["return_date"])
    print("**********************************************************************")
    print("All overdues books during this month ")
    for i in borrow_transaction_For_monthly_report.values():
        if return_transaction_For_monthly_report:
            for j in return_transaction_For_monthly_report.values():
                if i["Book_Name"] != j["Book_Name"]:
                    current_date = datetime.today().date()
                    return_date = datetime.strptime(i["return_date"],'%Y-%m-%d').date()
                    if return_date < current_date:
                        print(i["Book_Name"])
        else:
            current_date = datetime.today().date()
            return_date = datetime.strptime(i["return_date"],'%Y-%m-%d').date()
            if return_date < current_date:
                print(i["Book_Name"])
    print("**********************************************************************")
    print("print most five common books had borrowed this month")
    book_list = []
    for i in borrow_transaction_For_monthly_report.values():
        book_list.append(i["Book_Name"])

    # Count occurrences of each book
    book_counts = Counter(book_list)

    # Get the top N most popular books
    most_popular = book_counts.most_common(5)

    print(most_popular)
    print("**********************************************************************")
    Book_Catalog_For_monthly_report.clear()
    Book_Catalog_Updated_For_monthly_report.clear()
    Book_Catalog_removed_For_monthly_report.clear()

    Members_For_monthly_report.clear()
    Members_Updated_For_monthly_report.clear()
    Members_removed_For_monthly_report.clear()

    borrow_transaction_For_monthly_report.clear()
    return_transaction_For_monthly_report.clear()

# User Interface
load_data()
print("Hello sir, Welcome to Library Management System")

# monthly Report
current_day = datetime.today().day
if 1 == current_day:
    print("Do you want to print monthly report")
    print("1) NO")
    print("2) YES")
    try:
        choice = int(input("Enter Your Choice: "))
        if 2 == choice:
            Monthly_Report()
            print("Monthly Report Ended")
        elif 1 == choice:
            pass
        else:
            raise Exception ("Invalid Choice")
    except Exception as e:
        print(e)


print("the operations you can do")
print("1) Add New Book")
print("2) Update Book")
print("3) Remove Book")
print("4) Register New Member")
print("5) Update Information of Member")
print("6) Delete Member from system")
print("7) Borrow Book ")
print("8) Return Borrowed Book")
print("9) List of all Borrowed Books")
print("10) List of Overdue Books (books that required to be returned)")
print("11) print all books and number of times that the book had borrowed")
print("12) Most Popular Books")
print("13) Print all books and their IDs")
print("14) Print all Members and their IDs")
print("15) Search for specific book")
print("16) Search for specific Member")
print("17) Exit")

while True:
    try:
        operation = int(input("Enter operation choice: "))
        if not (operation <= 17 and operation > 0):
            raise Exception ("Invalid Choice")
    except Exception as e:
        print(e)
        break

    if operation == 1:
        add_book()
        print("*****************************")
        print("you want another operation")
        print("1) NO")
        print("2) YES")
        try:
            ckeck_operation = int(input("Enter your choice: "))
        except TypeError:
            print("Invalid Input")
            ckeck_operation = int(input("Enter Integer Number For your choice: "))

        try:
            if ckeck_operation == 1 or ckeck_operation == 2:
                if ckeck_operation == 1:
                    break
                elif ckeck_operation == 2:
                    pass
            else:
                raise Exception("Invalid Input")
        except Exception as e:
            print(e)
            break

    elif operation == 2:
        try:
            book_number = int(input("Enter Book Number: "))
        except ValueError:
            print("You should enter integer number")
            book_number = int(input("Please enter integer number for Book Number: "))
        book_genre = input("Enter Book Genre: ")

        Book_ID = ((book_genre[0:2].upper()) + str(book_number))
        if Book_ID not in Book_Catalog:
            print("Invalid Book ID")
        else:
            print("1) book name")
            print("2) book author")
            print("3) Book Availability")
            print("4) Update three Parameters")
            try:
                update_parameter = int(input("please enter parameter you want to update: "))
                while True:
                    if update_parameter == 1:
                        book_name = input("Enter Book Name: ")
                        update_book(book_number , book_genre, Book_Name = book_name)
                        break
                    elif update_parameter == 2:
                        book_author = input("Enter Book Author: ")
                        update_book(book_number , book_genre, Book_Author = book_author)
                        break
                    elif update_parameter == 3:
                        book_availability = int(input("Enter Book Availability: "))
                        update_book(book_number , book_genre, Book_Availability = book_availability)
                        break
                    elif update_parameter == 4:
                        book_name = input("Enter Book Name: ")
                        book_author = input("Enter Book Author: ")
                        book_availability = int(input("Enter Book Availability: "))
                        update_book(book_number , book_genre, Book_Name = book_name,Book_Author = book_author ,Book_Availability = book_availability)
                    else:
                        print("Invalid Choice")
                        update_parameter = int(input("please enter parameter you want to update: "))
            except ValueError:
                print("Invalid Input, Only Integer Numbers are allowed")
                break

        print("*****************************")
        print("you want another operation")
        print("1) NO")
        print("2) YES")
        try:
            ckeck_operation = int(input("Enter your choice: "))
        except TypeError:
            print("Invalid Input")
            ckeck_operation = int(input("Enter Integer Number For your choice: "))

        try:
            if ckeck_operation == 1 or ckeck_operation == 2:
                if ckeck_operation == 1:
                    break
                elif ckeck_operation == 2:
                    pass
            else:
                raise Exception("Invalid Input")
        except Exception as e:
            print(e)
            break

    elif operation == 3:
        try:
            book_number = int(input("Enter Book Number to be deleted : "))
        except ValueError:
            print("You should Enter integer number")
            book_number = int(input("Please Enter Integer number for Book Number to be deleted : "))

        book_genre = input("Enter Book Genre: ")
        remove_book(book_number , book_genre)
        print("*****************************")
        print("you want another operation")
        print("1) NO")
        print("2) YES")
        try:
            ckeck_operation = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid Input")
            ckeck_operation = int(input("Enter Integer Number For your choice: "))

        try:
            if ckeck_operation == 1 or ckeck_operation == 2:
                if ckeck_operation == 1:
                    break
                elif ckeck_operation == 2:
                    pass
            else:
                raise Exception("Invalid Input")
        except Exception as e:
            print(e)
            break

    elif operation == 4:
        register_member()
        print("*****************************")
        print("you want another operation")
        print("1) NO")
        print("2) YES")
        try:
            ckeck_operation = int(input("Enter your choice: "))
        except TypeError:
            print("Invalid Input")
            ckeck_operation = int(input("Enter Integer Number For your choice: "))

        try:
            if ckeck_operation == 1 or ckeck_operation == 2:
                if ckeck_operation == 1:
                    break
                elif ckeck_operation == 2:
                    pass
            else:
                raise Exception("Invalid Input")
        except Exception as e:
            print(e)
            break

    elif operation == 5:
        try:
            member_number = int(input("Enter Member Number: "))
        except ValueError:
            print("you should enter integer number")
            member_number = int(input("please Enter Integer number for Member Number: "))

        member_name = input("Enter Member Name: ")

        Member_ID = ((member_name[0:2].upper()) + str(member_number))
        if Member_ID not in Members:
            print("Invalid Member ID")
        else:
            print("1) Add new Borrowed books")
            print("2) Return Borrowed books")
            print("3) change late fees")
            print("4) Update three Parameters")
            try:
                update_parameter = int(input("please enter parameter you want to update : "))
                while True:
                    if update_parameter == 1:
                        borrowed_book = input("Enter new Borrowed books: ")
                        update_member(member_number , member_name, Add_new_Borrowed_books = borrowed_book)
                        break
                    elif update_parameter == 2:
                        return_book_var = input("Enter Return books: ")
                        update_member(member_number , member_name, Return_Borrowed_books = return_book_var)
                        break
                    elif update_parameter == 3:
                        late_fees = int(input("Enter late fees: "))
                        update_member(member_number , member_name, late_fees = late_fees)
                        break
                    elif update_parameter == 4:
                        borrowed_book = input("Enter new Borrowed books: ")
                        return_book_var = input("Enter Return books: ")
                        late_fees = int(input("Enter late fees: "))
                        update_member(member_number , member_name, Add_new_Borrowed_books = borrowed_book, Return_Borrowed_books = return_book_var ,late_fees = late_fees)
                    else:
                        print("Invalid Choice")
                        update_parameter = int(input("please enter parameter you want to update : "))
            except ValueError:
                print("you should enter integer number")
                update_parameter = int(input("please enter integer number for parameter you want to update : "))

        print("*****************************")
        print("you want another operation")
        print("1) NO")
        print("2) YES")
        try:
            ckeck_operation = int(input("Enter your choice: "))
        except TypeError:
            print("Invalid Input")
            ckeck_operation = int(input("Enter Integer Number For your choice: "))

        try:
            if ckeck_operation == 1 or ckeck_operation == 2:
                if ckeck_operation == 1:
                    break
                elif ckeck_operation == 2:
                    pass
            else:
                raise Exception("Invalid Input")
        except Exception as e:
            print(e)
            break

    elif operation == 6:
        try:
            member_number = int(input("Enter member Number  : "))
        except ValueError:
            print("you should enter integer number")
            member_number = int(input("please Enter Integer number for Member Number to be deleted: "))

        member_name = input("Enter number name: ")
        remove_member(member_number , member_name)
        print("*****************************")
        print("you want another operation")
        print("1) NO")
        print("2) YES")
        try:
            ckeck_operation = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid Input")
            ckeck_operation = int(input("Enter Integer Number For your choice: "))

        try:
            if ckeck_operation == 1 or ckeck_operation == 2:
                if ckeck_operation == 1:
                    break
                elif ckeck_operation == 2:
                    pass
            else:
                raise Exception("Invalid Input")
        except Exception as e:
            print(e)
            break

    elif operation == 7:
        try:
            book_number = int(input("Enter book number :"))
        except ValueError:
            print("you should enter integer number")
            book_number = int(input("please Enter Integer number for book Number: "))
        book_genre =  input("Enter book Genre :")
        try:
            member_number = int(input("Enter member Number borrowing this book: "))
        except ValueError:
            print("you should enter integer number")
            member_number = int(input("please Enter Integer number for Member Number: "))
        member_name = input("Enter member Name : ")
        return_date = input("Enter a return date (YYYY-MM-DD): ")
        user_return_date = datetime.strptime(return_date, "%Y-%m-%d").date()

        borrow_book(book_number , book_genre , member_number , member_name, user_return_date)
        print("*****************************")
        print("you want another operation")
        print("1) NO")
        print("2) YES")
        try:
            ckeck_operation = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid Input")
            ckeck_operation = int(input("Enter Integer Number For your choice: "))

        try:
            if ckeck_operation == 1 or ckeck_operation == 2:
                if ckeck_operation == 1:
                    break
                elif ckeck_operation == 2:
                    pass
            else:
                raise Exception("Invalid Input")
        except Exception as e:
            print(e)
            break

    elif operation == 8:

        try:
            book_number = int(input("Enter book number :"))
        except ValueError:
            print("you should enter integer number")
            book_number = int(input("please Enter Integer number for book Number: "))
        book_genre =  input("Enter book Genre :")
        try:
            member_number = int(input("Enter member Number return this book: "))
        except ValueError:
            print("you should enter integer number")
            member_number = int(input("please Enter Integer number for Member Number: "))
        member_name = input("Enter member Name : ")

        return_book(book_number , book_genre , member_number , member_name)
        print("*****************************")
        print("you want another operation")
        print("1) NO")
        print("2) YES")
        try:
            ckeck_operation = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid Input")
            ckeck_operation = int(input("Enter Integer Number For your choice: "))

        try:
            if ckeck_operation == 1 or ckeck_operation == 2:
                if ckeck_operation == 1:
                    break
                elif ckeck_operation == 2:
                    pass
            else:
                raise Exception("Invalid Input")
        except Exception as e:
            print(e)
            break

    elif operation == 9:

        print("Borrowed Books :")
        list_borrowed_books()
        print("****************************")
        print("you want another operation")
        print("1) NO")
        print("2) YES")
        try:
            ckeck_operation = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid Input")
            ckeck_operation = int(input("Enter Integer Number For your choice: "))

        try:
            if ckeck_operation == 1 or ckeck_operation == 2:
                if ckeck_operation == 1:
                    break
                elif ckeck_operation == 2:
                    pass
            else:
                raise Exception("Invalid Input")
        except Exception as e:
            print(e)
            break

    elif operation == 10:

        print("Overdue Books :")
        list_overdue_books()
        print("*****************************")
        print("you want another operation")
        print("1) NO")
        print("2) YES")
        try:
            ckeck_operation = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid Input")
            ckeck_operation = int(input("Enter Integer Number For your choice: "))

        try:
            if ckeck_operation == 1 or ckeck_operation == 2:
                if ckeck_operation == 1:
                    break
                elif ckeck_operation == 2:
                    pass
            else:
                raise Exception("Invalid Input")
        except Exception as e:
            print(e)
            break

    elif operation == 11:
        print("Books      Number of times")
        most_popular_books()
        print("*****************************")
        print("you want another operation")
        print("1) NO")
        print("2) YES")
        try:
            ckeck_operation = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid Input")
            ckeck_operation = int(input("Enter Integer Number For your choice: "))

        try:
            if ckeck_operation == 1 or ckeck_operation == 2:
                if ckeck_operation == 1:
                    break
                elif ckeck_operation == 2:
                    pass
            else:
                raise Exception("Invalid Input")
        except Exception as e:
            print(e)
            break

    elif operation == 12:
        try:
            top = int(input("Enter number of most common books you want to be printed : "))
        except TypeError:
            print("you should enter integer number")
            top = int(input("please Enter number of most common books you want to be printed : "))
        most_popular_books(top = top)
        print("*****************************")
        print("you want another operation")
        print("1) NO")
        print("2) YES")
        try:
            ckeck_operation = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid Input")
            ckeck_operation = int(input("Enter Integer Number For your choice: "))

        try:
            if ckeck_operation == 1 or ckeck_operation == 2:
                if ckeck_operation == 1:
                    break
                elif ckeck_operation == 2:
                    pass
            else:
                raise Exception("Invalid Input")
        except Exception as e:
            print(e)
            break

    elif operation == 13:
        print("Book ID      Book Name      Book Genre")
        Print_Books_and_their_IDs()
        print("****************************************")
        print("you want another operation")
        print("1) NO")
        print("2) YES")
        try:
            ckeck_operation = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid Input")
            ckeck_operation = int(input("Enter Integer Number For your choice: "))

        try:
            if ckeck_operation == 1 or ckeck_operation == 2:
                if ckeck_operation == 1:
                    break
                elif ckeck_operation == 2:
                    pass
            else:
                raise Exception("Invalid Input")
        except Exception as e:
            print(e)
            break

    elif operation == 14:
        print("Member ID       Member Name")
        Print_Members_and_their_IDs()
        print("***************************")
        print("you want another operation")
        print("1) NO")
        print("2) YES")
        try:
            ckeck_operation = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid Input")
            ckeck_operation = int(input("Enter Integer Number For your choice: "))

        try:
            if ckeck_operation == 1 or ckeck_operation == 2:
                if ckeck_operation == 1:
                    break
                elif ckeck_operation == 2:
                    pass
            else:
                raise Exception("Invalid Input")
        except Exception as e:
            print(e)
            break

    elif operation == 15:
        book_genre = input("Enter book Genre : ")
        book_name = input("Enter Book Name : ")
        print(Search_for_book(book_genre , book_name))
        print("*********************************")
        print("you want another operation")
        print("1) NO")
        print("2) YES")
        try:
            ckeck_operation = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid Input")
            ckeck_operation = int(input("Enter Integer Number For your choice: "))

        try:
            if ckeck_operation == 1 or ckeck_operation == 2:
                if ckeck_operation == 1:
                    break
                elif ckeck_operation == 2:
                    pass
            else:
                raise Exception("Invalid Input")
        except Exception as e:
            print(e)
            break

    elif operation == 16:

        Member_name = input("Enter Member Name : ")
        print(Search_For_Member(Member_name))
        print("*********************************")
        print("you want another operation")
        print("1) NO")
        print("2) YES")
        try:
            ckeck_operation = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid Input")
            ckeck_operation = int(input("Enter Integer Number For your choice: "))

        try:
            if ckeck_operation == 1 or ckeck_operation == 2:
                if ckeck_operation == 1:
                    break
                elif ckeck_operation == 2:
                    pass
            else:
                raise Exception("Invalid Input")
        except Exception as e:
            print(e)
            break

    elif operation == 17:
        break
    else:
        print("Invalid Choice")
        operation = int(input("Enter operation choice: "))

save_data()
print("Thank you for your visit , see you soon")

