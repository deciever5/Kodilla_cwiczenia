import copy

goods = {"milk": [100, "l", 2.5], "coffee": [50, "kg", 10], "tea": [30, "kg", 5], "pepsi": [200, "l", 6],
         "wine": [10, "l", 30], "beer": [200, "l", 3]}

sold_goods = copy.deepcopy(goods)
for k, v in sold_goods.items(): v[0] = 0


def getitems():
    print("Name\tQuantity\tUnit\tUnit Price (PLN)")
    print("----\t--------\t----\t----------------")
    for key, value in goods.items():
        print(f"{key:8}{repr(value[0]).ljust(12)}{value[1].ljust(8)}{repr(value[2]).ljust(16)}")


def add_item():
    name = input("Item name: ")
    unit_name = input("Item units of measure :")
    quantity = input("Item quantity: ")
    unit_price = input("Unit price in PLN: ")
    goods[name] = [int(quantity), unit_name, int(unit_price)]


def sell_item():
    sold_item = input("Item sold: ")
    quantity_sold = input("Quantity sold: ")
    goods[sold_item][0] -= int(quantity_sold)
    print(f"Succesfully sold {quantity_sold}{goods[sold_item][1]} of {sold_item}")
    sold_goods[sold_item][0] += int(quantity_sold)
    getitems()

def get_costs():
    pass


while True:
    user_operation = input("What would you like to do? ")
    if user_operation == "exit":
        exit()
    elif user_operation == "show":
        getitems()
    elif user_operation == "add":
        add_item()
    elif user_operation == "sell":
        sell_item()
