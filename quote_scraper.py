import requests
from bs4 import BeautifulSoup
import time

page_num = 1
with open('quotes.txt', 'w') as file:
    for i in range(10): # runs 10 times a.k.a gets 10 pages worth of quotes (~300 quotes (2 skipped cuz of exception))
        url = "https://www.goodreads.com/quotes?page=" + str(page_num)
        r = requests.get(url).text
        soup = BeautifulSoup(r, "lxml")

        for quote in soup.find_all('div', class_='quote'):
            quote_text = quote.find('div', class_='quoteText').text
            n = quote_text.lstrip()
            list = n.split('\n')
            final = list[0] + list[3] + '\n'
            try:
                file.write(final)
            except Exception as e:
                print(e)

        page_num += 1