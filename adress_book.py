from faker import Faker
from datetime import datetime,timedelta
from functools import wraps

fake = Faker()


class BaseContact:
    def __init__(self, name, address, email, work_phone):
        self.name = name
        self.address = address
        self.email = email
        self.home_phone = work_phone
        self._label_lenght = len(self.name)

    def contact(self):
        print(f'Wybieram numer telefonu {self.home_phone} i dzwonię do {self.name}')

    def __str__(self):
        return f'{self.name}, {self.address}, {self.email}, {self.home_phone}'

    @property
    def label_lenght(self):
        return self._label_lenght

    @label_lenght.setter
    def label_lenght(self, value):
        self._label_lenght = value


class BusinessContact(BaseContact):
    def __init__(self, company, job, work_phone, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company = company
        self.job = job
        self.work_phone = work_phone

    def __str__(self):
        return f'{self.name}, {self.company}, {self.email}, {self.work_phone}'

    def contact(self):
        print(f'Wybieram numer {self.work_phone} i dzwonię do {self.name}')

def runtime(func):
    start = datetime.now()
    func()
    end = datetime.now()
    difference = end - start
    print(f'Wykonanie funkcji zajęło {difference} czasu')

@runtime
def create_contacts():
    card_type = BusinessContact
    ammount = 1000000
    name = fake.name()
    address = fake.address()
    email = fake.email()
    home_phone = fake.phone_number()
    company = fake.company()
    job = fake.job()
    work_phone = fake.phone_number()
    if card_type == BusinessContact:
        return [card_type(company, job, work_phone, name, address, email, home_phone) for _ in range(ammount)]
    elif card_type == BaseContact:
        return [card_type(name, address, email, home_phone) for _ in range(ammount)]

