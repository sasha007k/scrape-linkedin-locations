import pandas as pd
import re
import itertools
from openpyxl import Workbook
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
from IPython.core.display import clear_output
from random import randint
from requests import get
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from time import sleep
from time import time
import csv

data = pd.read_csv(r"C:\Users\HP\Desktop\Company Cards - Sheet7.csv") 
mylist = data['url'].tolist()

option = webdriver.ChromeOptions()
option.add_argument('headless')
#driver = webdriver.Chrome(ChromeDriverManager(version="102.0.5005.115").install(), options=option)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
driver.find_element_by_xpath('//*[@id="username"]').send_keys("sashakryklyvets@gmail.com")
driver.find_element_by_xpath('//*[@id="password"]').send_keys("260600ks")
driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button').click()


def write_to_file(url, website, industry, founding_date, number_of_employees, headquarter):
	with open(r'C:\Users\HP\Desktop\location-2.csv', 'a', encoding='utf-8') as file:
			file.write("%s*%s*%s*%s*%s*%s\n"%(url,website,industry,founding_date,number_of_employees,headquarter))

def find_value_by_field_name(list_values, field_name):
    for index, value in enumerate(list_values):
        if value == field_name:
            return list_values[index+1]
    return ""

with open(r'C:\Users\HP\Desktop\location-2.csv', 'w', encoding='utf-8') as file:
		file.write("Url*Website*Industry*Founding Date*Number of Employees*Headquarter\n")

n = len(mylist)
for i in range(0, len(mylist)):
    url = mylist[i]
    if not url.endswith('about') and not url.endswith('about/'):
        if url.endswith('/'):
            url += 'about'
        else:
            url += '/about'
    driver.get(url)
    sleep(1)  

    website = ''
    industry = ''
    founding_date = ''
    number_of_employees = ''
    headquater = ''

    try:
        soup = BeautifulSoup(driver.page_source, 'lxml')
    except:
        write_to_file(url, website, industry, founding_date, number_of_employees, headquater)
        continue
     
    try:
         overview_section = soup.find('section', 'artdeco-card p5 mb4')
         overview_description_list = soup.find('dl', 'overflow-hidden')

         overview_description_text = overview_description_list.text.replace("\n", "").strip()
         list_with_values = overview_description_text.split("  ")
         list_with_values = list(filter(None, list_with_values))

         website = find_value_by_field_name(list_with_values, "Website")
         industry = find_value_by_field_name(list_with_values, "Industry")
         founding_date = find_value_by_field_name(list_with_values, "Founded")
         number_of_employees = find_value_by_field_name(list_with_values, "Company size")
         headquater = find_value_by_field_name(list_with_values, "Headquarters")
         
         write_to_file(url, website, industry, founding_date, number_of_employees, headquater)
         print("{0} / {1}".format(i, n))

    except:
        write_to_file(url, website, industry, founding_date, number_of_employees, headquater)

print('end')

