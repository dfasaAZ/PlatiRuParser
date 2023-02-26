from urllib.parse import quote
import time
import re
import operator
from operator import itemgetter
from urllib.parse import quote
import yaml


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options


class Products:
    data = []  # Список, в котором будут словари

    def read_yaml_file(self, filename):
        """Read the data from a YAML file and return a list of dictionaries"""
        with open(filename, 'r') as file:
            self.data = yaml.load(file, Loader=yaml.FullLoader)
        return

    def write_yaml_file(self, filename):
        """Write the data in YAML format to a file"""
        with open(filename, 'w') as file:
            yaml.dump(self.data, file)

    def sortProducts(self,criteria: str,order :bool=False):
        """Sort list of products by given criteria:
        \n price - price of a product
        \n rating - total rating of a seller
        \n sold - the amount of items sold
        \n\n order - asc=0, desc=1
        """
        self.data.sort(key=operator.itemgetter(criteria),reverse=order)

    def printData(self):
        for item in self.data:
            print(item['name']+'\t'+item['link'] +
                  '\n'+str(item['price'])+"  "+str(item['rating'])+"   "+str(item['sold'])+'\n\n')

    def ParsePage(self, query):
        """Find all elements on page and store them into the dictionary"""
        self.data=[]
        options = Options()
        options.add_argument("headless")# Показывать ли окно браузера

        browser = webdriver.Edge(
            executable_path='msedgedriver.exe', options=options)
        q=quote(query)
        url = f"https://plati.market/search/{q}"
        browser.get(url)
        time.sleep(1)
        #Searching through website
        while True:

            try:
                browser.find_element(By.ID, 'gdpr_accept_button').click()#Accept cookies if present, DO NOT REMOVE
            except:
                pass
            try:
                # :Список всех блоков с товаром
                allBlocks = browser.find_elements(By.CSS_SELECTOR, 'li.shadow')

                pageNumber = int(browser.find_elements(By.CSS_SELECTOR, 'a.active')[
                                 1].text)  # :Номер текущей страницы
            except:
                print("Результаты не найдены")
                break
            for block in allBlocks:
                BlockTitle = block.find_element(
                    By.TAG_NAME, 'h1')  # """ Часть блока с ценой и названием"""
                BlockName = BlockTitle.find_element(
                    By.TAG_NAME, 'a')  # """Название блока"""
                BlockLink = BlockName.get_attribute(
                    'href')  # """Ссылка на продукт"""
                BlockPrice = BlockTitle.find_element(By.TAG_NAME, 'span')
                RubPrice = re.search(" [0-9]+ ", BlockPrice.text)
                RubPrice = int(RubPrice.group(0))
                BlockInfo = block.find_elements(By.TAG_NAME,"strong")#all additional information
                BlockRating= float(BlockInfo[0].text.replace(',','.'))#sellers rating
                try:
                    BlockSold = int(BlockInfo[1].text.replace('>',''))#Total amount sold
                except:
                    BlockSold=0#На случай если у блока нет информации
                    pass

            
                self.data.append(
                    {'name': BlockName.text, 'link': BlockLink, 'price': RubPrice,'rating':BlockRating,'sold':BlockSold})
            try:
                browser.find_element(By.LINK_TEXT, str(pageNumber+1)).click()# Переход на следующую страницу
            except:
                break
