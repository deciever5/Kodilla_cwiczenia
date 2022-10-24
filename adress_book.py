from faker import Faker

fake = Faker()


class BaseContact:
    def __init__(self):
        self.name = fake.name()
        self.address = fake.address()
        self.email = fake.email()
        self.home_phone = fake.phone_number()
        self._name_len = len(self.name)

    def contact(self):
        print(f'Wybieram numer telefonu {self.home_phone} i dzwonię do {self.name}')

    def __str__(self):
        return f'{self.name}, {self.address}, {self.email}, {self.home_phone}'

    def label_length(self):
        print(len(self.name))
        return len(self.name)


class BusinessContact(BaseContact):
    def __init__(self):
        super().__init__()
        self.company = fake.company()
        self.job = fake.job()
        self.work_phone = fake.phone_number()

    def __str__(self):
        return f'{self.name}, {self.company}, {self.email}, {self.work_phone}'

    def contact(self):
        print(f'Wybieram numer {self.work_phone} i dzwonię do {self.name}')




lista_wizytowek = [BaseContact() for _ in range(5)]
lista_wizytowek2 = [BusinessContact() for _ in range(5)]
lista_wizytowek[0].contact()
lista_wizytowek2[0].contact()
print(lista_wizytowek2[0].label_length())
