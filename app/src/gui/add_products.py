from tkinter import Entry, Frame, Scrollbar, RIGHT, Listbox, BOTH, SUNKEN, Y, END, Grid, W, E, N, S, Button, Toplevel
from tkinter.ttk import Combobox

from gui.examine_new_product import ExamineNewProduct


class AddProducts:
    def __init__(self, service, top_level):
        self.service = service
        self.top_level = top_level
        # Gui elements
        self.name_entry = None
        self.shops_combo = None
        self.category_combo = None
        self.search_button = None
        self.listbox = None
        # Last searched products list
        self.products_found = None
        self.init_gui()

    def init_gui(self):
        self.top_level.geometry("600x750")

        self.name_entry = Entry(self.top_level)
        self.name_entry.grid(row=0, column=0, columnspan=2, sticky=W + E)
        self.name_entry.insert(0, 'Product name')
        self.name_entry.bind("<FocusIn>", lambda args: self.name_entry.delete('0', 'end'))

        # shop_choices = ['Emag', 'Altex', 'Media Galaxy']
        shop_choices = ['Emag']
        self.shops_combo = Combobox(self.top_level, values=shop_choices)
        self.shops_combo.grid(row=1, column=0, sticky=W + E)
        self.shops_combo.current(0)

        # Make it configurable from config file
        category_choices = ['Laptops', 'Phones', 'Tablets', 'Tvs', 'Portable speakers', 'Headphones', 'Consoles']
        self.category_combo = Combobox(self.top_level, values=category_choices)
        self.category_combo.grid(row=1, column=1, sticky=W + E)
        self.category_combo.current(0)

        # Search bu
        self.search_button = Button(self.top_level, text='Search', command=self.on_search_event)
        self.search_button.grid(row=2, column=0, columnspan=2, sticky=W + E + S + N)

        # Frame to encapsulate the listbox and scrollbar
        frame = Frame(self.top_level, bd=2, relief=SUNKEN)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox = Listbox(frame, bd=0, yscrollcommand=scrollbar.set)

        self.listbox.bind('<Double-Button-1>', self.on_product_inspect)
        self.listbox.bind('<Return>', self.on_product_inspect)

        self.listbox.pack(fill=BOTH, expand=1)
        frame.grid(row=3, column=0, columnspan=2, sticky=W + E + N + S)

        scrollbar.config(command=self.listbox.yview)

        for x in range(3):
            Grid.rowconfigure(self.top_level, x, pad=10)
        Grid.rowconfigure(self.top_level, 3, weight=1)
        for x in range(2):
            Grid.columnconfigure(self.top_level, x, weight=1)

    def on_product_inspect(self, event):
        w = event.widget
        index = int(w.curselection()[0])

        new_win = Toplevel(self.top_level)
        ex = ExamineNewProduct(self.service, self.products_found[index], new_win)
        # TODO: Add observeersssssss!
        # self.service.add_observer(ex, Events.MONITORING)
        # new_win.protocol("WM_DELETE_WINDOW", lambda: self.destroy_examination(ex, new_win))

    def destroy_examination(self, ex, new_win):
        # self.service.remove_observer(ex, Events.MONITORING)
        # new_win.destroy()
        pass

    def on_search_event(self):
        self.products_found = self.service.search_products(self.name_entry.get(), self.category_combo.get(), 'Emag')
        if self.products_found is None:
            return
        self.listbox.delete(0, 'end')
        for index, product in enumerate(self.products_found):
            self.listbox.insert(END, product.title)
            if self.service.product_already_exists(product.id):
                self.listbox.itemconfig(index, foreground='orange')
