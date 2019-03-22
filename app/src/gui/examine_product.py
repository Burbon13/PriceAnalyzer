from tkinter import Label, PhotoImage, Button, LEFT, BOTH
import webbrowser
from PIL import Image, ImageTk
import requests
from io import BytesIO
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ExamineProduct:
    def __init__(self, service, product, top_level):
        self.top_level = top_level
        self.service = service
        self.product = product
        self.img = None
        self.init_gui()

    def init_gui(self):
        self.top_level.geometry("500x650")
        Label(self.top_level, text=self.product.title).grid(row=0, column=0, columnspan=2)

        # May want to customize in near future
        link_label = Label(self.top_level, text="Emag - Link to shop", fg="blue", cursor="hand2")
        link_label.grid(row=1, column=0, columnspan=2)
        link_label.bind('<Button-1>', self.open_browser)

        response=requests.get(self.product.image_link)

        self.img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((150,150)))
        panel = Label(self.top_level, image=self.img)
        panel.grid(row=2, column=0, rowspan=2)

        current_data = self.service.current_price(self.product._id)
        current_price = current_data[0]
        current_price_str = str(current_price) + '  (' + str(current_data[1].strftime("%Y-%m-%d %H:%M:%S")) + ')' if current_price != -1 else 'No data record' 

        best_data = self.service.lowest_price(self.product._id)
        lowest_price = best_data[0]
        lowest_price_str = str(lowest_price) + '  (' + str(best_data[1].strftime("%Y-%m-%d %H:%M:%S")) + ')' if lowest_price != -1 else 'No data record'

        Label(self.top_level, text='Current price: ' + current_price_str).grid(row=3, column=1)
        Label(self.top_level, text='Lowest price: ' + lowest_price_str).grid(row=2, column=1)

        monitoring_status = 'This device is being monitored' if self.product.monitored else 'This device is not being monitored'
        fg = 'green' if self.product.monitored else 'red'
        Label(self.top_level, text=monitoring_status, fg=fg).grid(row=4, column=1)

        text_bu = 'Turn off' if self.product.monitored else 'Turn on'
        Button(self.top_level, text=text_bu).grid(row=4, column=0)

        history = self.service.get_all_history(self.product._id)

        if len(history) > 0:
            Data2 = {'Date': [h[0] for h in history],'Price': [h[1] for h in history]}
            df2 = DataFrame(Data2,columns=['Date','Price'])
            df2 = df2[['Date', 'Price']].groupby('Date').sum()
            
        figure2 = plt.Figure(figsize=(5,4), dpi=100)
        ax2 = figure2.add_subplot(111)
        line2 = FigureCanvasTkAgg(figure2, self.top_level)
        line2.get_tk_widget().grid(row=5, column=0, columnspan=2)
        
        if len(history) > 0:
            df2.plot(kind='line', legend=True, ax=ax2, color='r',marker='o', fontsize=10)
            
        ax2.set_title('Price evolution')
    
    def open_browser(self, event):
        webbrowser.open_new(self.product.link)
    