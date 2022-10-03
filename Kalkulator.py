import logging

logging.basicConfig(level=logging.DEBUG)

choice = input \
    ("Podaj działanie, posługując się odpowiednią liczbą: 1 Dodawanie, 2 Odejmowanie, 3 Mnożenie, 4 Dzielenie:")
num1 = input("Podaj składnik 1: ")
num2 = input("Podaj składnik 2: ")


def do_the_math(x, a, b):
    if x == "1":
        logging.debug(f" Dodaję:{num1},{num2}")
        return a + b
    elif x == "2":
        logging.debug(f" Odejmuję:{num1},{num2}")
        return a - b
    elif x == "3":
        logging.debug(f" Mnożę:{num1},{num2}")
        return a * b
    elif x == "4":
        logging.debug(f" Dzielę:{num1},{num2}")
        return a / b
    else:
        print("Niewłaściwy wybór!")


print(f"Wynik to: {do_the_math(choice, num1, num2)}")
