#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


#getting the query from user
query = input('Enter the category')

#function to get the url of the query 
def creating_query(keyword):
    kw = keyword.split()
    if len(kw)==2:
        return(f"https://www.coursera.org/search?query={kw[0]}%20{kw[1]}")
    elif len(kw)==1:
        return(f"https://www.coursera.org/search?query={kw[0]}")

    else:
        raise Exception('Your entry needs to be only one or two words, divided by a white space')
#storing the query
url = creating_query(query)

#initiating the web driver
driver = webdriver.Chrome()
driver.get(url)
#waiting for the page to load 
driver.implicitly_wait(30)
#function for getting all the links
def get_links():
    driver.maximize_window()
    links_we = driver.find_elements(By.XPATH,"//a[@data-click-key='search.search.click.search_card']")
    links = []
    for e in links_we:
        links.append(e.get_attribute('href'))
    return links
#function for going to the next_page 
def next_page():
    driver.maximize_window()
    driver.implicitly_wait(30)
    next_page= driver.find_element(By.XPATH,"//button[@data-e2e='pagination-controls-next']")
    next_page.click()
#storing all the links    
all_links = []    
count = 1
#getting the number of pages
last_page = driver.find_elements(By.XPATH,"//span[@class='cds-33 css-pa6u6k cds-35']")
last_page_int = int(last_page[-1].text)
#looping through all the pages 
while count<=last_page_int:
    all_links+=get_links()
    next_page()
    count+=1
#creating a data frame for our data

table_of_content = pd.DataFrame(columns=['Links','Course Name','Course Provider', 'Course Description', '# Enrolled', '# Rating'])

#assigning the links we just found to our data frame 
table_of_content['Links']=all_links


#Itterating through the links and getting the needed information


def get_course_page(url):
    
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(30)
    
    
    try:
        #course name web element = cn_we
        cn_we = driver.find_element(By.XPATH,"//h1[@class='banner-title m-b-0']")
    except:
        cn_we = driver.find_element(By.XPATH,"//h1[@class='banner-title banner-title-without--subtitle m-b-0']")
    
    course_name = cn_we.text
    

    #finding course providers
    
    cp_we = driver.find_elements(By.XPATH,"//h3[@class='headline-4-text bold rc-Partner__title']")
        
    #some courses have more than one provider. getting all of them
    course_provider = [el.text for el in cp_we]
   #COURSE DESCRIPTION
    try:
        course_description = driver.find_element(By.XPATH,"//div[@class='AboutS12n']").text
    except:
        course_description = driver.find_element(By.XPATH,"//div[@class='AboutCourse']").text
    
    #number of people enrolled
    try:
        
        enrolled = driver.find_element(By.XPATH,"//div[@class='rc-ProductMetrics']").text
    except:
        enrolled= ''

    #number of ratings
    try: 
        rating_we = driver.find_element(By.XPATH,"//span[@data-test='ratings-count-without-asterisks']").text
    
    except:
        rating_we = ''
    
    if rating_we!='':
        rating = [el.text for el in rating_we][:1]
    
    else:
        rating = rating_we
    
    
    
    return course_name,course_provider,course_description,enrolled, rating 



for index,row in table_of_content.iterrows():
    
    link = row['Links']
    
    row['Course Name'], row['Course Provider'], row['Course Description'], row['# Enrolled'], row['# Rating'] = get_course_page(link)
    

    
driver.quit()

os.makedirs('folder/data', exist_ok=True)  
table_of_content.to_csv('folder/data/data.csv')  

