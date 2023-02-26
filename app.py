import tkinter as tk
from tkinter import ttk
from products import Products
import webbrowser

class App:
    def __init__(self, title):
        self.title = title
        self.window = None
        self.product=Products()
        self.filePath="test.yaml"
        self.data = []
        self.order= 0
    def create_window(self):
        # Create the window
        self.window = tk.Tk()#Main widget
        self.window.title(self.title)
        self.window.geometry("720x480")
        #Gather information
        self.product.read_yaml_file(self.filePath)
        self.data=self.product.data
        # Add widgets to the window
        label = tk.Label(self.window, text="Hello, World!")
        label.pack()
         # Create the Update button and pack it
        update_button = tk.Button(self.window, text="Update", command=self.update_window)
        update_button.pack()
        
        self.text_field = tk.Entry(self.window)
        self.text_field.pack(side=tk.TOP)
        update_button = tk.Button(self.window, text="Search", command=self.search)
        update_button.pack()

        button_frame = tk.Frame(self.window)
        button_frame.pack()

        button1 = tk.Button(button_frame, text="Цена", command=lambda: self.sortResults("price"))
        button1.pack(side=tk.LEFT)

        button2 = tk.Button(button_frame, text="Кол-во продано", command=lambda: self.sortResults("sold"))
        button2.pack(side=tk.LEFT)

        button3 = tk.Button(button_frame, text="Рейтинг продавца", command=lambda: self.sortResults("rating"))
        button3.pack(side=tk.LEFT)

        #Create list
        self.table= MyListbox(self.window,self.data)
        self.table.create_treeview()
        
        # Run the window
        self.window.mainloop()
    def update_window(self):
        self.product.read_yaml_file(self.filePath)
        self.data = self.product.data
        self.table.update_treeview(self.data)
    def search(self):
        self.product.ParsePage(self.text_field.get()) 
        self.product.write_yaml_file(self.filePath) 
        self.update_window()
    def sortResults(self,a):
        self.order= not self.order
        self.product.sortProducts(a,self.order) 
        self.data = self.product.data
        self.table.update_treeview(self.data)    
        
class MyListbox:
    def __init__(self, master, items):
        self.master = master
        self.items = items
        self.treeview = None
    
    def create_treeview(self):
        # Create the Treeview
        self.treeview = ttk.Treeview(self.master, columns=("name", "price", "rating", "sold"), show="headings", selectmode="browse")
        
        # Define the column headings
        self.treeview.heading("name", text="Name")
        self.treeview.heading("price", text="Price")
        self.treeview.heading("rating", text="Rating")
        self.treeview.heading("sold", text="Sold")
        
        # Add items to the Treeview
        for item in self.items:
            self.treeview.insert("", tk.END, values=(item['name'], item['price'], item['rating'], item['sold']), tags=(item['link'],))
        
        # Bind a function to the double click event on a row to open the corresponding link
        self.treeview.bind("<Double-1>", self.open_link)
        
        # Pack the Treeview
        self.treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def update_treeview(self, data):
        self.data = data
        # Delete the existing items in the Treeview
        self.treeview.delete(*self.treeview.get_children())
        # Add the updated items to the Treeview
        for item in self.data:
            self.treeview.insert("", tk.END, values=(item['name'], item['price'], item['rating'], item['sold']), tags=(item['link'],))
    
    def open_link(self, event):
        # Get the item selected in the Treeview
        item = self.treeview.selection()[0]
        # Get the link associated with the item
        link = self.treeview.item(item, "tags")[0]
        # Open the link in the default web browser
        webbrowser.open(link)   