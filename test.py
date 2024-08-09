class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
          self.phones.append(phone)

class Book:
    def __init__(self):
        self.data = {}

    def add(self, record):
        self.data[record.name.value] = record
