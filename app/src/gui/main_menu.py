from tkinter import *
from tkinter import messagebox
from gui.products_gui import ProductsMenu
from obs.Events import Events

class MenuWindow(Frame):
    def __init__(self, service, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.service = service
        # All products menu
        self.new_win_prod = None
        self.products_menu = None

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
        scan_bu = Button(self, text="Scan now", command=self.scan_my_products)
        scan_bu.pack(fill=X, padx=10, pady=10)

        settings_bu = Button(self, text="Settings")
        settings_bu.pack(fill=X, padx=10, pady=10)

        exit_bu = Button(self, text="Quit", command=self.exit_program)
        exit_bu.pack(fill=X, padx=10, pady=10)

    def open_my_products(self):
        if self.new_win_prod is not None:
            return

        self.new_win_prod = Toplevel(self)
        self.products_menu = ProductsMenu(self.service, self.new_win_prod)
        self.service.add_observer(self.products_menu, Events.MONITORING)
        self.new_win_prod.protocol("WM_DELETE_WINDOW", self.close_my_products)

    def close_my_products(self):
        self.service.remove_observer(self.products_menu, Events.MONITORING)
        self.new_win_prod.destroy()
        self.new_win_prod = None

    def open_new_products(self):
        pass

    def exit_program(self):
        exit()

    def scan_my_products(self):
        self.service.monitor()
