import pandas as pd
import requests
import json
import  math

def print_hi(url = "https://file.notion.so/f/s/0f8850ad-e46f-4f37-99ea-0e4e2a6af5b6/trial_task.json?id=2583a04b-4256-4c1f-939e-6eac0f749ceb&table=block&spaceId=41165294-a784-489a-a401-1a916d020564&expirationTimestamp=1690128000000&signature=IdaxCGDPdE2P3r7fO3xrBUANskv5Q_yCRywVXrT--g0&downloadName=trial_task.json"):
    summary_data = {}
    r = requests.get(url)
    data = r.json()
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

            summary_data[order_id] = { 'product' : p_name,'quantity' : quantity,'income' : income,'expenses' : expenses, 'profit': profit, 'order_profit' : order_profit}
    df = pd.DataFrame(summary_data)


    print(df.to_string())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()

