import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkmacosx import Button

class DeforestationApplication:
    def __init__(self) -> None:
        # Main window
        self.window = tk.Tk()
        #self.window.geometry('1920x1080')
        self.window.attributes('-fullscreen', True)
        #self.window.resizable(False, False)
        self.window.configure(bg="#FFF9F7")
        self.window.title('Deforestation Detection')

        style = ttk.Style()
        style.configure('TFrame', background='white')

        # Navigation bar
        self.nav_bar = ttk.Frame(self.window, height=70, relief=tk.FLAT)
        #self.nav_bar.propagate(True)
        self.InitNavBar()
        self.nav_bar.grid(column=0, row=0, columnspan=3, sticky="nsew")
        self.nav_bar.grid_rowconfigure(0, weight=1)
        self.nav_bar.grid_columnconfigure(0, weight=1)
        self.nav_bar.grid_columnconfigure(1, weight=1)
        self.nav_bar.grid_columnconfigure(2, weight=1)

        # Introduction page
        self.intro_frame = ttk.Frame(self.window, relief=tk.FLAT)
        #self.intro_frame.propagate(False)
        #self.intro_frame.grid_propagate(False)
        self.InitIntroPage()
        self.intro_frame.grid(column=0, row=1, sticky="nsew")
        self.intro_frame.grid_rowconfigure(0, weight=1)
        self.intro_frame.grid_columnconfigure(0, weight=1)
        self.intro_frame.grid_columnconfigure(1, weight=1)
        
        
        # Data insertion page
        self.data_insertion_frame = ttk.Frame(self.window, relief=tk.FLAT)
        #self.data_insertion_frame.propagate(False)
        #self.data_insertion_frame.grid_propagate(False)
        self.InitDataInsertionPage()
        self.data_insertion_frame.grid(column=0, row=1, sticky="nsew")

        # Results page
        self.results_frame = ttk.Frame(self.window, relief=tk.FLAT)
        #self.results_frame.propagate(False)
        #self.results_frame.grid_propagate(False)
        self.InitResultsPage()
        self.results_frame.grid(column=0, row=1, sticky="nsew")

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # Start application
        self.intro_frame.tkraise()
        self.window.mainloop()
    
    def ShowFrame(self, frame):
        frame.tkraise()

    def InitNavBar(self):
        # Colors
        background_color = '#00DF51'
        active_background_color = '#42FF87'
        foreground_color = '#000000'
        active_foreground_color = '#000000'
        highlight_color = '#5BFF9E'

        # Intro button
        intro_button = Button(self.nav_bar, 
                                   text='Introduction', 
                                   #width=565, 
                                   height=70, 
                                   relief='solid',
                                   borderless=1,
                                   command=lambda: self.ShowFrame(self.intro_frame))
        intro_button.config(font=('Arial', 20, 'bold'))
        intro_button.config(bg=background_color)
        intro_button.config(fg=foreground_color)
        intro_button.config(activebackground=active_background_color)
        intro_button.config(activeforeground=active_foreground_color)
        intro_button.config(highlightbackground=background_color)
        intro_button.config(highlightcolor=highlight_color)
        intro_button.grid(column=0, row=0, sticky="ew", padx=(10,10), pady=(5, 5))

        # Data button
        data_insertion_button = Button(self.nav_bar, 
                                    text='Data Insertion', 
                                    #width=565, 
                                    height=70, 
                                    relief='solid',
                                    borderless=1,
                                    command=lambda: self.ShowFrame(self.data_insertion_frame))
        data_insertion_button.config(font=('Arial', 20, 'bold'))
        data_insertion_button.config(bg=background_color)
        data_insertion_button.config(fg=foreground_color)
        data_insertion_button.config(activebackground=active_background_color)
        data_insertion_button.config(activeforeground=active_foreground_color)
        data_insertion_button.grid(column=1, row=0, sticky="ew", padx=(10,10), pady=(5, 5))

        # Results button
        results_button = Button(self.nav_bar, 
                                    text='Results', 
                                    #width=565, 
                                    height=70, 
                                    relief='solid',
                                    borderless=1,
                                    command=lambda: self.ShowFrame(self.results_frame))
        results_button.config(font=('Arial', 20, 'bold'))
        results_button.config(bg=background_color)
        results_button.config(fg=foreground_color)
        results_button.config(activebackground=active_background_color)
        results_button.config(activeforeground=active_foreground_color)
        results_button.grid(column=2, row=0, sticky="ew", padx=(10,10), pady=(5, 5))



    def InitIntroPage(self):
        # Side menu frame
        side_menu = ttk.Frame(self.intro_frame, relief=tk.FLAT)
        side_menu.grid_columnconfigure(0, weight=1)
        side_menu.grid_rowconfigure(0, weight=1)
        side_menu.grid_rowconfigure(1, weight=1)
        side_menu.grid_rowconfigure(2, weight=1)
        side_menu.grid_rowconfigure(3, weight=1)
        #side_menu.propagate(False)
        side_menu.grid(column=0, row=0, sticky="nsew")

        # Colors
        background_color = '#D9DBDA'
        active_background_color = '#F6F6F6'
        foreground_color = '#000000'
        active_foreground_color = '#000000'
        highlight_color = '#5BFF9E'

        # Side menu buttons
        tool_usage_button = Button(side_menu, 
                                   text='How to use the tool', 
                                   #width=420, 
                                   height=70, 
                                   relief='solid',
                                   borderless=1)
        tool_usage_button.config(font=('Arial', 20, 'bold'))
        tool_usage_button.config(bg=background_color)
        tool_usage_button.config(fg=foreground_color)
        tool_usage_button.config(activebackground=active_background_color)
        tool_usage_button.config(activeforeground=active_foreground_color)
        tool_usage_button.config(highlightbackground=background_color)
        tool_usage_button.config(highlightcolor=highlight_color)
        tool_usage_button.grid(column=0, row=0, sticky="ew", padx=(10,10), pady=(10, 20))

        # # Data button
        algo_button = Button(side_menu, 
                                   text='Algorithm description', 
                                   #width=420, 
                                   height=70, 
                                   relief='solid',
                                   borderless=1)
        algo_button.config(font=('Arial', 20, 'bold'))
        algo_button.config(bg=background_color)
        algo_button.config(fg=foreground_color)
        algo_button.config(activebackground=active_background_color)
        algo_button.config(activeforeground=active_foreground_color)
        algo_button.config(highlightbackground=background_color)
        algo_button.config(highlightcolor=highlight_color)
        algo_button.grid(column=0, row=1, sticky="ew", padx=(10,10), pady=(0, 20))

        # # Results button
        about_button = Button(side_menu, 
                                   text='About', 
                                   #width=420, 
                                   height=70, 
                                   relief='solid',
                                   borderless=1)
        about_button.config(font=('Arial', 20, 'bold'))
        about_button.config(bg=background_color)
        about_button.config(fg=foreground_color)
        about_button.config(activebackground=active_background_color)
        about_button.config(activeforeground=active_foreground_color)
        about_button.config(highlightbackground=background_color)
        about_button.config(highlightcolor=highlight_color)
        about_button.grid(column=0, row=2, sticky="ew", padx=(10,10), pady=(0, 20))

        exit_button = Button(side_menu, 
                                   text='Exit', 
                                   #width=420, 
                                   height=70, 
                                   relief='solid',
                                   borderless=1)
        exit_button.config(font=('Arial', 20, 'bold'))
        exit_button.config(bg=background_color)
        exit_button.config(fg=foreground_color)
        exit_button.config(activebackground=active_background_color)
        exit_button.config(activeforeground=active_foreground_color)
        exit_button.config(highlightbackground=background_color)
        exit_button.config(highlightcolor=highlight_color)
        exit_button.grid(column=0, row=3, sticky="ew", padx=(10,10), pady=(10, 10))

        # Text information on the right
        text_info = tk.Text(self.intro_frame, 
                            wrap='word', 
                            font=('Arial', 14), 
                            state='disabled', 
                            bg="lightgrey",
                            #width=1420,
                            #height=970)
        )
        text_info.insert("end", "This is editable text.\n", "normal")
        text_info.grid(column=1, row=0, sticky='nsew', padx=(10,10), pady=(10, 10))

    def InitDataInsertionPage(self):
        pass

    def InitResultsPage(self):
        pass

    def plot_on_frame(frame):
        # Create a sample plot
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3, 4], [1, 4, 2, 3])

        # Create a FigureCanvasTkAgg instance
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()

        # Pack the canvas into the frame
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    






