
from selenium import webdriver
import time
from seleniumrequests import Chrome
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import re


file_path='reuters/articles'

d = Chrome()


number_of_articles=20

illegal_chars_pattern = r'[<>:"/\\|?*]'

reuters_url=f'https://www.reuters.com/pf/api/v3/content/fetch/articles-by-section-alias-or-id-v1?query=%7B%22fetch_type%22%3A%22collection_or_section%22%2C%22section_id%22%3A%22%2Fbusiness%2Fautos-transportation%2F%22%2C%22size%22%3A{number_of_articles}%2C%22website%22%3A%22reuters%22%7D&d=296&mxId=00000000&_website=reuters'
response = d.request('GET',reuters_url )

article_urls=[]
article_titles=[]
base_url='https://www.reuters.com'
for item in response.json()['result']['articles']:
    article_name=re.sub(illegal_chars_pattern, '_', item['web'])
    if not os.path.exists(file_path+ '/'+ article_name+'.txt'): #check if article has already been scraped
        article_urls.append(base_url+item['canonical_url'])
        article_titles.append(article_name)

d.quit()

if len(article_urls)==0:
    print('The 20 latest articles have already been scraped')
else:
    for i in range(len(article_urls)):
        driver = webdriver.Chrome()
        driver.get(article_urls[i])
        xpath_expression = "//div[starts-with(@data-testid, 'paragraph-')]"
        div_elements =  driver.find_elements(By.XPATH, xpath_expression) 

        paragraph=''
        for index, div in enumerate(div_elements): 
            inner_html = div.get_attribute('innerHTML')
            paragraph+=inner_html + ' ' + '\n'
        soup = BeautifulSoup(paragraph, 'html.parser')
        driver.quit()
        paragraph= soup.get_text()
        paragraph=paragraph.replace("opens new tab", "")

        with open(f"{file_path}/{article_titles[i]}.txt", "w",encoding="utf-8") as text_file: #save as txt
            text_file.write(paragraph)
            time.sleep(5)

