

from operator import itemgetter
from urllib.parse import quote



from products import Products
# Заменить на Selenium и возможно понадобится PhantomJS
# import requests
# import bs4 

# url= f"https://plati.market/search/xbox%20game%20pass?pponly=false"
# browser.get(url)
#print("\n БРАУЗЕР ЗАПУЩЕН \n")
  
#time.sleep(5)
product = Products()
      
    
  
def main():
    query =quote(input("Введите название товара: "))   
    url= f"https://plati.market/search/{query}"
    product.ParsePage(url)
    
    

main()

product.sortProducts()
product.read_yaml_file('test.yaml')
product.printData()

  