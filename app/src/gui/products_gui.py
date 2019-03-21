from tkinter import *

class ProductsMenu:
    def __init__(self, top_level):
        self.top_level = top_level
        self.init_gui()

    def init_gui(self):
        # Setting the size of the window
        self.top_level.geometry("400x300")

        # Top window label
        Label(self.top_level, text="Your products!").pack()

        # Frame to encapsulate the listbox and scrollbar
        frame = Frame(self.top_level, bd=2, relief=SUNKEN)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Scrollbar listent to changes in the listbox to set it's position correctly
        listbox = Listbox(frame, bd=0, yscrollcommand=scrollbar.set)

        # fill - tells the manager that the widget wants to fill the entire space assignet to it
        # expand - tells the manager to assign additional space to the widget box
        #        - if the parent widget is made larger, hold everything packed, any exceeding space
        #          will be distributed among all widgets that have expand option set to a non-zero value                   
        listbox.pack(fill=BOTH, expand=1)
        frame.pack(fill=BOTH, expand=1)   

        # Mock data
        for i in range(100):
            listbox.insert(END, "iPhone 6s " + str(i))

        # Listbox listens to changes in the scrollbar to set its view position right
        scrollbar.config(command=listbox.yview)