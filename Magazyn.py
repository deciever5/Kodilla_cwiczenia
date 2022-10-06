items = {"milk": [100, "l", 2.5], "coffee": [50, "kg", 10], "tea": [30, "kg", 5], "pepsi": [200, "l", 6],
         "wine": [10, "l", 30], "beer": [200, "l", 3]}


def getitems():
    print("Name\tQuantity\tUnit\tUnit Price (PLN)")
    print("----\t--------\t----\t----------------")
    for key, value in items.items():
        print(f"{key:8}{repr(value[0]).ljust(12)}{value[1].ljust(8)}{repr(value[2]).ljust(16)}")


def add_item():
    name = input("Item name: ")
    unit_name = input("Item units of measure :")
    quantity = input("Item quantity: ")
    unit_price = input("Unit price in PLN: ")
    items[name] = [int(quantity), unit_name, int(unit_price)]


while True:
    user_operation = input("What would you like to do? ")
    if user_operation == "exit":
        exit()
    elif user_operation == "show":
        getitems()
    elif user_operation == "add":
        add_item()
