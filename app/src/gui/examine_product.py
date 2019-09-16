from tkinter import Label, PhotoImage, Button, LEFT, BOTH, Grid
import webbrowser
from PIL import Image, ImageTk
from io import BytesIO
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from obs.Events import Events


class ExamineProduct:
    def __init__(self, service, product, top_level):
        self.top_level = top_level
        self.service = service
        self.product = product
        self.img = None
        self.monitor_bu = None
        self.monitor_label = None
        self.figure = None
        self.current_price_label = None
        self.best_price_label = None
        self.init_gui()

    def init_gui(self):
        self.top_level.geometry("600x750")
        Label(self.top_level, text=self.product.title).grid(row=0, column=0, columnspan=2)

        # May want to customize in near future
        link_label = Label(self.top_level, text="Emag - Link to shop", fg="blue", cursor="hand2")
        link_label.grid(row=1, column=0, columnspan=2)
        link_label.bind('<Button-1>', self.open_browser)

        img_data = self.service.get_image(self.product._id)

        self.img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)).resize((150, 150)))
        panel = Label(self.top_level, image=self.img)
        panel.grid(row=2, column=0, rowspan=2)

        self.current_price_label = Label(self.top_level)
        self.current_price_label.grid(row=3, column=1)
        self.best_price_label = Label(self.top_level)
        self.best_price_label.grid(row=2, column=1)

        self.set_price_labels()

        monitoring_status = 'This device is being monitored' if self.product.monitored else 'This device is not being monitored'
        fg = 'green' if self.product.monitored else 'red'
        self.monitor_label = Label(self.top_level, text=monitoring_status, fg=fg)
        self.monitor_label.grid(row=4, column=1)

        text_bu = 'Turn off' if self.product.monitored else 'Turn on'
        self.monitor_bu = Button(self.top_level, text=text_bu, command=self.set_monitoring)
        self.monitor_bu.grid(row=4, column=0)

        self.set_price_plot()

        Button(self.top_level, text='Remove product').grid(row=6, column=0, columnspan=2)

        for x in range(7):
            Grid.rowconfigure(self.top_level, x, weight=1)
        for x in range(2):
            Grid.columnconfigure(self.top_level, x, weight=1)

    def set_price_plot(self):
        if self.figure is not None:
            self.figure.clf()

        history = self.service.get_all_history(self.product._id)

        # Plotting part
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        ax = self.figure.add_subplot(111)
        # Tkinter widget
        line = FigureCanvasTkAgg(self.figure, self.top_level)
        line.get_tk_widget().grid(row=5, column=0, columnspan=2)

        if len(history) > 0:
            data = {'Date': [h[0] for h in history], 'Price (ron)': [h[1] for h in history]}
            df = DataFrame(data, columns=['Date', 'Price (ron)'])
            df = df[['Date', 'Price (ron)']].groupby('Date').sum()
            df.plot(kind='line', legend=True, ax=ax, color='r', marker='o', fontsize=10)

        ax.set_title('Price evolution')

    def set_monitoring(self):
        self.service.set_monitoring_product(self.product._id, not self.product.monitored)

    def open_browser(self, event):
        webbrowser.open_new(self.product.link)

    def set_price_labels(self):
        current_price = self.product.current_price
        current_price_str = str(current_price) + ' ron  (' + str(self.product.current_price_date.strftime(
            "%Y-%m-%d %H:%M:%S")) + ')' if current_price != -1 else 'No data record'
        self.current_price_label.config(text=current_price_str)

        lowest_price = self.product.best_price
        lowest_price_str = str(lowest_price) + ' ron  (' + str(self.product.best_price_date.strftime(
            "%Y-%m-%d %H:%M:%S")) + ')' if lowest_price != -1 else 'No data record'
        self.best_price_label.config(text=lowest_price_str)

    def update(self, data, event):
        if event == Events.MONITORING:
            if data[0] == self.product._id:
                self.product.monitored = data[1]
                self.monitor_bu.configure(text='Turn off' if self.product.monitored else 'Turn on')
                self.monitor_label.configure(
                    text='This device is being monitored' if self.product.monitored else 'This device is not being monitored')
                self.monitor_label.configure(fg='green' if self.product.monitored else 'red')
        elif event == Events.SCAN:
            if self.product.monitored:
                self.product = self.service.find_product(self.product._id)
                self.set_price_labels()
                self.set_price_plot()
        else:
            print('examine_product: update() event case not implemented')
