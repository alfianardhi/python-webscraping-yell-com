import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

__author__ = "Alfian A"

try:
    """
    Web scraping for https://www.amazon.fr/gp/new-releases/books/301135/ref=zg_bsnr_pg_1?ie=UTF8&pg=1
    """

    dict_datas = []
    end_val = 3
    print('Start Process')
    for page in range(0, end_val):

        page_number = page + 1
        bar_length = 20
        percent = float(page_number) / end_val
        hashes = '#' * int(round(percent * bar_length))
        spaces = ' ' * (bar_length - len(hashes))

        zg_bsnr_pg = 'zg_bsnr_pg_'+str(page_number)
        html_datas = requests.get('https://www.amazon.fr/gp/new-releases/books/301135/',
                                  params={'ref': zg_bsnr_pg, 'ie': 'UTF8', 'pg': str(page_number)})
        if html_datas.status_code == 200:
            soup = BeautifulSoup(html_datas.text, 'html.parser')
            soup_datas = soup.find_all('li', 'zg-item-immersion')
            for soup_data in soup_datas:
                # row_datas = {}
                startup_web = soup_data.find('a', 'a-link-normal')['href']

                urltmp = 'https://www.amazon.fr/' + startup_web
                book_title = soup_data.find('div', 'a-section a-spacing-small').find('img')['alt']
                author_name = soup_data.find('span', 'a-size-small a-color-base')
                if not author_name:
                    author_name = soup_data.find('a', 'a-size-small a-link-child')
                else:
                    product = author_name

                row_datas = {
                    "Book Title": book_title,
                    "Author Name": author_name.text,
                    "Amazon URL": urltmp,
                }
                dict_datas.append(row_datas)
                sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
                sys.stdout.flush()

            df = pd.DataFrame(dict_datas)
            df.to_excel('amazon_datas.xlsx', index=False)
        else:
            print('404 - Not Found ')

    print('\nEnd Process')

except Exception as ex:
    print(ex)