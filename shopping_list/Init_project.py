print("Lista zakupów")
shops = {"piekarnia": ["chleb", "bułki", "pączek"], "warzywniak": ["marchew", "rukola", "seler"]}
number_of_items = 0
for shop in shops:
    capital_values = []
    for i, item in enumerate(shops.get(shop)):
        capital_values.append(item.capitalize())
        number_of_items += 1

    print(f'Idę do {shop.capitalize()}, kupuję tu następujące rzeczy:{capital_values}')
print(f"W sumie kupuję {number_of_items} produktów")
