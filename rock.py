
import json
import time
from seleniumrequests import Chrome
from selenium.webdriver.common.by import By

import html
import pandas as pd






number_of_articles=60 # integer must be a multiple of 12
base_url='https://www.bloomberg.com'

article_urls=[]
article_titles=[]

illegal_chars_pattern = r'[<>:"/\\|?*]'

for offset in range(0,number_of_articles,12):
     
    d = Chrome()
    time.sleep(2)
    bloomberg_url=f'https://www.bloomberg.com/lineup-next/api/paginate?id=archive_story_list&page=phx-industries-transportation&offset={offset}&variation=archive&type=lineup_content'
    d.get(bloomberg_url)
    time.sleep(5)
    xpath_expression = "//pre"
    div_element =  d.find_element(By.XPATH, xpath_expression)
    
    inner_html = div_element.get_attribute('innerHTML')
    decoded_string = html.unescape(inner_html)


    response=json.loads(decoded_string)    
    d.quit() 
    for i in range(len(response['archive_story_list']['items'])):
        article_urls.append(base_url+response['archive_story_list']['items'][i]['url'])
        article_titles.append(response['archive_story_list']['items'][i]['headline'])


df=pd.DataFrame({'article_name':article_titles,'article_url':article_urls})
df.to_csv('bloomberg.csv', index=False)



