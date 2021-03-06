from tkinter import *
from tkinter import messagebox


from gui.add_products import AddProducts
from gui.products_gui import ProductsMenu
from obs.Events import Events
from queue import Queue, Empty

from threading_manager.TaskType import TaskType
from threading_manager.monitoring import MonitorProductsTask


class MenuWindow(Frame):
    def __init__(self, service, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.service = service
        # Gui elements
        self.scan_bu = None
        # All products menu
        self.my_products_window = None
        self.my_products_controller = None
        # New products menu
        self.new_products_window = None
        self.new_products_controller = None
        self.init_menu_window()
        self.queue = Queue()


    def init_menu_window(self):
        # Setting up the title
        self.master.title("Price Analyzer")
        # Allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # Button for showing analyzed products
        myp_bu = Button(self, text="My Products", command=self.open_my_products_window)
        myp_bu.pack(fill=X, padx=10, pady=10)

        # Button for adding new products to be analyzed
        new_bu = Button(self, text="Add Products", command=self.open_new_products_window)
        new_bu.pack(fill=X, padx=10, pady=10)

        # Button for exiting the application
        self.scan_bu = Button(self, text="Scan now", command=self.scan_my_products)
        self.scan_bu.pack(fill=X, padx=10, pady=10)

        # Not implemented
        # settings_bu = Button(self, text="Settings")
        # settings_bu.pack(fill=X, padx=10, pady=10)

        exit_bu = Button(self, text="Quit", command=self.exit_program)
        exit_bu.pack(fill=X, padx=10, pady=10)

    def open_my_products_window(self):
        if self.my_products_window is not None:
            return

        self.my_products_window = Toplevel(self)
        self.my_products_controller = ProductsMenu(self.service, self.my_products_window)
        self.service.add_observer(self.my_products_controller, Events.MONITORING, Events.NEW_P)
        self.my_products_window.protocol("WM_DELETE_WINDOW", self.close_my_products_window)

    def close_my_products_window(self):
        self.service.remove_observer(self.my_products_controller, Events.MONITORING, Events.NEW_P)
        self.my_products_window.destroy()
        self.my_products_controller = None
        self.my_products_window = None

    def open_new_products_window(self):
        if self.new_products_window is not None:
            return

        self.new_products_window = Toplevel(self)
        self.new_products_controller = AddProducts(self.service, self.new_products_window)
        self.service.add_observer(self.new_products_controller, Events.NEW_P)
        self.new_products_window.protocol("WM_DELETE_WINDOW", self.close_new_products_window)

    def close_new_products_window(self):
        self.service.remove_observer(self.new_products_controller, Events.NEW_P)
        self.new_products_window.destroy()
        self.new_products_controller = None
        self.new_products_window = None
        pass

    def exit_program(self):
        exit()

    def scan_my_products(self):
        # self.service.monitor()
        # self.master.title("Loading")
        self.scan_bu.config(text='Scanning...', state='disabled')
        MonitorProductsTask(self.queue, self.service).start()
        # What does dis do? How does it synchronize???
        self.master.after(100, self.__process_queue)

    def __process_queue(self):
        try:
            result = self.queue.get(0)
            if result[0] == TaskType.SCAN:
                self.scan_bu.config(text='Scan', state='normal')
            else:
                print('What???')
        except Exception as e:
            self.master.after(100, self.__process_queue)
