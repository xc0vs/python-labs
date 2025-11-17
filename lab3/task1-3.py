import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt 


start_date = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
url = f'https://bank.gov.ua/NBU_Exchange/exchange_site?start={start_date}&valcode=usd&json'

r = requests.get(url)
data = r.json()

date = []
currency = []

for item in data:
    date.append(item['exchangedate'])
    currency.append(item['rate'])
    

plt.plot(date, currency, marker='o', linestyle='-')

plt.title('Зміна курсу долара США за останні 7 днів')
plt.xlabel('Дата')
plt.ylabel('Курс (грн)')
plt.grid(True)
plt.show()
