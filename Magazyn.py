import copy
import csv
import sys
import tkinter
from tkinter import *

goods = {"milk": [100.5, "l", 2.5], "coffee": [50, "kg", 10], "tea": [30, "kg", 5], "pepsi": [200, "l", 6],
         "wine": [10, "l", 30], "beer": [200, "l", 3]}

sold_goods = copy.deepcopy(goods)
for k, v in sold_goods.items(): v[0] = 0


def export_csv():
    headers = ["Name", "Quantity", "Unit", "Unit Price (PLN)"]
    with open("goods.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows([key, *value] for key, value in goods.items())
    export_sales_to_csv()


def export_sales_to_csv():
    headers = ["Name", "Quantity", "Unit", "Unit Price (PLN)"]
    with open("sold_goods.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows([key, *value] for key, value in sold_goods.items())


def load_items_from_csv():
    with open(sys.argv[1], newline="") as csvfile:
        for _, value in goods.items(): value.clear()
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            goods[row[0]] = [float(row[1]), row[2], float(row[3])]
    with open(sys.argv[2], newline="") as csvfile:
        for _, value in sold_goods.items(): value.clear()
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            sold_goods[row[0]] = [float(row[1]), row[2], float(row[3])]

    print(f"Successfully loaded data from {sys.argv[1]} and {sys.argv[2]}")


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
    load_items_from_csv()


class App:
    def __init__(self, master):
        fm1 = Frame(master)
        fm2 = Frame(master)
        fm3 = Frame(master)
        exiting = tkinter.Button(fm3, text="Exit", command=exit)
        exiting.pack(side="right")
        show = tkinter.Button(fm2, text="Show warehouse", command=get_items)
        show.pack(side="top")
        add = tkinter.Button(fm1, text="Add item", command=add_item)
        add.pack(side="left")
        sell = tkinter.Button(fm1, text="Sell item", command=sell_item)
        sell.pack(side="left")
        cost = tkinter.Button(fm2, text="Warehouse value", command=get_costs)
        cost.pack(side="top")
        revenue = tkinter.Button(fm2, text="Revenue value", command=show_revenue)
        revenue.pack(side="top")
        save = tkinter.Button(fm3, text="Save warehouse", command=export_csv)
        save.pack(side="right")
        fm1.pack(side=LEFT, fill=BOTH, expand=YES)
        fm2.pack(side=LEFT, padx=10)
        fm3.pack(side=RIGHT, padx=10)


window = tkinter.Tk()
window.title("Storage managment")
display = App(window)
window.mainloop()

"""
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
    elif user_operation == "cost":
        get_costs()
    elif user_operation == "revenue":
        show_revenue()
    elif user_operation == "save":
        export_csv()
        export_sales_to_csv()

    else:
        print("No such operation.")"""
