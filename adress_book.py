from faker import Faker

fake = Faker()

random_plp = [(fake.name(), fake.address(), fake.email(), fake.company(), fake.job()) for _ in range(5)]


class BusinessCard:
    def __init__(self):
        self.name = fake.name()
        self.address = fake.address()
        self.email = fake.email()
        self.company = fake.company()
        self.job = fake.job()

    def __str__(self):
        return f'{self.name}, {self.address}, {self.email}, {self.company}, {self.job}'


wizytowka1 = BusinessCard()
wizytowka2 = BusinessCard()
wizytowka3 = BusinessCard()
wizytowka4 = BusinessCard()
wizytowka5 = BusinessCard()
lista_wizytowek = [wizytowka1, wizytowka2, wizytowka3, wizytowka4, wizytowka5]
by_name = (sorted(lista_wizytowek, key=lambda card: card.email))
for i in range(len(by_name)):
    print(by_name[i])
