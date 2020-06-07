import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

__author__ = "Alfian A"

try:
    """
    Web scraping for https://www.kisskissbankbank.com/fr/discover?categories[social]=on&categories[web-and-tech]=on&categories[education]=on&categories[film-and-video]=on&categories[ecology]=on&categories[agriculture]=on&categories[food]=on&filter=all 
    """

    dict_datas = []
    end_val = 1
    print('Start Process')
    for page in range(0, end_val):

        page_number = page + 1
        bar_length = 20
        percent = float(page_number) / end_val
        hashes = '#' * int(round(percent * bar_length))
        spaces = ' ' * (bar_length - len(hashes))

        html_datas = requests.get('https://www.kisskissbankbank.com/fr/discover?categories[social]=on&categories[web-and-tech]=on&categories[education]=on&categories[film-and-video]=on&categories[ecology]=on&categories[agriculture]=on&categories[food]=on&filter=all')
        if html_datas.status_code == 200:
            soup = BeautifulSoup(html_datas.text, 'html.parser')
            soup_datas = soup.find_all(attrs={'class': 'k-LegoGrid__item__content'})
            for soup_data in soup_datas:
                kissbank_web = soup_data.find('a')['href']
                category = soup_data.find('p', 'k-u-color-font1 k-u-size-micro k-u-weight-regular k-CrowdfundingCard__subtitle__subtitleText k-u-margin-none k-CrowdfundingCard__subtitle__subtitleText--truncated')
                project_url = kissbank_web
                kissbank_datas = requests.get(project_url)
                kissbank_data = BeautifulSoup(kissbank_datas.text, 'html.parser')
                name_of_project = kissbank_data.find('h1', 'title__StyledTitle-sc-46lshq-0 jqndyC titles__StyledTitle-sc-1v04wsx-0 gwAQhx k-u-align-center')
                facebook_page_URL = kissbank_data.find('a', 'k-u-color-font1 k-u-size-tiny k-u-weight-regular social__StyledSocialLink-sc-1ucfrap-2 diRnbK')
                if not facebook_page_URL:
                    facebook_page_URL = 'No Facebook'
                else:
                    facebook_page_URL = facebook_page_URL['href']

                domain_name_URL = kissbank_data.find('a', 'k-u-color-primary1 k-u-weight-regular')
                if not domain_name_URL:
                    domain_name_URL = 'No Domain'
                else:
                    domain_name_URL = domain_name_URL['href']

                row_datas = {
                    "Name Of Project": name_of_project.text,
                    "Project URL": project_url,
                    "Category": category.text,
                    "Domain Name URL": domain_name_URL,
                    "Facebook Name URL": facebook_page_URL,
                }
                dict_datas.append(row_datas)
                sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
                sys.stdout.flush()

            df = pd.DataFrame(dict_datas)
            df.to_excel('kissbank_datas.xlsx', index=False)
        else:
            print('404 - Not Found ')

    print('\nEnd Process')

except Exception as ex:
    print(ex)