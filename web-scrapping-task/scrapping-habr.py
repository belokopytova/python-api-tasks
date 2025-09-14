import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

KEYWORDS = ['дизайн', 'фото', 'python', 'web']
HEADERS = Headers().generate()
url = 'https://habr.com/ru/articles/top/monthly/'

response = requests.get(url, headers=HEADERS).text
soup = BeautifulSoup(response, 'html.parser')
posts = soup.find_all('article', class_='tm-articles-list__item')

def is_in_hubs(word, list_hub): #фукнция для проверки вхождения ключевого слова в хабы статьи

    flag = False
    for h in list_hub:
        if word in h:
            flag = True
    return flag

def get_text_from_post(link): #функция для получения текста по ссылке на статью

    response = requests.get(link, headers=HEADERS).text
    soup = BeautifulSoup(response, 'html.parser')
    post_ = soup.find('article', class_='tm-article-presenter__content tm-article-presenter__content_narrow')
    return post_.get_text()

def find_keywords_in_article(articles): #функция для анализа текста статьи целиком

    result = []
    count = 0

    for post in articles:

        count+=1
        print(f'Просматривается {count} статья')
        href = post.find('a', class_='tm-title__link').attrs['href']
        link_post = 'https://habr.com' + href
        text_post = get_text_from_post(link_post).split()

        for keyword in KEYWORDS:
            if keyword in text_post:
                date_time = post.find('time').get('title')
                title = post.find('a', class_='tm-title__link').text
                #title = post.find('h1', class_='tm-title tm-title_h1').text
                result.append(f"<{date_time}>-<{title}>-<{link_post}>")
                break

    if result == []:
        return 'ключевые слова не найдены\n'
    else:
        return result

def find_keywords_in_preview(articles): #функция для анализа только preview-информацию статьи

    result = []

    for post in posts:

        list_hubs = []
        hubs = post.find_all(class_='tm-publication-hub__link')

        for hub in hubs:
            list_hubs.append(hub.text)

        for keyword in KEYWORDS:

            if keyword in post.text.split() and is_in_hubs(keyword, list_hubs) == False:

                    date_time = post.find('time').get('title')
                    title = post.find('a', class_='tm-title__link').text
                    href = post.find('a', class_='tm-title__link').attrs['href']
                    link = 'https://habr.com' + href
                    result.append(f"<{date_time}>-<{title}>-<{link}>")
                    break

        list_hubs.clear()

    if result == []:
        return 'статьи не найдены\n'
    else:
        return result

def main():
    print('Список статей, где ключевые слова найдены в preview: ', find_keywords_in_preview(posts))
    print('Список статей, где ключевые слова найдены в целой статье: ', find_keywords_in_article(posts))

if __name__ == '__main__':
    main()


