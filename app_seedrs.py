import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

__author__ = "Alfian A"

try:
    """
    Web scraping for https://www.seedrs.com/investment-opportunities?current_page=2&last_page=2&sectors[]=energy&sectors[]=healthcare&sectors[]=finance-and-payments&sectors[]=saas-paas&sectors[]=automotive-and-transport&sort=trending_desc 
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

        html_datas = requests.get('https://www.seedrs.com/investment-opportunities?current_page=2&last_page=2&sectors[]=energy&sectors[]=healthcare&sectors[]=finance-and-payments&sectors[]=saas-paas&sectors[]=automotive-and-transport&sort=trending_desc')
        if html_datas.status_code == 200:
            soup = BeautifulSoup(html_datas.text, 'html.parser')
            soup_datas = soup.find_all(attrs={'class': 'sc-AxhUy gcWpmH'})
            for soup_data in soup_datas:
                seedrs_web = soup_data.find('a')['href']
                profile_url = 'https://www.seedrs.com' + seedrs_web
                seedrs_datas = requests.get(profile_url)
                seedrs_data = BeautifulSoup(seedrs_datas.text, 'html.parser')
                project_name = seedrs_data.find('h1', {'itemprop': 'name'})
                project_description = seedrs_data.find('p', 'summary')
                project_description = project_description.find('b')
                project_domain_url = seedrs_data.find('a', 'website')['href']
                project_category = seedrs_data.find('span', 'CategoryLabel')

                row_datas = {
                    "Profile URL": profile_url,
                    "Project Name": project_name.text,
                    "Project Description": project_description.text.strip(),
                    "Project Domain URL": project_domain_url,
                    "Project Category": project_category.text,
                }
                dict_datas.append(row_datas)
                sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
                sys.stdout.flush()

            df = pd.DataFrame(dict_datas)
            df.to_excel('seedrs_datas.xlsx', index=False)
        else:
            print('404 - Not Found ')

    print('\nEnd Process')

except Exception as ex:
    print(ex)