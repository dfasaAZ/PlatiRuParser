

from operator import itemgetter


from app import App
from products import Products

product = Products()


def main():
    
    
    # my_window.create_window()
    # query =input("Введите название товара: ")
    
    # product.ParsePage(query)
    #product.write_yaml_file('test.yaml')
    try:
        product.read_yaml_file('test.yaml')
    except:
        product.write_yaml_file('test.yaml')
        pass
    my_window = App("Plati.market Parser")
    my_window.create_window()
    #print(product.data)


main()

# product.sortProducts('rating')
# product.printData()

