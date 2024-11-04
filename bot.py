from datetime import datetime
from address_book import AddressBook
from serialize import save_data, load_data


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value: str):
        if len(value) == 10:
            super().__init__(value)
        else:
            raise ValueError("Phone number must be 10 digits")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)} {self.birthday if self.birthday else None}"

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    def edit_phone(self, old_phone, new_phone):
        edited = False
        for p in self.phones:
            if p.value == old_phone:
                if len(new_phone) == 10:
                    p.value = new_phone
                    edited = True
                else:
                    raise ValueError("Phone number must be 10 digits")
        if not edited:
            raise ValueError("Phone number not found")

    def find_phone(self, n):
        for phone in self.phones:
            if phone.value == n:
                return phone


class Birthday(Field):
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
            if len(value) == 10:
                date_obj = datetime.strptime(value, "%d.%m.%Y").date()
                super().__init__(date_obj)
            else:
                raise ValueError()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return f"Birthday: {self.value.strftime('%d.%m.%Y')}"


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(str(e))

    return inner


@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Please provide both a name and a phone number.")

    name, phone, *_ = args
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
def edit_contact(args, book):
    if len(args) < 3:
        raise ValueError("Please provide a name, old phone number, and new phone number.")

    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        return "Contact not found."
    record.edit_phone(old_phone, new_phone)
    return message


@input_error
def add_birthday(args, book):
    if len(args) < 2:
        raise ValueError("Please provide both a name and a birthday (in DD.MM.YYYY format).")

    name, birthday, *_ = args
    record = book.find(name)
    message = "Birthday added."
    if record is None:
        return "Contact not found."
    if birthday:
        record.add_birthday(birthday)
    return message


@input_error
def show_birthday(args, book):
    if len(args) < 1:
        raise ValueError("Please provide a name to show the birthday.")

    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    return record.birthday


@input_error
def phones(args, book):
    if len(args) < 1:
        raise ValueError("Please provide a name to show the phone numbers.")

    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    output = ", ".join(map(lambda phone: phone.value, record.phones))
    return f"User phones: {output}"


@input_error
def all_contacts(args, book):
    return str(book)


@input_error
def birthdays(args, book):
    today = datetime.today().date()
    upcoming_birthdays = {}
    for name, record in book.data.items():
        if record.birthday:
            this_year_birthday = datetime(today.year, record.birthday.value.month, record.birthday.value.day).date()
            if this_year_birthday < today:
                this_year_birthday = datetime(today.year + 1, record.birthday.value.month,
                                              record.birthday.value.day).date()
            days_until_birthday = (this_year_birthday - today).days
            if 0 <= days_until_birthday <= 7:
                upcoming_birthdays[name] = record.birthday

    if not upcoming_birthdays:
        return "No upcoming birthdays."
    output = ', '.join(f"{name}: {birthday}" for name, birthday in upcoming_birthdays.items())
    return f"Upcoming birthday{'s' if len(upcoming_birthdays) > 1 else ''} for {output}"


def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(edit_contact(args, book))

        elif command == "phone":
            print(phones(args, book))

        elif command == "all":
            print(all_contacts(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
