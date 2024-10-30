import csv
import os

def add_orders(file_path):
    id = int(input("Enter order ID: "))
    order = input("Enter order type (Buy/Sell): ").capitalize()
    type = str(input("Please enter type (Add/Remove): ")).capitalize()
    price = float(input("Enter price: "))
    quantity = int(input("Enter quantity: "))

    try:
        with open(file_path, "a", newline="") as stock:
            stock.write(f"\n{id},{order},{type},{price},{quantity}")
            print("Order successfully added!")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}") 
        
def remove_orders(file_path, condition_function):
    with open(file_path, 'r') as input_file, open('temp.csv', 'w', newline='') as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)
        for row in reader:
            if not condition_function(row):
                writer.writerow(row)

    os.remove(file_path)
    os.rename('temp.csv', file_path)

def display_best_order(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        best_buy = None
        best_sell = None
        for row in reader:
            try:
                order_type = row[1]
                price = row[3]
                quantity = row[4]
            except ValueError:
                print(f"Skipping invalid row: {row}")
                continue
            if order_type == 'Buy':
                if not best_buy or price > best_buy[1]:
                    best_buy = (row, price)
            elif order_type == 'Sell':
                if not best_sell or price < best_sell[1]:
                    best_sell = (row, price)

        if best_buy:
            print("Best Buy Order:")
            print(f"ID: {best_buy[0][0]}, Price: {best_buy[1]}, Quantity: {best_buy[0][4]}")
        else:
            print("No buy orders found.")

        if best_sell:
            print("Best Sell Order:")
            print(f"ID: {best_sell[0][0]}, Price: {best_sell[1]}, Quantity: {best_sell[0][4]}")
        else:
            print("No sell orders found.")

def main(file_path):
    while True:
        print("1. Add Order")
        print("2. Remove order/s with type 'Remove'")
        print("3. Display buy/sell orders with best price")
        print("0. Exit the program")

        input_choice = int(input("Please enter operation: "))

        if input_choice == 1:
            add_orders(file_path)
        elif input_choice == 2:
            remove_orders(file_path, lambda row: row[2] == "Remove")
        elif input_choice == 3:
            display_best_order(file_path)
        elif input_choice == 0:
            break
        else:
            print("Unknown operation code. Please try again!")

if __name__ == "__main__":
    file_path = os.path.join("data", "stock_exchange.csv")
    print(main(file_path))