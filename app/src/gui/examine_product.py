from tkinter import Label, PhotoImage
import webbrowser
from PIL import Image, ImageTk
import requests
from io import BytesIO

class ExamineProduct:
    def __init__(self, service, product, top_level):
        self.top_level = top_level
        self.service = service
        self.product = product
        self.img = None
        self.init_gui()

    def init_gui(self):
        self.top_level.geometry("500x400")
        Label(self.top_level, text=self.product.title).grid(row=0, column=0, columnspan=2)
        link_label = Label(self.top_level, text="Link to shop", fg="blue", cursor="hand2")
        link_label.grid(row=1, column=0, columnspan=2)
        link_label.bind('<Button-1>', self.open_browser)

        response=requests.get(self.product.image_link)

        self.img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((150,150)))
        panel = Label(self.top_level, image=self.img)
        panel.grid(row=2, column=0)
        # self.im = Image.open("iphone.jpg")
        # self.im.show()
    
    def open_browser(self, event):
        webbrowser.open_new(self.product.link)
    