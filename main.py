from collections import UserDict
from datetime import datetime, timedelta
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if self.validate(value):
            super().__init__(value)
        else:
            raise ValueError("Invalid phone, needed 10 numbers")
        

    @staticmethod
    def validate(value):
        return bool(re.fullmatch(r'\d{10}', value))
        
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        phone = Phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone_to_remove):
          for phone in self.phones:
                if phone == phone_to_remove:
                    index = self.phones.index(phone)
                    self.phones.pop(index)
                else:
                    pass

    def edit_phone(self, old, new):
        if old in self.phones:
            self.remove_phone(old)
            self.add_phone(new)
        else:
            comment = 'we dont have such number, try another'
            raise ValueError(comment)

    def find_phone(self, phone):
        if phone in self.phones:
            return phone
        else:
            return None
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def get_bd(self):
        return self.birthday
    
    def get_name(self):
        return self.name
    
    def get_phone(self):
        return self.phones
            

    def __str__(self):
        phones_str = '; '.join(self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {self.birthday}"

#birthday block

def string_to_date(date_string):
    return datetime.strptime(date_string, "%Y.%m.%d").date()

def date_to_string(date):
    return date.strftime("%Y.%m.%d")

def prepare_user_list(user_data):
    prepared_list = []
    for user in user_data:
        prepared_list.append({"name": user["name"], "birthday": string_to_date(user["birthday"])})
    return prepared_list

def find_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)

def adjust_for_weekend(birthday):
    if birthday.weekday() >= 5:
        return find_next_weekday(birthday, 0)
    return birthday    

class AddressBook(UserDict):

    def __init__(self):
        self.data = {}

    def add_record(self, Record):
        self.data[Record.name.value] = Record

    def find(self, name):
        if name in self.data:
            obj = self.data[name]
            return obj
        else:
            return None
        
    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            return 'we dont have this number'
    
    def __str__(self):
        keys = list(self.data.keys())
        counter = 0
        result = ''
        while counter < len(keys)-1:
            person_data = self.data[keys[counter]]
            counter +=1
            new_str = f'{person_data}\n'
            result += new_str
        else:
            person_data = self.data[keys[counter]]
            new_str = f'{person_data}'
            result += new_str
        return result
    
    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = datetime.today()
        # print(type(today))

        for user in self.data:
            user_data = self.data[user]
            bd = datetime.strptime(user_data.get_bd(), '%d.%m.%Y')
            
            birthday_this_year = bd.replace(year=today.year)
            # print(birthday_this_year)
            if birthday_this_year < today:
                birthday_this_year = bd.replace(year=today.year+1)
                

            if 0 <= (birthday_this_year - today).days <= days:
                birthday_this_year = adjust_for_weekend(birthday_this_year)

            congratulation_date_str = date_to_string(birthday_this_year)
            name = str(user_data.get_name())
            upcoming_birthdays.append({"name": name, "congratulation_date": congratulation_date_str})
        return upcoming_birthdays
    
# bot block
# decorators

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "We don't have this name in data base, try another"
        except IndexError:
            return "Please try pattern 'add Bob 1234567890'"
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split(' ')
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
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
def change_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    if record:
        phones = record.get_phone()
        phone_to_remove = phones[0]
        record.remove_phone(phone_to_remove)
        record.add_phone(phone)
        message = "Contact updated."
        return message

@input_error
def show_phone(args, book: AddressBook):
    name = args
    record = book.find(name)
    if record:
        return record.get_phone()
    else:
        print('we dont have this contact')

def show_all(args, book: AddressBook):
    return book

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    record.add_birthday(birthday)
    message = "Birthday added."
    return message

@input_error
def show_birthday(args, book: AddressBook):
    name = args
    record = book.find(name)
    if record:
        return record.get_bd()

@input_error
def birthdays(args, book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    return upcoming_birthdays

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

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
            print(show_all(args, book))
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

# book = AddressBook()
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")
# john_record.add_birthday('10.10.2005')
# book.add_record(john_record)

# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# jane_record.add_birthday('11.11.2001')
# book.add_record(jane_record)

# upcoming_birthdays = book.get_upcoming_birthdays()
# print(upcoming_birthdays)

# find_jane = book.find('Jane')
# print(find_jane)

#  add john 12345
#  add jane 987654
#  add-birthday john 01.01.2001
#  add-birthday jane 02.02.2001
#  show-birthday john
#  birthdays
