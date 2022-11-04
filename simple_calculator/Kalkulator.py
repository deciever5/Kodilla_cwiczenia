import logging

logging.basicConfig(level=logging.DEBUG)


def do_the_math(x, a, b):
    if x == "1":
        logging.debug(f" Dodaję:{num1},{num2}")
        return a + b
    elif x == "2":
        logging.debug(f" Odejmuję:{num1},{num2}")
        return a - b
    elif x == "3":
        logging.debug(f" Mnożę: {num1} , {num2}")
        return a * b
    elif x == "4":
        logging.debug(f" Dzielę:{num1},{num2}")
        return a / b


while True:
    choice = input(
        "Podaj działanie, posługując się odpowiednią liczbą: 1 Dodawanie, 2 Odejmowanie, 3 Mnożenie, 4 Dzielenie:")
    if choice in ["1", "2", "3", "4"]:
        try:
            num1 = float(input("Podaj składnik 1: "))
            num2 = float(input("Podaj składnik 2: "))
            print(f"Wynik to: {do_the_math(choice, num1, num2)}")
            break
        except ValueError:
            print("Podaj tylko liczby!")

    else:
        print("Nieprawidłowy wybór. Wybierz działanie (1-4)")
