from assignments.bot import AddressBook, Record, parse_input, add_contact, change_contact, show_phone, show_all, add_birthday, show_birthday, birthdays


def main():
    book = AddressBook()
    record = Record("John")
    record.add_phone("1234567890")
    record.add_birthday("13.11.2025")
    book.add_record(record)
    record = Record("Jane")
    record.add_phone("9876543210")
    record.add_birthday("12.11.2025")
    book.add_record(record)
    record = Record("Jim")
    record.add_phone("1112223333")
    record.add_birthday("19.11.2025")
    book.add_record(record)

    print(book.get_upcoming_birthdays())
    
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))
        
        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
