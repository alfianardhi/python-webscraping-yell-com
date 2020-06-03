import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

__author__ = "Alfian A"

try:
    """
    Web scraping for https://www.crowdfunder.com/?q=filter&industry=3,7,19,8,18,13,17,1,2
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

        html_datas = requests.get('https://www.crowdfunder.com', params={'q': 'filter', 'industry': '3,7,19,8,18,13,17,1,2'})

        if html_datas.status_code == 200:
            soup = BeautifulSoup(html_datas.text, 'html.parser')
            soup_datas = soup.find_all(attrs={'class': 'card deal-card'})
            dict_datas = []
            for soup_data in soup_datas:
                row_datas = {}
                crowdfunder_web = soup_data.find('a', 'deal-card-link card-link')['href']
                profile_url = 'https://www.crowdfunder.com' + crowdfunder_web
                # print(profile_url)
                crowdfunder_datas = requests.get(profile_url)
                crowdfunder_data = BeautifulSoup(crowdfunder_datas.text, 'html.parser')
                project_name = crowdfunder_data.find('div', 'company-name').find('h1')
                # print(project_name.text)
                project_description = crowdfunder_data.find('div', 'company-name').find('p')
                # print(project_description.text)
                project_domain_url = crowdfunder_data.find('a', 'company-link-url')
                if not project_domain_url:
                    project_domain_url = "No Website"
                else:
                    project_domain_url = project_domain_url['href']

                # print(project_domain_url)

                row_datas = {
                    "Profile URL": profile_url,
                    "Project Name": project_name.text,
                    "Project Description": project_description.text,
                    "Project Domain URL": project_domain_url,
                }
                dict_datas.append(row_datas)
                sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
                sys.stdout.flush()

            df = pd.DataFrame(dict_datas)
            df.to_excel('crowdfunder_datas.xlsx', index=False)
        else:
            print('404 - Not Found ')

    print('\nEnd Process')

except Exception as ex:
    print(ex)