''' Воскресенская солянка '''
from bs4 import BeautifulSoup
import requests

url = 'http://salavatmk.ru/raspisanie.php'
post = []

page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")


def pars(message_user):
    if page.status_code == 200: #проверка соединения с сайтом
        for a in soup.find_all('a', href=True):
            if '.pdf' in a['href'] and message_user == 'проверить':
                post.append(f"http://salavatmk.ru{a['href']}")
        
        if len(post) == 0:
            return f"На сайте еще нет расписания"
        else:
            return post[-1]
    else:#ошибка если дисконнект
        return f"Ошибка соединения с сайтом"



