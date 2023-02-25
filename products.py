
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

    def sortProducts(self):
        Products.data.sort(key=operator.itemgetter('price'))

    def printData(self):
        for item in self.data:
            print(item['name']+'\t'+item['link'] +
                  '\n'+str(item['price'])+'\n\n')

    def ParsePage(self, url):
        """Find all elements on page and store them into the dictionary"""
        options = Options()
        # options.add_argument("headless")

        browser = webdriver.Edge(
            executable_path='msedgedriver.exe', options=options)

        browser.get(url)
        time.sleep(1)
        while True:

            try:
                browser.find_element(By.ID, 'gdpr_accept_button').click()
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
            # print(allBlocks[0].text)
            # print('\n'+BlockName.get_attribute('href'))
                self.data.append(
                    {'name': BlockName.text, 'link': BlockLink, 'price': RubPrice})
            try:
                browser.find_element(By.LINK_TEXT, str(pageNumber+1)).click()
            except:
                break
