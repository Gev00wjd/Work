import pandas as pd
import requests
import json
import  math

def print_hi(url = "https://file.notion.so/f/s/0f8850ad-e46f-4f37-99ea-0e4e2a6af5b6/trial_task.json?id=2583a04b-4256-4c1f-939e-6eac0f749ceb&table=block&spaceId=41165294-a784-489a-a401-1a916d020564&expirationTimestamp=1690128000000&signature=IdaxCGDPdE2P3r7fO3xrBUANskv5Q_yCRywVXrT--g0&downloadName=trial_task.json"):
    summary_data = {}


    table = {}
    r = requests.get(url)
    data = r.json()
    for item in data:
        products = item['products']
        highway_cost = int(math.fabs(item.get('highway_cost')))
        count = sum(i['quantity'] for i in products)

        for i in products:
            p_name = i.get('product')

            quantity = i.get('quantity')
            income = i.get('price') * quantity
            expenses = int(math.fabs(highway_cost / count)) * quantity

            profit = income - expenses
            # If the warehouse already exists in the dictionary, add values to existing data

            if p_name in summary_data:
                summary_data[p_name]['quantity'] += quantity
                summary_data[p_name]['profit'] += profit
            else:
                # If the warehouse doesn't exist in the dictionary, create a new entry for it
                summary_data[p_name] = {'p_name': p_name ,'quantity': quantity, 'profit': profit}
    # print(summary_data)
    for item in data:

        w_name = item.get('warehouse_name').strip()
        order_id = item.get('order_id')
        products = item.get('products')
        highway_cost = int(math.fabs(item.get('highway_cost')))
        count = 0;
        order_profit = 0
        for i in products:
            count += i.get('quantity')
            order_profit += i.get('price') * i.get('quantity')
        order_profit -= highway_cost
        for i in products:
            p_name = i.get('product')
            quantity = i.get('quantity')
            income = i.get('price') * quantity
            expenses = int(math.fabs(highway_cost / count)) * quantity

            profit = income - expenses
            percent_profit_product_of_warehouse = (profit / summary_data[p_name]['profit']) * 100

            table[order_id] = { 'product' : p_name,'quantity' : quantity,'income' : income,'expenses' : expenses, 'profit': profit, 'order_profit' : order_profit, 'percent_profit_product_of_warehouse' : percent_profit_product_of_warehouse}
    sorted_products = sorted(table.items(), key=lambda x: x[1]['percent_profit_product_of_warehouse'], reverse=True)
    accumulated_percent = 0
    for product, product_data in sorted_products:
        if(accumulated_percent > 100):
            accumulated_percent = 0
        percent_profit = product_data['percent_profit_product_of_warehouse']
        accumulated_percent += percent_profit
        product_data['accumulated_percent_profit_product_of_warehouse'] = accumulated_percent
        print(accumulated_percent)
    tableFinal = []
    for product, product_data in sorted_products:
        product = product_data['product']
        quantity = product_data['quantity']
        profit = product_data['profit']
        percent_profit = product_data['percent_profit_product_of_warehouse']
        accumulated_percent = product_data['accumulated_percent_profit_product_of_warehouse']
        category = ''
        if (accumulated_percent < 70):
            category = 'A'
        elif (accumulated_percent <90 and accumulated_percent > 70):
            category = 'B'
        else:
            category = 'C'
        tableFinal.append(( product, quantity, profit, percent_profit, accumulated_percent, category))

    df = pd.DataFrame(tableFinal, columns=['product', 'quantity', 'profit', 'percent_profit_product_of_warehouse', 'accumulated_percent_profit_product_of_warehouse', 'category'])

    print(df.to_string())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()

