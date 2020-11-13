import os, requests
from bs4 import BeautifulSoup as bs

ARTICLE_URL = 'https://www.economist.com/china/2020/11/14/hong-kongs-legislature-has-been-stripped-of-a-vocal-opposition'

page = requests.get(ARTICLE_URL)
soup = bs(page.content, 'html.parser')

title = soup.find('span', class_='article__headline')
body = soup.find_all('p', class_='article__body-text')

print(title.text)

for p in body:
    #print(p.text)
    #print('\n')
    pass
