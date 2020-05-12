import requests
from bs4 import BeautifulSoup
import pandas as pd

try:
    dict_datas = []
    print('====================== check1 ========================')
    for page in range(0,3):
        page_number = page + 1
        print('====================== check2 ========================')
        urlcheck = 'https://www.usine-digitale.fr/annuaire-start-up/'+str(page_number)+'/'
        html_datas = requests.get('https://www.usine-digitale.fr/annuaire-start-up/'+str(page_number)+'/')

        print(urlcheck)
        print('====================== STARTS ========================')
        print('====================== LOADING ========================')
        if html_datas.status_code == 200:
            soup = BeautifulSoup(html_datas.text, 'html.parser')
            soup_datas = soup.find('div','contenuPage').find_all(attrs={'class': 'blocType1'}) #loop

            for soup_data in soup_datas:
                row_datas = {}
                startup_web = soup_data.find('a','contenu')['href']

                urltmp = 'https://www.usine-digitale.fr'+startup_web
                startup_datas = requests.get(urltmp)
                startup_data = BeautifulSoup(startup_datas.text, 'html.parser')
                name = startup_data.find('h1', 'titreFicheStartUp')
                description = startup_data.find('div', {'itemprop': 'description'})
                product = startup_data.find('div', {'itemprop': 'makesOffer'})
                creators = startup_data.find('div', {'itemprop': 'founders'})
                domains = startup_data.find('div','deco').find('a', {'itemprop': 'url'})
                if not domains:
                    domains = 'No Phone'
                else:
                    domains = domains.text

                email = startup_data.find('div','deco').find('p', {'itemprop': 'email'})
                if not email:
                    email = 'No Phone'
                else:
                    email = email.text

                phone = startup_data.find('div','deco').find('p', {'itemprop': 'telephone'})
                if not phone:
                    phone = 'No Phone'
                else:
                    phone = phone.text
                category = startup_data.find('p','titreAgConsMark')
                url = urltmp

                row_datas = {
                    "Name": name.text,
                    "Description": description.text.strip(),
                    "Product": product.text,
                    "Creators": creators.text,
                    "Domains": domains,
                    "Email": email,
                    "Phone": phone,
                    "Category":category.text.replace(':',''),
                    "Url": url,
                }
                #print(row_datas)
                dict_datas.append(row_datas)

            df = pd.DataFrame(dict_datas)
            df.to_excel('startup_data.xlsx', index=False)
        else:
            print('404 - Not Found ')

        print('====================== FINISH ========================')

except Exception as ex:
    print(ex)