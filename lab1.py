import requests
import pandas as pd
from bs4 import BeautifulSoup


class Data:
    def __init__(self, name, link, category):
        self.name = name
        self.link = link
        self.category = category


def get_html(url):
    source = requests.get(url)
    return source.text


def get_data(html):
    soup = BeautifulSoup(html, "html.parser")
    ads = soup.find('div', class_='list-view').find_all('div', class_='item product_listbox oh')
    name = []
    link = []
    category = []
    for ad in ads:
        name.append(ad.find('strong').text)
        link.append('https://www.kivano.kg' + ad.find('strong').find('a').get('href'))
        category.append(soup.find('div', class_="product-index").find_next('div', class_="portlet-title").find_next('ul', class_="breadcrumb2").find_all_next('li', itemprop="itemListElement")[-1].text)
    data = Data(name, link, category)
    return data


def writer_to_csv(data):
    data_pd = pd.DataFrame(
        {'name': data.name,
         'link': data.link,
         'category': data.category,})
    csv_file = data_pd.to_csv(index=False)
    with open("kivano.csv", "a", encoding='utf-8') as f:
        f.write(csv_file)


def main():
    url1 = 'https://www.kivano.kg/noutbuki-i-kompyutery'
    url2 = 'https://www.kivano.kg/mobilnye-telefony'
    url3 = 'https://www.kivano.kg/melkaya-bytovaya-tekhnika'
    url4 = 'https://www.kivano.kg/tovary-dlya-krasoty'
    lst_url = [url1, url2, url3, url4]
    url_part = '?page='
    for url in lst_url:
        for i in range(1, 4):
            url_final = url + url_part + str(i)
            print(f'Сохраняются данные со страницы {url_final}')
            writer_to_csv(get_data(get_html(url_final)))
    print('Файл сохранен')

main()
