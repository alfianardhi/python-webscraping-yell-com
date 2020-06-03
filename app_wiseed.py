import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

__author__ = "Alfian A"

try:
    """
    Web scraping for https://www.wiseed.com/fr/projets-en-vote
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

        html_datas = requests.get('https://www.wiseed.com/fr/projets-en-vote')
        if html_datas.status_code == 200:
            soup = BeautifulSoup(html_datas.text, 'html.parser')
            soup_datas = soup.find('div', 'list-cards__trail').find_all(attrs={'class': 'col-project-card'})
            for soup_data in soup_datas:
                row_datas = {}
                startup_web = soup_data.find('a', 'link')['href']

                urltmp = 'https://www.wiseed.com' + startup_web
                startup_datas = requests.get(urltmp)
                startup_data = BeautifulSoup(startup_datas.text, 'html.parser')
                project_url = urltmp;
                domain_url = startup_data.find('a', 'btn btn-sm btn-flat btn-primary new-tab')['href']

                founder_name1 = 'No Name'
                founder_name2 = 'No Name'
                founder_name3 = 'No Name'
                founder_linkedlin1 = 'No linkedlin'
                founder_linkedlin2 = 'No linkedlin'
                founder_linkedlin3 = 'No linkedlin'

                count = 0
                media_teams = startup_data.find_all('div', 'media team')
                for media_team in media_teams:
                    count += 1
                    founder_name = media_team.find('h3', 'media-heading h4')
                    if not founder_name:
                        founder_name = 'No Name'
                    else:
                        founder_name = founder_name.text

                    founder_linkedlin = media_team.find('a', 'linkedin-color')
                    if not founder_linkedlin:
                        founder_linkedlin = 'No linkedlin'
                    else:
                        founder_linkedlin = founder_linkedlin['href']

                    if count == 1:
                        founder_name1 = founder_name
                        founder_linkedlin1 = founder_linkedlin
                    elif count == 2:
                        founder_name2 = founder_name
                        founder_linkedlin2 = founder_linkedlin
                    else:
                        founder_name3 = founder_name
                        founder_linkedlin3 = founder_linkedlin

                row_datas = {
                    "Project URL": project_url,
                    "Founder Name 1": founder_name1,
                    "Founder Linkedlin 1": founder_linkedlin1,
                    "Founder Name 2": founder_name2,
                    "Founder Linkedlin 2": founder_linkedlin2,
                    "Founder Name 3": founder_name3,
                    "Founder Linkedlin 3": founder_linkedlin3,
                    "Domain Name URL": domain_url,
                }
                dict_datas.append(row_datas)
                sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
                sys.stdout.flush()

            df = pd.DataFrame(dict_datas)
            df.to_excel('wiseed_datas.xlsx', index=False)
        else:
            print('404 - Not Found ')

    print('\nEnd Process')

except Exception as ex:
    print(ex)