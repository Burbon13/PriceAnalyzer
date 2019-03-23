import requests
import webbrowser
from PIL import ImageTk, Image
from six import BytesIO
from tkinter import Label, Button, Message, Grid, E, W, S, N, DISABLED

from obs.Events import Events


class ExamineNewProduct:
    def __init__(self, service, product, top_level):
        self.top_level = top_level
        self.service = service
        self.product = product
        self.imf = None
        self.already_exists = self.service.product_already_exists(self.product.id)
        # GUI elements
        self.add_bu = None
        self.init_gui()

    def init_gui(self):
        self.top_level.geometry("400x450")
        Message(self.top_level, text=self.product.title, width=380).grid(row=0, column=0, columnspan=2, sticky=N+S+W+E)

        # May want to customize in near future
        link_label = Label(self.top_level, text="Emag - Link to shop", fg="blue", cursor="hand2")
        link_label.grid(row=1, column=1, sticky=N+S+W+E)
        link_label.bind('<Button-1>', self.open_browser)

        response = requests.get(self.product.image_link)

        self.img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((150, 150)))
        panel = Label(self.top_level, image=self.img)
        panel.grid(row=1, column=0, rowspan=2, sticky=N+S+W+E)

        Label(self.top_level, text='Current price: ' + str(self.product.new_price)).grid(row=2, column=1)

        text_bu = 'Add'
        self.add_bu = Button(self.top_level, text=text_bu, command=self.add_product)
        self.add_bu.grid(row=3, column=0, columnspan=2, sticky=N + S + W + E)
        if self.already_exists:
            self.add_bu.config(state=DISABLED)

        for x in range(4):
            Grid.rowconfigure(self.top_level, x, weight=1)
        for x in range(2):
            Grid.columnconfigure(self.top_level, x, weight=1)

    def add_product(self):
        self.service.save_products(self.product)

    def open_browser(self, event):
        webbrowser.open_new(self.product.link)

    def update(self, data, event):
        if event == Events.NEW_P:
            id = data
            if id == self.product.id:
                self.add_bu.config(state=DISABLED)
        else:
            print('Update not implemented for ' + str(event))
