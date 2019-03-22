from tkinter import *
from gui.examine_product import ExamineProduct
from obs.Events import Events
from Domain import Product

class ProductsMenu:
    def __init__(self, service, top_level):
        self.top_level = top_level
        self.service = service
        self.products = []
        self.listbox = None
        self.init_gui()

    def init_gui(self):
        # Setting the size of the window
        self.top_level.geometry("500x400")

        # Top window label
        Label(self.top_level, text="Your products!").pack()

        # Frame to encapsulate the listbox and scrollbar
        frame = Frame(self.top_level, bd=2, relief=SUNKEN)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Scrollbar listent to changes in the listbox to set it's position correctly
        self.listbox = Listbox(frame, bd=0, yscrollcommand=scrollbar.set)
        
        # Bind double click event to the listbox
        self.listbox.bind('<Double-Button-1>', self.on_product_select)
        self.listbox.bind('<Return>', self.on_product_select)

        # fill - tells the manager that the widget wants to fill the entire space assignet to it
        # expand - tells the manager to assign additional space to the widget box
        #        - if the parent widget is made larger, hold everything packed, any exceeding space
        #          will be distributed among all widgets that have expand option set to a non-zero value                   
        self.listbox.pack(fill=BOTH, expand=1)
        frame.pack(fill=BOTH, expand=1)   

        self.products = self.service.find_all_products()
        for index, product in enumerate(self.products):
            self.listbox.insert(END, product.title)
            self.listbox.itemconfig(index, foreground = 'green' if product.monitored else 'red')

        # listbox.itemconfig(3, {'fg': 'blue'})

        # Listbox listens to changes in the scrollbar to set its view position right
        scrollbar.config(command=self.listbox.yview)

    def on_product_select(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])

        new_win = Toplevel(self.top_level)
        ex = ExamineProduct(self.service, self.products[index], new_win)
        self.service.add_observer(ex, Events.MONITORING)

    def update(self, data, event):
        if event == Events.MONITORING:
            index = next(i for i,v in enumerate(self.products) if v._id == data[0])
            self.listbox.itemconfig(index, foreground = 'green' if data[1] else 'red')
