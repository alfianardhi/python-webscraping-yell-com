import requests
from bs4 import BeautifulSoup
import pandas as pd

try:
    header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'}
    dict_datas = []
    for page in range(0,3):
        page_number = page + 1
        html_datas = requests.get('https://www.yell.com/ucs/UcsSearchAction.do',
                                  params={'keywords': 'Restaurants', 'location': 'united+kingdom',
                                          'scrambleSeed': '1558621577', 'pageNum': page_number}, headers=header)

        if html_datas.status_code == 200:
            soup = BeautifulSoup(html_datas.text, 'html.parser')

            soup_datas = soup.find(attrs={'class': 'row results--row results--capsuleList'})
            restaurants_datas = soup_datas.find_all(attrs={'class': 'row businessCapsule--mainRow'})

            for restaurants in restaurants_datas:
                row_datas = {}
                restaurant_name = restaurants.find('span', 'businessCapsule--name')
                restaurants_class = restaurants.find('div', 'col-sm-24 businessCapsule--classStrap').find('a','businessCapsule--classification businessCapsule--link')
                restaurant_telp = restaurants.find('span', 'business--telephoneNumber')
                restaurant_web = restaurants.find('div', 'col-sm-24 businessCapsule--ctas').find('a', {
                    'rel': 'nofollow noopener'})
                if not restaurant_web:
                    restaurant_web = 'No Web'
                else:
                    restaurant_web = restaurant_web['href']
                restaurant_str_addrs = restaurants.find('span', {'itemprop': 'streetAddress'})
                restaurant_addrs_local = restaurants.find('span', {'itemprop': 'addressLocality'})
                restaurant_pstl_code = restaurants.find('span', {'itemprop': 'postalCode'})
                restaurant_rating = restaurants.find('span', 'starRating--average')
                if not restaurant_rating:
                    restaurant_rating = 'No Rating'
                else:
                    restaurant_rating = restaurant_rating.text

                row_datas = {
                    "Name": restaurant_name.text,
                    "Classification": restaurants_class.text.strip(),
                    "Telephone": restaurant_telp.text,
                    "Web":restaurant_web,
                    "StreetAddress":restaurant_str_addrs.text,
                    "AddressLocality":restaurant_addrs_local.text,
                    "PostalCode":restaurant_pstl_code.text,
                    "Rating":restaurant_rating,
                }
                dict_datas.append(row_datas)

            #export datas to excel
            df = pd.DataFrame(dict_datas)
            df.to_excel('restaurant_data.xlsx', index=False)
        else:
            print('404 - Not Found ')

except Exception as ex:
    print(ex)