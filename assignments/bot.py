from collections import UserDict
from typing import Tuple, List
from datetime import datetime, timedelta


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Error: Contact not found."
        except ValueError as e:
            if "Phone" in str(e):
                return f"Error: {e}"
            elif "date" in str(e).lower():
                return f"Error: {e}"
            else:
                return "Error: Give me name and phone please."
        except IndexError:
            return "Error: Enter user name."

    return inner

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        phone = self.find_phone(old_phone)
        if phone:
            new_phone_obj = Phone(new_phone)
            phone.value = new_phone_obj.value
            return
        raise ValueError(f"Phone {old_phone} not found")

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)
            return
        raise ValueError(f"Phone {phone} not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self):
        """
        Визначає дні народження на наступні 7 днів та переносить
        вихідні на понеділок
        """
        upcoming_birthdays = []
        today = datetime.today().date()

        for user in self.data.values():
            # Перевіряємо, чи є день народження
            if not user.birthday:
                continue

            # Отримуємо дату народження з Birthday об'єкта
            birthday = user.birthday.value.date()

            # Визначаємо день народження в цьому році
            birthday_this_year = birthday.replace(year=today.year)

            # Якщо день народження вже минув в цьому році,
            # розглядаємо наступний рік
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(
                    year=today.year + 1
                )

            # Визначаємо різницю в днях
            days_until_birthday = (birthday_this_year - today).days

            # Перевіряємо, чи день народження в наступні 7 днів
            if 0 <= days_until_birthday <= 7:
                # Переносимо на понеділок, якщо вихідний
                congratulation_date = self.move_birthday_to_weekday(
                    birthday_this_year
                )

                upcoming_birthdays.append({
                    'name': user.name.value,
                    'congratulation_date': congratulation_date.strftime(
                        '%Y.%m.%d'
                    )
                })

        return upcoming_birthdays

    def move_birthday_to_weekday(self, birthday_date):
        """
        Переносить день народження на наступний понеділок, якщо він припадає на вихідний
        """
        # 5 = субота, 6 = неділя
        if birthday_date.weekday() == 5:  # субота
            return birthday_date + timedelta(days=2)  # переносимо на понеділок
        elif birthday_date.weekday() == 6:  # неділя
            return birthday_date + timedelta(days=1)  # переносимо на понеділок
        else:
            return birthday_date  # залишаємо як є

class Birthday(Field):
    # DD.MM.YYYY format
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book):
    if len(args) < 3:
        raise ValueError("Give me name, old phone and new phone please.")
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error
def show_phone(args, book):
    if len(args) < 1:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if record.phones:
        return "; ".join(p.value for p in record.phones)
    else:
        return "No phones for this contact."

@input_error
def show_all(book):
    if not book.data:
        return "No contacts stored."
    result = []
    for _, record in book.data.items():
        result.append(str(record))
    return "\n".join(result)

@input_error
def add_birthday(args, book):
    if len(args) < 2:
        raise ValueError("Give me name and birthday please.")
    name, birthday = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book):
    if len(args) < 1:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if record.birthday:
        return str(record.birthday)
    else:
        return "No birthday set for this contact."
    
@input_error
def birthdays(book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays for the next week."
    result = []
    for item in upcoming:
        result.append(f"{item['name']}: {item['congratulation_date']}")
    return "\n".join(result)

def parse_input(user_input: str) -> Tuple[str, List[str]]:
    parts = user_input.split()
    if not parts:
        return "", []
    cmd, *args = parts
    return cmd.strip().lower(), args


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
