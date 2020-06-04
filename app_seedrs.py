import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

__author__ = "Alfian A"

try:
    """
    Web scraping for https://www.usine-digitale.fr/
    """

    dict_datas = []
    end_val = 270
    print('Start Process')
    for page in range(41, end_val):

        page_number = page + 1
        bar_length = 20
        percent = float(page_number) / end_val
        hashes = '#' * int(round(percent * bar_length))
        spaces = ' ' * (bar_length - len(hashes))

        urlcheck = 'https://www.usine-digitale.fr/annuaire-start-up/' + str(page_number) + '/'
        html_datas = requests.get('https://www.usine-digitale.fr/annuaire-start-up/' + str(page_number) + '/')
        if html_datas.status_code == 200:
            soup = BeautifulSoup(html_datas.text, 'html.parser')
            soup_datas = soup.find('div', 'contenuPage').find_all(attrs={'class': 'blocType1'})  # loop

            for soup_data in soup_datas:
                row_datas = {}
                startup_web = soup_data.find('a', 'contenu')['href']

                urltmp = 'https://www.usine-digitale.fr' + startup_web
                startup_datas = requests.get(urltmp)
                startup_data = BeautifulSoup(startup_datas.text, 'html.parser')
                name = startup_data.find('h1', 'titreFicheStartUp')
                description = startup_data.find('div', {'itemprop': 'description'})
                product = startup_data.find('div', {'itemprop': 'makesOffer'})
                if not product:
                    product = 'No Creators'
                else:
                    product = product.text.strip()
                creators = startup_data.find('div', {'itemprop': 'founders'})
                if not creators:
                    creators = 'No Creators'
                else:
                    creators = creators.text.strip()

                domains = startup_data.find('div', 'deco').find('a', {'itemprop': 'url'})
                if not domains:
                    domains = 'No Phone'
                else:
                    domains = domains.text

                email = startup_data.find('div', 'deco').find('p', {'itemprop': 'email'})
                if not email:
                    email = 'No Phone'
                else:
                    email = email.text

                phone = startup_data.find('div', 'deco').find('p', {'itemprop': 'telephone'})
                if not phone:
                    phone = 'No Phone'
                else:
                    phone = phone.text
                category = startup_data.find('p', 'titreAgConsMark')
                if not category:
                    category = 'No Phone'
                else:
                    category = category.text.replace(':', '')
                url = urltmp

                row_datas = {
                    "Name": name.text,
                    "Description": description.text.strip(),
                    "Product": product,
                    "Creators": creators,
                    "Domain": domains,
                    "Email": email,
                    "Phone": phone,
                    "Category": category,
                    "Url": url,
                }
                dict_datas.append(row_datas)
                sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
                sys.stdout.flush()

            df = pd.DataFrame(dict_datas)
            df.to_excel('startup_datas.xlsx', index=False)
        else:
            print('404 - Not Found ')

    print('\nEnd Process')

except Exception as ex:
    print(ex)