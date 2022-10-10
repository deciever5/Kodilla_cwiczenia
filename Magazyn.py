import copy
import csv
import sys

goods = {"milk": [100.5, "l", 2.5], "coffee": [50, "kg", 10], "tea": [30, "kg", 5], "pepsi": [200, "l", 6],
         "wine": [10, "l", 30], "beer": [200, "l", 3]}

sold_goods = copy.deepcopy(goods)
for k, v in sold_goods.items(): v[0] = 0


def export_csv(filename, data):
    headers = ["Name", "Quantity", "Unit", "Unit Price (PLN)"]
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows([key, *value] for key, value in data)


def load_items_from_csv(argument):
    with open(argument, newline="") as csvfile:
        for _, value in goods.items(): value.clear()
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            goods[row[0]] = [float(row[1]), row[2], float(row[3])]

    print(f"Successfully loaded data from {sys.argv[1]}")
    print(f"Successfully loaded data from {sys.argv[2]}")


def get_items():
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
    print(f"Successfully sold {quantity_sold}{goods[sold_item][1]} of {sold_item}")
    sold_goods[sold_item][0] += int(quantity_sold)
    get_items()


def get_costs():
    goods_value = sum([x * z for x, _, z in goods.values()])
    return goods_value


def get_income():
    sales_value = sum([x * z for x, _, z in sold_goods.values()])
    return sales_value


def show_revenue():
    print(f"Revenue breakdown (PLN)\nIncome: {get_income():.2f}\nCosts: {get_costs():.2f}\n-----------")
    print(f"Revenue: {(get_income() - get_costs()):.2f}")


if len(sys.argv) > 1:
    load_items_from_csv(sys.argv[1])
    load_items_from_csv(sys.argv[2])



while True:
    user_operation = input("What would you like to do? ")
    if user_operation == "exit":
        exit()
    elif user_operation == "show":
        get_items()
    elif user_operation == "add":
        add_item()
    elif user_operation == "sell":
        sell_item()
    elif user_operation == "revenue":
        show_revenue()
    elif user_operation == "save":
        export_csv("goods.csv", goods.items())
        export_csv("sold_goods.csv", sold_goods.items())

    else:
        print("No such operation.")
