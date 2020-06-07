import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

__author__ = "Alfian A"

try:
    """
    Web scraping for https://www.seedinvest.com/offerings 
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

        html_datas = requests.get('https://www.seedinvest.com/offerings')
        if html_datas.status_code == 200:
            print(html_datas.status_code)
            soup = BeautifulSoup(html_datas.text, 'html.parser')
            soup_datas = soup.find_all(attrs={'class': 'thumbnail-content'})
            for soup_data in soup_datas:
                project_name = soup_data.find('h5', 'thumbnail-title')

                if project_name.text != 'Private':
                    seedinvest_web = project_name.find('a')
                    if not seedinvest_web:
                        continue
                    else:
                        seedinvest_web = seedinvest_web['href']
                        if seedinvest_web != '/case-studies':

                            project_url = 'https://www.seedinvest.com' + seedinvest_web
                            seedinvest_datas = requests.get(project_url)
                            seedinvest_data = BeautifulSoup(seedinvest_datas.text, 'html.parser')

                            project_desc = seedinvest_data.find('p', 'plain-subtitle xs')

                            project_domain_URL = seedinvest_data.find('div', 'snippet left collapse-margin-bottom min-height-6')
                            if not project_domain_URL:
                                project_domain_URL = 'No Website'
                            else:
                                project_domain_URL_Tmp=project_domain_URL.text.split(': ')
                                project_domain_URL=project_domain_URL_Tmp[1].strip()

                            row_datas = {
                                "Profile URL": project_url,
                                "Project Name": project_name.text,
                                "Project Description": project_desc.text,
                                "Project Domain URL": project_domain_URL,
                            }
                            dict_datas.append(row_datas)

                        else:
                            continue
                else:
                    continue

                sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
                sys.stdout.flush()

            df = pd.DataFrame(dict_datas)
            df.to_excel('seedinvest_datas.xlsx', index=False)
        else:
            print('404 - Not Found ')

    print('\nEnd Process')

except Exception as ex:
    print(ex)