from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
		pass

class Phone(Field):
    def validation(self, value):
        if len(int(value)) != 10:
             raise ValueError('phone should have 10 numbers')
        else:
            self.value = value

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
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
          pass
            

    def __str__(self):
        phones_str = '; '.join(self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"
        

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
        str = ', '.join(self.data)
        return str
        # return str(self.data)

book = AddressBook()

john_record = Record("John")

john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

find_jane = book.find('Jane')

print(find_jane)
print(book)

book.delete('Jane')

print(book)