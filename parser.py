''' Воскересенская солянка '''
from bs4 import BeautifulSoup
import requests

url = 'http://salavatmk.ru/raspisanie.php'
post = []
test = []
page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")
news = soup.findAll('div', class_='content-wrapper')

for a in soup.find_all('a', href=True):
    if '.pdf' in a['href']:
        post.append(f"http://salavatmk.ru{a['href']}")
print(post[-1])




