import tkinter as tk
from products import Products

class App:
    def __init__(self, title):
        self.title = title
        self.window = None
        self.product=Products()
        self.filePath="test.yaml"
        self.data = []
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
        #Create list
        self.listBox= MyListbox(self.window,self.data)
        self.listBox.create_listbox()
        
        # Run the window
        self.window.mainloop()
    def update_window(self):
        self.product.read_yaml_file(self.filePath)
        self.data = self.product.data
        self.listBox.update_listbox(self.data)
    def search(self):
        self.product.ParsePage(self.text_field.get()) 
        self.product.write_yaml_file(self.filePath) 
        self.update_window()  
        
class MyListbox:
    def __init__(self, master, items):
        self.master = master
        self.items = items
        self.listbox = None
    
    def create_listbox(self):
        # Create the listbox
        self.listbox = tk.Listbox(self.master, width=50)
        
        # Add items to the listbox
        for item in self.items:
            formatted_item = f"{item['name']} - {item['price']} - {item['rating']}"
            self.listbox.insert(tk.END, formatted_item)
        
        # Pack the listbox
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)        
    def update_listbox(self,data):
        self.data=data
        # Delete the existing items in the Listbox
        self.listbox.delete(0, tk.END) 
        # Add the updated items to the Listbox
        for item in self.data:
            formatted_item = f"{item['name']} - {item['price']} - {item['rating']}"
            self.listbox.insert(tk.END, formatted_item)   