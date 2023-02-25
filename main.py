
import json
import time
import re
import operator
from operator import itemgetter
from urllib.parse import quote

import csv
import asyncio
import aiohttp
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
# Заменить на Selenium и возможно понадобится PhantomJS
# import requests
# import bs4 

# url= f"https://plati.market/search/xbox%20game%20pass?pponly=false"
# browser.get(url)
#print("\n БРАУЗЕР ЗАПУЩЕН \n")
class Products:
    data =[] #Список, в котором будут словари
    def sortProducts():
        Products.data.sort(key=operator.itemgetter('price')) 

#time.sleep(5)
product = Products
def ParsePage(url):
    """Find all elements on page and store them into the dictionary"""
    options = Options()
    #options.add_argument("headless")
    
    browser = webdriver.Edge(executable_path='msedgedriver.exe',options=options)

    
    
        
    browser.get(url)
    time.sleep(1)
    for i in range(1,23):
        
        try:
            browser.find_element(By.ID,'gdpr_accept_button').click()
        except:
            pass
        try:
            allBlocks =  browser.find_elements(By.CSS_SELECTOR,'li.shadow') #:Список всех блоков с товаром
           
            pageNumber = int(browser.find_elements(By.CSS_SELECTOR,'a.active')[1].text) #:Номер текущей страницы
        except:
            print("Результаты не найдены")
            break
        for block in allBlocks:
            BlockTitle = block.find_element(By.TAG_NAME,'h1')#""" Часть блока с ценой и названием"""
            BlockName  = BlockTitle.find_element(By.TAG_NAME,'a')#"""Название блока"""
            BlockLink = BlockName.get_attribute('href')#"""Ссылка на продукт"""
            BlockPrice = BlockTitle.find_element(By.TAG_NAME,'span')
            RubPrice=re.search(" [0-9]+ ",BlockPrice.text)
            RubPrice=int(RubPrice.group(0))
        #print(allBlocks[0].text)
        #print('\n'+BlockName.get_attribute('href'))
            product.data.append({'name':BlockName.text,'link':BlockLink,'price':RubPrice})
        try:
            browser.find_element(By.LINK_TEXT,str(pageNumber+1)).click()
        except:
            break        
    
  
def main():
    query =quote(input("Введите название товара: "))   
    url= f"https://plati.market/search/{query}"
    ParsePage(url)
    
    
#data.append(asyncio.run(main()))
main()
#product.data.sort(key=operator.itemgetter('price')) 
product.sortProducts()
for item in product.data:
    print (item['name']+'\t'+item['link']+'\n'+str(item['price'])+'\n\n')

  