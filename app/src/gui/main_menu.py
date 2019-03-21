from tkinter import *
from gui.products_gui import ProductsMenu

class MenuWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master;
        self.init_window()

    def init_window(self):
        # Setting up the title
        self.master.title("Price Analyzer")
        # Allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # Button for showing analyzed products
        products_bu = Button(self, text="My Products", command=self.open_my_products)
        products_bu.pack(fill=X, padx=10, pady=10)

        # Button for adding new products to be analyzed
        new_bu = Button(self, text="Add Products", command=self.open_new_products)
        new_bu.pack(fill=X, padx=10, pady=10)

        # Button for exiting the application
        exit_bu = Button(self, text="Quit", command=self.exit_program)
        exit_bu.pack(fill=X, padx=10, pady=10)

    def open_my_products(self):
        # To close current window
        # self.master.withdraw()
        new_win = Toplevel(self)
        controller = ProductsMenu(new_win)

    def open_new_products(self):
        pass

    def exit_program(self):
        exit()
