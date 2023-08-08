import csv
from datetime import datetime


def load_csv(filename):
    data = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data


class Inventory:
    def __init__(self, manufacturer_filename, price_filename, service_date_filename):
        self.inventory = {}
        self.load_inventory(manufacturer_filename, price_filename, service_date_filename)

    def load_inventory(self, manufacturer_filename, price_filename, service_date_filename):
        manufacturer_data = load_csv(manufacturer_filename)
        price_data = load_csv(price_filename)
        service_date_data = load_csv(service_date_filename)

        for item in manufacturer_data:
            item_id, manufacturer, item_type, damaged = item
            self.inventory[item_id] = {
                'manufacturer': manufacturer,
                'item_type': item_type,
                'damaged': damaged
            }

        for item in price_data:
            item_id, price = item
            self.inventory[item_id]['price'] = float(price)

        for item in service_date_data:
            item_id, service_date_str = item
            self.inventory[item_id]['service_date'] = datetime.strptime(service_date_str, '%m/%d/%Y')

    def query_item(self, manufacturer, item_type):
        matching_items = [(item_id, item) for item_id, item in self.inventory.items()
                          if manufacturer.lower() in item['manufacturer'].lower()
                          and item_type.lower() in item['item_type'].lower()
                          and item['service_date'] >= datetime.now()
                          and item['damaged'] != 'damaged']

        return matching_items


def main():
    inventory = Inventory("ManufacturerList.csv", "PriceList.csv", "ServiceDatesList.csv")

    while True:
        query = input("Enter the manufacturer and item type or q to quit: ")
        if query.lower() == 'q':
            break

        query_parts = query.split()

        if len(query_parts) != 2:
            print("Invalid input format. Please enter both the manufacturer and item type.")
            continue

        manufacturer, item_type = query_parts

        items = inventory.query_item(manufacturer, item_type)

        if not items:
            print("No such item in inventory\n")
            continue

        items.sort(key=sort_by_price, reverse=True)
        chosen_item_id, chosen_item = items[0]

        print(f"Your item is: {chosen_item_id}, {chosen_item['manufacturer']}, "
              f"{chosen_item['item_type']}, ${chosen_item['price']}\n")

        similar_items = []
        for item_id, item_type in items[1]:
            if item_type["item_type"] == chosen_item["item_type"]:
                similar_items.append((item_id, item_type))

        if similar_items:
            closest_item_id, closest_item = min(similar_items, key=compare_item_prices(chosen_item['price']))
            print(f"You may also consider: {closest_item_id}, {closest_item['manufacturer']}, "
                  f"{closest_item['item_type']}, ${closest_item['price']}\n")


def sort_by_price(item):
    return item[1]["price"]


def compare_item_prices(reference_price):
    def price_difference(item):
        return abs(item[1]['price'] - reference_price)
    return price_difference


if __name__ == "__main__":
    main()
