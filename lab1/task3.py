""""
Статистика продажів. Створіть список словників, де кожен словник представляє продаж з 
ключами: "продукт", "кількість", "ціна". Напишіть функцію, яка обчислює загальний дохід 
для кожного продукту та повертає словник, де ключі - це назви продуктів, а значення - загальний дохід.
Створіть список продуктів, що принесли дохід більший ніж 1000.
"""

sales = [
    {"product": "pen", "quantity": "13", "price": "40"},
    {"product": "eraser", "quantity": "7", "price": "20"},
    {"product": "notebook", "quantity": "25", "price": "50"},   # 25 * 50 = 1250 (>1000)
    {"product": "marker", "quantity": "10", "price": "60"},
    {"product": "stapler", "quantity": "5", "price": "150"}     # 5 * 150 = 750
]

def calculate_revenues(sales_list):
    product_revenues = {}
    for sale in sales_list:
        product_name = sale["product"]
        quantity = sale["quantity"]
        price = sale["price"]

        product_revenues[product_name] = product_revenues.get(product_name, 0) + int(quantity) * float(price)
    return product_revenues

total_revenues = calculate_revenues(sales)
print("Total revenue for each product: ", total_revenues)

high_income_products = []
for product, revenue in total_revenues.items():
    if revenue > 1000:
        high_income_products.append(product)

print("Products with revenue over 1000: ", high_income_products)



