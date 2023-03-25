import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

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
        self.table=None
       
    def create_window(self):
        # Create the window
        self.window = tk.Tk()#Main widget
        self.window.title(self.title)
        self.window.geometry("720x480")
        #Gather information
        self.product.read_yaml_file(self.filePath)
        self.data=self.product.data
        # Add widgets to the window
        label = tk.Label(self.window, text="Input what you like to find in the field below\nDouble click on the result to open it in external browser")
        label.pack()
        #  # Create the Update button and pack it
        # update_button = tk.Button(self.window, text="Update", command=self.update_window)
        # update_button.pack()
        
        self.text_field = tk.Entry(self.window)
        self.text_field.pack(side=tk.TOP)
        update_button = tk.Button(self.window, text="Search", command=self.search)
        update_button.pack()


        
        
        # Run the window
        self.window.mainloop()
    def update_window(self):
        self.product.read_yaml_file(self.filePath)
        self.data = self.product.data
        #Create list
        if not self.table:
            self.table= MyListbox(self.window,self.data)
            self.table.create_treeview()
        self.table.update_treeview(self.data)
    def search(self):
        self.product.parseAPI(self.text_field.get()) 
        self.product.write_yaml_file(self.filePath) 
        self.update_window()
        self.table.update_treeview(self.data) 
    def sortResults(self,a):
        """deprecated, sorting is now performed inside treeview"""
        self.order= not self.order
        self.product.sortProducts(a,self.order) 
        self.data = self.product.data
        self.table.update_treeview(self.data)    
        
class MyListbox:
    def __init__(self, master, items):
        self.master = master
        self.items = items
        self.treeview = None
        self.columns= ["name", "price", "rating", "sold"]
        self.sort_column = None
    
    def create_treeview(self):
        # Create the Treeview
        self.treeview = ttk.Treeview(self.master, columns=("name", "price", "rating", "sold"), show="headings", selectmode="browse")
        


        for column in self.columns:
            self.treeview.heading(column, text=column, anchor=tk.CENTER,command=lambda c=column: self.sort_by_column(c))
            self.treeview.column(column, anchor=tk.CENTER)
            
        
        
        # Add items to the Treeview
        for item in self.items:
            self.treeview.insert("", tk.END, values=(item['name'], item['price'], item['rating'], item['sold']), tags=(item['link'],))
         # Automatically set the width of each column based on the length of the data in that column
        for col in self.treeview["columns"]:
            max_len = max([len(str(self.treeview.set(row, col))) for row in self.treeview.get_children()])
            self.treeview.column(col, width=max_len * 10)
        # Bind a function to the double click event on a row to open the corresponding link
        self.treeview.bind("<Double-1>", self.open_link)
        
        # Pack the Treeview
        self.treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    def sort_by_column(self, column):
        # Determine the sort order
        if self.sort_column == column:
            self.sort_descending = not self.sort_descending
        else:
            self.sort_column = column
            self.sort_descending = False

        # Sort the data
        self.items.sort(key=lambda x: x[self.sort_column], reverse=self.sort_descending)

        # Update the Treeview display
        self.treeview.delete(*self.treeview.get_children())
        for item in self.items:
            formatted_item = (item["name"], item["price"], item["rating"], item["sold"])
            self.treeview.insert("", tk.END, values=formatted_item,tags=(item['link'],))
    def update_treeview(self, data):
        self.items = data
        # Delete the existing items in the Treeview
        self.treeview.delete(*self.treeview.get_children())
        # Add the updated items to the Treeview
        for item in self.items:
            self.treeview.insert("", tk.END, values=(item['name'], item['price'], item['rating'], item['sold']), tags=(item['link'],))
    
    def open_link(self, event):
        # Get the item selected in the Treeview
        item = self.treeview.selection()[0]
        # Get the link associated with the item
        link = self.treeview.item(item, "tags")[0]
        # Open the link in the default web browser
        webbrowser.open(link)   