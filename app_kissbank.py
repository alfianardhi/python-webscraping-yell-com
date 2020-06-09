import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import sys
import time

__author__ = "Alfian A"

try:
    """
    Web scraping for https://www.kisskissbankbank.com/fr/discover?categories[social]=on&categories[web-and-tech]=on&categories[education]=on&categories[film-and-video]=on&categories[ecology]=on&categories[agriculture]=on&categories[food]=on&filter=all 
    """

    driver = webdriver.Chrome('/usr/bin/chromedriver')

    driver.delete_all_cookies()
    driver.implicitly_wait(15)
    driver.maximize_window()
    url = 'https://www.kisskissbankbank.com/fr/discover?categories[social]=on&categories[web-and-tech]=on&categories[education]=on&categories[film-and-video]=on&categories[ecology]=on&categories[agriculture]=on&categories[food]=on&page=101'
    driver.get(url)
    driver.refresh()

    dict_datas = []
    end_val = 100
    print('Start Process')
    count = 0
    # while True:
    while count < end_val:

        page_number = count + 1
        bar_length = 20
        percent = float(page_number) / end_val
        hashes = '#' * int(round(percent * bar_length))
        spaces = ' ' * (bar_length - len(hashes))

        try:
            clickNextButton = driver.find_element_by_xpath("//li[@class='Pagination__ListItem__Arrow Pagination__ListItem__Arrow--direction-right']//a[@class='Pagination__Link'][@aria-disabled='false']")
            time.sleep(2)

            kbdatas=driver.find_elements_by_xpath("//div[contains(@class, 'k-LegoGrid__item__content')]/a")
            categorydatas = driver.find_elements_by_xpath("//p[contains(@class, 'k-u-color-font1 k-u-size-micro k-u-weight-regular k-CrowdfundingCard__subtitle__subtitleText k-u-margin-none k-CrowdfundingCard__subtitle__subtitleText--truncated')]/span")
            for kbdata, categorydata in zip(kbdatas, categorydatas):
                row_datas = {}
                project_url = kbdata.get_attribute('href')

                category = categorydata.text

                kissbank_datas = requests.get(project_url)
                time.sleep(3)
                kissbank_data = BeautifulSoup(kissbank_datas.text, 'html.parser')

                name_of_project = kissbank_data.find('h1','title__StyledTitle-sc-46lshq-0 jqndyC titles__StyledTitle-sc-1v04wsx-0 gwAQhx k-u-align-center')
                if not name_of_project:
                    name_of_project = 'No Project name'
                else:
                    name_of_project = name_of_project.text

                facebook_page_URL = kissbank_data.find('a','k-u-color-font1 k-u-size-tiny k-u-weight-regular social__StyledSocialLink-sc-1ucfrap-2 diRnbK')
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
                    "Name Of Project": name_of_project,
                    "Project URL": project_url,
                    "Category": category,
                    "Domain Name URL": domain_name_URL,
                    "Facebook Name URL": facebook_page_URL,
                }
                dict_datas.append(row_datas)
                sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
                sys.stdout.flush()


            df = pd.DataFrame(dict_datas)
            df.to_excel('kissbank2_datas.xlsx', index=False)

            clickNextButton.click()
            time.sleep(5)
            count += 1

        except Exception as e:
            print(e)
            break

    print("Complete Next Button")
    time.sleep(10)

    driver.quit()

    print('\nEnd Process')

except Exception as ex:
    print(ex)