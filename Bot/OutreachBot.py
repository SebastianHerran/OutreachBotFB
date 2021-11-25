#!/usr/bin/env python
# coding: utf-8

# In[55]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
import time
import os


# ### Extract Facebook links from company webpages

# In[47]:


def selenium_extract_face_link(url):
    global driver
    options_chrome = Options()
    options_chrome.add_argument("headless")
    driver = webdriver.Chrome(options=options_chrome)
    driver.get(url)
    WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CSS_SELECTOR, facebook_css)))
    empresa = driver.page_source
    soup_emp = BeautifulSoup(empresa, 'lxml')
    return soup_emp


# In[48]:


def RodoBot_extract_fbs(urls):   
    feisbucs=[]
    facebook_css = '[href*="facebook.com/"]:not([href*="facebook.com/sharer"])'
    
    for url in urls:
        try:
            empresa = requests.get(url)
            soup_emp = BeautifulSoup(empresa.content, 'lxml')
            face_link= soup_emp.select(facebook_css)
            
            if len(face_link) > 0: feisbucs.append(face_link[0]['href'])
            else: raise Exception("No Facebook link found")
        except:
            try:
                face_link= selenium_extract_face_link(url).select(facebook_css) 
                feisbucs.append(face_link[0]['href'])
                driver.quit()
            except:
                driver.quit()
                try:
                        face_link= selenium_extract_face_link(url).select(facebook_css) 
                        feisbucs.append(face_link[0]['href'])
                except:
                        feisbucs.append('')
                finally:
                    driver.quit()
    return feisbucs


# ### Get email from facebook page ###

# In[49]:


def RodoBot_get_contact_from_fb_page(fb_links):
    contact_emails=[]
    
    user_data_path = os.path.dirname(os.path.abspath('__file__'))+'\\User_Data'
    options_chrome = Options()
    options_chrome.add_argument(f"user-data-dir={user_data_path}")
    options_chrome.add_argument("headless")
    driver = webdriver.Chrome(options=options_chrome)
    
    email_class = re.sub(' ','.','oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl py34i1dx gpro0wi8')
    contact_email_css = f'a.{email_class}[href^="mailto:"]'
    
    for fb_link in fb_links:
        if fb_link == '': contact_emails.append('')
        else:
            try:
                driver.get(fb_link)
                WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CSS_SELECTOR, contact_email_css)))
                facebook_page = driver.page_source
                soup_facebook_page = BeautifulSoup(facebook_page, 'lxml')
                email_address = soup_facebook_page.select(contact_email_css)
                if email_address: contact_emails.append(email_address[0].text)
            except:
                driver.quit()
                try:
                    driver = webdriver.Chrome(options=options_chrome)
                    driver.get(fb_link)
                    WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CSS_SELECTOR, contact_email_css)))
                    facebook_page = driver.page_source
                    soup_facebook_page = BeautifulSoup(facebook_page, 'lxml')
                    email_address = soup_facebook_page.select(contact_email_css)
                    if email_address: contact_emails.append(email_address[0].text)
                except:
                    contact_emails.append('')
                
    driver.quit()
    return contact_emails


# ### Outreach Bot

# In[54]:


def OutreachBot(urls):    
    feisbucs = RodoBot_extract_fbs(urls)
    contact_emails = RodoBot_get_contact_from_fb_page(feisbucs)
    
    links = pd.DataFrame(zip(urls,feisbucs,contact_emails), columns=['URL','Facebook','Contact Emails'])
    
    return links


# ### Input

# In[51]:


input_file = os.listdir(os.path.dirname(os.path.abspath('__file__'))+'\\Input')
df_input = pd.read_csv(os.path.dirname(os.path.abspath('__file__'))+'\\Input\\'+input_file[0])


# ### Output

# In[60]:


df_output = OutreachBot(df_input.iloc[:,0])
print('Done!')
df_output.to_csv(os.path.dirname(os.path.abspath('__file__'))+'\\Output\\'+'Output_File.csv')

