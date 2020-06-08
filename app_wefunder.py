import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import sys
import time

__author__ = "Alfian A"

try:
    """
    Web scraping for https://wefunder.com/explore
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

        print("hallo")
        driver = webdriver.Chrome('/usr/bin/chromedriver')

        driver.delete_all_cookies()
        driver.implicitly_wait(15)
        driver.maximize_window()
        url = 'https://wefunder.com/explore'
        driver.get(url)
        driver.refresh()

        count = 0
        #while True:
        while count < 3:
            try:
                loadMoreButton = driver.find_element_by_xpath('//button[text()="load more"]')
                time.sleep(2)
                loadMoreButton.click()
                time.sleep(5)
                count += 1
            except Exception as e:
                print(e)
                break
        print("Complete Button more")
        time.sleep(10)

        wfdr=driver.find_elements_by_xpath("//div[contains(@class, 'card effect__click')]/a");

        for i in wfdr:
            row_datas = {}
            project_url = i.get_attribute('href')
            wefunder_datas = requests.get(project_url)
            wefunder_data = BeautifulSoup(wefunder_datas.text, 'html.parser')
            project_div = wefunder_data.find('div', 'left-col-h')
            project_name = ''
            project_description = ''
            project_domain_url = ''
            if not project_div:
                project_name = 'No Project Name'
                project_description = 'No Description'
                project_domain_url = 'No Website'
            else:
                project_description = project_div.find('h4').text

                project_domain_url = wefunder_data.find('a', 'wf-standalone-muted')
                if not project_domain_url:
                    project_domain_url = 'No Website'
                else:
                    project_domain_url = project_domain_url['href']

                project_name = project_div.find('h2')
                if project_name.text.find("in") != -1:
                    project_name_tmp = project_name.text.split("in")
                    if len(project_name_tmp) > 0:
                        project_name = project_name_tmp[1].strip()
                    else:
                        project_name = project_name_tmp[0].strip()
                else:
                    project_name = project_name.text


            row_datas = {
                "Project URL": project_url,
                "Project Name": project_name,
                "Project Description": project_description.strip(),
                "Project Domain URL": project_domain_url,
            }

            dict_datas.append(row_datas)
            sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
            sys.stdout.flush()

        df = pd.DataFrame(dict_datas)
        df.to_excel('wefunder_datas.xlsx', index=False)

        driver.quit()

    print('\nEnd Process')

except Exception as ex:
    print(ex)