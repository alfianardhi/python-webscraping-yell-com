import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import sys
import time

__author__ = "Alfian A"

try:
    """
    Web scraping for https://fr.ulule.com/discover/?categories=other
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

        driver = webdriver.Chrome('/usr/bin/chromedriver')

        driver.delete_all_cookies()
        driver.implicitly_wait(15)
        driver.maximize_window()
        url = 'https://fr.ulule.com/discover/?categories=other'
        driver.get(url)
        driver.refresh()

        count = 0
        while True:
            try:
                loadMoreButton = driver.find_element_by_xpath('//span[text()="Plus de projets"]')
                time.sleep(2)
                loadMoreButton.click()
                time.sleep(5)
            except Exception as e:
                print(e)
                break
        print("Complete Button more")
        time.sleep(10)

        ids = driver.find_elements_by_css_selector("a.sc-fzomME")

        for i in ids:
            row_datas = {}
            project_url = i.get_attribute('href')

            ulule_datas = requests.get(project_url)
            ulule_data = BeautifulSoup(ulule_datas.text, 'html.parser')
            project_name = ulule_data.find('header', 'title')
            project_name = project_name.find('h1')

            creators = ulule_data.find('a', 'profile-link')
            creator_name = creators.find('h3')
            creator_profile_URL = creators['href']

            potential_email = 'No Email'

            category = ulule_data.find('ul', 'tags')
            category = category.find('a')
            if not category:
                category = 'No Category'
            else:
                category = category.text.strip()

            url = creator_profile_URL

            driver2 = webdriver.Chrome('/usr/bin/chromedriver')
            driver2.delete_all_cookies()
            driver2.implicitly_wait(15)
            driver2.maximize_window()
            driver2.get(url)
            driver2.refresh()

            media_teams = driver2.find_elements_by_css_selector("a.b-user__social--link")
            social_media = ''
            for media_team in media_teams:
                social_media += media_team.get_attribute('href') + '\n'

            if not social_media:
                social_media = 'No Social Media'
            else:
                social_media = social_media

            driver2.quit()

            row_datas = {
                "Project URL": project_url,
                "Project Name": project_name.text,
                "Creator Name": creator_name.text,
                "Creator Profile URL": creator_profile_URL,
                "Potential Email": potential_email,
                "Category Name": category,
                "Social Media": social_media,
            }

            dict_datas.append(row_datas)
            sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
            sys.stdout.flush()

        df = pd.DataFrame(dict_datas)
        df.to_excel('ulule_datas.xlsx', index=False)

        driver.quit()

    print('\nEnd Process')

except Exception as ex:
    print(ex)