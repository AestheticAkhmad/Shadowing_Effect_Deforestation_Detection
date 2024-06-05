import tkinter as tk
import time
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

from tkmacosx import Button

from DataHolder import DataHolder
from InputValidator import InputValidator
from AlgorithmExecutor import AlgorithmExecutor

# test plotting
from PIL import Image, ImageTk

class DeforestationApplication:
    def __init__(self) -> None:
        # Main window
        self.window = tk.Tk()
        self.window.geometry('1280x720')
        self.window.configure(bg="#FFF9F7")
        self.window.title('Deforestation Detection')
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # Main frame
        self.main_frame = tk.Frame(self.window, relief=tk.FLAT)
        self.main_frame.pack(anchor='center', fill='both', expand=True)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # All entries
        self.entries = list()

        # Navigation bar
        self.nav_bar = tk.Frame(self.main_frame, height=70, relief=tk.FLAT)
        self.nav_bar.grid(column=0, row=0, columnspan=3, sticky="new")
        self.nav_bar.grid_rowconfigure(0, weight=1)
        self.nav_bar.grid_columnconfigure(0, weight=1)
        self.nav_bar.grid_columnconfigure(1, weight=1)
        self.nav_bar.grid_columnconfigure(2, weight=1)
        self.InitNavBar()

        # Introduction page
        self.intro_frame = tk.Frame(self.main_frame, relief=tk.FLAT)
        self.intro_frame.grid(column=0, row=1, sticky="nsew")
        self.intro_frame.grid_rowconfigure(0, weight=1)
        self.intro_frame.grid_columnconfigure(1, weight=1)
        self.InitIntroPage()
        
        
        # Data insertion page
        self.data_insertion_frame = tk.Frame(self.main_frame, relief=tk.FLAT)
        self.data_insertion_frame.grid(column=0, row=1, sticky="nsew")
        self.data_insertion_frame.grid_rowconfigure(0, weight=1)
        self.data_insertion_frame.grid_columnconfigure(0, weight=0)
        self.data_insertion_frame.grid_columnconfigure(1, weight=0)
        self.data_insertion_frame.grid_columnconfigure(2, weight=1)
        self.InitDataInsertionPage()

        # Results page
        self.results_frame = tk.Frame(self.main_frame, relief=tk.FLAT)
        self.image_canvas = None
        self.results_frame.grid(column=0, row=1, sticky="nsew")
        self.results_frame.grid_rowconfigure(0, weight=1)
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_columnconfigure(1, weight=0)
        self.InitResultsPage()

        # Validator variables
        self.can_validate = True

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
                                   text='Main Menu', 
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
        intro_button.grid(column=0, row=0, sticky="new", padx=(10,10), pady=(5, 5))

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
        data_insertion_button.grid(column=1, row=0, sticky="new", padx=(10,10), pady=(5, 5))

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
        results_button.grid(column=2, row=0, sticky="new", padx=(10,10), pady=(5, 5))

    def InitIntroPage(self):
        # Side menu frame
        side_menu = tk.Frame(self.intro_frame, width=250, relief=tk.FLAT)
        side_menu.grid_columnconfigure(0, weight=1)
        side_menu.grid_rowconfigure(0, weight=0)
        side_menu.grid_rowconfigure(1, weight=0)
        side_menu.grid_rowconfigure(2, weight=0)
        side_menu.grid_rowconfigure(3, weight=1)
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
                                   #width=230, 
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
        tool_usage_button.grid(column=0, row=0, sticky="new", padx=(10,10), pady=(5, 5))

        # # Data button
        algo_button = Button(side_menu, 
                                   text='Algorithm description', 
                                   #width=230, 
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
        algo_button.grid(column=0, row=1, sticky="new", padx=(10,10), pady=(5, 5))

        # # Results button
        about_button = Button(side_menu, 
                                   text='About', 
                                   #width=230, 
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
        about_button.grid(column=0, row=2, sticky="new", padx=(10,10), pady=(5, 5))

        exit_button = Button(side_menu, 
                                   text='Exit', 
                                   #width=230, 
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
        exit_button.grid(column=0, row=3, sticky="sew", padx=(10,10), pady=(10, 5))

        # Text information on the right
        text_info = tk.Label(self.intro_frame, 
                                    font=('Arial', 28), 
                                    bg="lightgrey",
                                    anchor='nw',
                                    fg='#333d36',
                                    justify='left'
        )

        info = "To use this tool, follow these instructions:\n"
        info += "1. Click the 'Data Insertion' button on the top middle.\n"
        info += "2. Enter the dates you want to detect deforestation on.\n"
        info += "3. Enter the region of interest.\n"
        info += "4. Press 'Start' button to execute the algorithm.\n"
        info += "5. After the console states that results are redy, press 'Results' button.\n\n"
        info += "The plot is automaticall saved on your machine in folder 'data'\n"

        text_info.config(text=info)

        text_info.grid(column=1, row=0, sticky='nsew', padx=(10,10), pady=(5, 5))

    def InitDataInsertionPage(self):
        # Dates column (left side)
        self.InitDataInsertionPageFirstColumn()

        # ROI column (middle)
        self.InitDataInsertionPageSecondColumn()

        # Console column (right side)
        self.InitDataInsertionPageThirdColumn()
    
    def resize_canvas(self, event):
        self.canvas_width = event.width
        self.canvas_height = event.height
        self.canvas.config(width=self.canvas_width, height=self.canvas_height)

    def InitResultsPage(self):
        # Left column
        left_frame = tk.Frame(self.results_frame, relief=tk.FLAT)
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(10,10), pady=(10,10))

        image_label = tk.Label(left_frame, 
                        text="Deforestation detection plot:",
                        font=('Arial', 20, 'bold'))
        image_label.grid(column=0, row=0, sticky="new", padx=(10,10), pady=(10,10))
        
        # Creating canvas for the result images
        self.image_frame = tk.Frame(left_frame, relief=tk.SUNKEN)
        self.image_frame.grid(row=1, column=0, sticky='nsew', padx=(10, 10), pady=(10,10))
        self.image_frame.grid_columnconfigure(0, weight=1)  
        self.image_frame.grid_rowconfigure(0, weight=1)

        # Canvas
        self.canvas = tk.Canvas(self.image_frame, width=800, height=600)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Create vertical and horizontal scrollbars
        v_scrollbar = tk.Scrollbar(self.image_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = tk.Scrollbar(self.image_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.config(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.canvas.bind("<Configure>", self.resize_canvas)

        # Grid the scrollbars to the frame
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

                
        # Right column
        right_frame = tk.Frame(self.results_frame, width=450, relief=tk.FLAT)
        right_frame.grid(row=0, column=1, sticky='nsew')
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=0)
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_propagate(False)

        info_label = tk.Label(right_frame, 
                            text="Results:",
                            font=('Arial', 20, 'bold'))
        info_label.grid(column=0, row=0, sticky="new", padx=(10,10), pady=(10,10))

        self.results_info = tk.Label(right_frame, 
                font=('Courier', 24, 'bold'), 
                bg="lightgrey",
                anchor='nw',
                fg='#7d0000',
                justify='left'
        )

        self.results_info.grid(column=0, row=1, sticky='nsew', padx=(10,10), pady=(10, 10))

    def InitDataInsertionPageThirdColumn(self):
        # 2nd column frame
        console_frame = tk.Frame(self.data_insertion_frame, relief=tk.FLAT)
        console_frame.grid_columnconfigure(0, weight=1)
        console_frame.grid_rowconfigure(0, weight=0)
        console_frame.grid_rowconfigure(1, weight=1)
        console_frame.grid(column=2, row=0, sticky='nsew')

        info_label = tk.Label(console_frame, 
                               text="Algorithm progress info:",
                               font=('Arial', 20, 'bold'))
        info_label.grid(column=0, row=0, sticky="new", padx=(10,10), pady=(10,10))

        self.info_var = tk.StringVar()
        self.console_info = tk.Label(console_frame, 
                        font=('Courier', 24), 
                        bg="lightgrey",
                        anchor='nw',
                        fg='#7d0000',
                        justify='left'
        )

        self.console_info.grid(column=0, row=1, sticky='nsew', padx=(10,10), pady=(10, 10))

    def InitDataInsertionPageSecondColumn(self):
        # 2nd column frame
        roi_frame = tk.Frame(self.data_insertion_frame, width=400, relief=tk.FLAT)
        roi_frame.grid(column=1, row=0, sticky="ns")
        roi_frame.grid_columnconfigure(0, weight=1)
        roi_frame.grid_rowconfigure(0, weight=0)
        roi_frame.grid_rowconfigure(1, weight=0)
        roi_frame.grid_rowconfigure(2, weight=0)
        roi_frame.grid_rowconfigure(3, weight=0)
        roi_frame.grid_rowconfigure(4, weight=0)
        roi_frame.grid_rowconfigure(5, weight=1)

        roi_label = tk.Label(roi_frame, 
                               text="Enter the coordinates \nfor the region of interest:",
                               font=('Arial', 20, 'bold'))
        roi_label.grid(column=0, row=0, sticky="new", padx=(10,10), pady=(20,20))

        # West frame
        west_frame = tk.Frame(roi_frame, relief=tk.FLAT)
        west_frame.grid_columnconfigure(0, weight=1)
        west_frame.grid_columnconfigure(1, weight=1)
        west_frame.grid(column=0, row=1, sticky="new")

        west_label = tk.Label(west_frame,
                                   text="West:",
                                   font=('Arial', 18, 'bold'))
        west_label.grid(column=0, row=0, sticky="nw", padx=(10,10), pady=(20,20))
        
        west_entry = tk.Entry(west_frame,
                                   font=('Arial', 18, 'bold'),
                                   width=12)
        west_entry.grid(column=1, row=0, sticky="new", padx=(10,10), pady=(20,20))
        self.entries.append(west_entry)

        # South frame
        south_frame = tk.Frame(roi_frame, relief=tk.FLAT)
        south_frame.grid_columnconfigure(0, weight=1)
        south_frame.grid_columnconfigure(1, weight=1)
        south_frame.grid(column=0, row=2, sticky="nsew")

        south_label = tk.Label(south_frame,
                                   text="South:",
                                   font=('Arial', 18, 'bold'))
        south_label.grid(column=0, row=0, sticky="nw", padx=(10,10), pady=(20,20))
        
        south_entry = tk.Entry(south_frame,
                                   font=('Arial', 18, 'bold'),
                                   width=12)
        south_entry.grid(column=1, row=0, sticky="new", padx=(10,10), pady=(20,20))
        self.entries.append(south_entry)

        # East frame
        east_frame = tk.Frame(roi_frame, relief=tk.FLAT)
        east_frame.grid_columnconfigure(0, weight=1)
        east_frame.grid_columnconfigure(1, weight=1)
        east_frame.grid(column=0, row=3, sticky="nsew")

        east_label = tk.Label(east_frame,
                                   text="East:",
                                   font=('Arial', 18, 'bold'))
        east_label.grid(column=0, row=0, sticky="nw", padx=(10,10), pady=(20,20))
        
        east_entry = tk.Entry(east_frame,
                                   font=('Arial', 18, 'bold'),
                                   width=12)
        east_entry.grid(column=1, row=0, sticky="new", padx=(10,10), pady=(20,20))
        self.entries.append(east_entry)

        # North frame
        north_frame = tk.Frame(roi_frame, relief=tk.FLAT)
        north_frame.grid_columnconfigure(0, weight=1)
        north_frame.grid_columnconfigure(1, weight=1)
        north_frame.grid(column=0, row=4, sticky="nsew")

        north_label = tk.Label(north_frame,
                                   text="North:",
                                   font=('Arial', 18, 'bold'))
        north_label.grid(column=0, row=0, sticky="nw", padx=(10,10), pady=(20,20))
        
        north_entry = tk.Entry(north_frame,
                                   font=('Arial', 18, 'bold'),
                                   width=12)
        north_entry.grid(column=1, row=0, sticky="new", padx=(10,10), pady=(20,20))
        self.entries.append(north_entry)

        # Clear all fields Button
        # Colors
        background_color = '#F45C51'
        active_background_color = '#F46F65'
        foreground_color = '#000000'
        active_foreground_color = '#000000'
        highlight_color = '#5BFF9E'

        clear_button = Button(roi_frame, 
                                   text='Clear all fields', 
                                   width=300, 
                                   height=70, 
                                   relief='solid',
                                   borderless=1,
                                   command=self.ClearAllFields)
        clear_button.config(font=('Arial', 20, 'bold'))
        clear_button.config(bg=background_color)
        clear_button.config(fg=foreground_color)
        clear_button.config(activebackground=active_background_color)
        clear_button.config(activeforeground=active_foreground_color)
        clear_button.config(highlightbackground=background_color)
        clear_button.config(highlightcolor=highlight_color)
        clear_button.grid(column=0, row=5, sticky="sew", padx=(10,10), pady=(10, 10))

    def ClearAllFields(self):
        for entry in self.entries:
            entry.delete(0, tk.END)

    def InitDataInsertionPageFirstColumn(self):
        # 1st column frame
        dates_frame = tk.Frame(self.data_insertion_frame, width=400, relief=tk.FLAT)
        dates_frame.grid_columnconfigure(0, weight=1)
        dates_frame.grid_rowconfigure(0, weight=0)
        dates_frame.grid_rowconfigure(1, weight=0)
        dates_frame.grid_rowconfigure(2, weight=0)
        dates_frame.grid_rowconfigure(3, weight=1)

        dates_label = tk.Label(dates_frame, 
                               text="Enter the dates for which \nto observe deforestation:",
                               font=('Arial', 20, 'bold'))
        dates_label.grid(column=0, row=0, sticky="new", padx=(10,10), pady=(20,20))

        # Date from
        date_from_frame = ttk.Frame(dates_frame, relief=tk.FLAT)
        date_from_frame.grid_columnconfigure(0, weight=1)
        date_from_frame.grid_columnconfigure(1, weight=1)
        date_from_frame.grid(column=0, row=1, sticky="new")

        date_from_label = tk.Label(date_from_frame,
                                   text="Date from:\nYYYY-MM-DD",
                                   font=('Arial', 18, 'bold'))
        date_from_label.grid(column=0, row=0, sticky="w", padx=(10,10), pady=(20,20))
        
        date_from_entry = tk.Entry(date_from_frame,
                                   font=('Arial', 18, 'bold'),
                                   width=12)
        date_from_entry.grid(column=1, row=0, sticky="w", padx=(10,10), pady=(20,20))
        self.entries.append(date_from_entry)

        # Date to
        date_to_frame = tk.Frame(dates_frame, relief=tk.FLAT)
        date_to_frame.grid_columnconfigure(0, weight=1)
        date_to_frame.grid_columnconfigure(1, weight=1)
        date_to_frame.grid(column=0, row=2, sticky="nsew")

        date_to_label = tk.Label(date_to_frame,
                                   text="Date to:\nYYYY-MM-DD",
                                   font=('Arial', 18, 'bold'))
        date_to_label.grid(column=0, row=0, sticky="w", padx=(10,10), pady=(20,20))
        
        date_to_entry = tk.Entry(date_to_frame,
                                   font=('Arial', 18, 'bold'),
                                   width=12)
        date_to_entry.grid(column=1, row=0, sticky="w", padx=(10,10), pady=(20,20))
        self.entries.append(date_to_entry)

        # Start Button
        # Colors
        background_color = '#BFACD6'
        active_background_color = '#C9BCDB'
        foreground_color = '#000000'
        active_foreground_color = '#000000'
        highlight_color = '#5BFF9E'

        start_button = Button(dates_frame, 
                                   text='Start', 
                                   width=300, 
                                   height=70, 
                                   relief='solid',
                                   borderless=1,
                                   command=self.InitValidator
                                   )
        start_button.config(font=('Arial', 20, 'bold'))
        start_button.config(bg=background_color)
        start_button.config(fg=foreground_color)
        start_button.config(activebackground=active_background_color)
        start_button.config(activeforeground=active_foreground_color)
        start_button.config(highlightbackground=background_color)
        start_button.config(highlightcolor=highlight_color)
        start_button.grid(column=0, row=3, sticky="sew", padx=(10,10), pady=(10, 10))

        dates_frame.grid(column=0, row=0, sticky="nsew")
    
    def UpdateConsoleInfo(self, text):
        current_text = self.console_info.cget("text")
        updated_text = current_text + text
        self.console_info.config(text=updated_text)

    def InitAlgorithmExecutor(self):
        alg_ex = AlgorithmExecutor(self.dh, "VH", "data")
        exec_time_str = ""
        total_time = None

        self.UpdateConsoleInfo('****************************************************************\n')
        # Starting downloading data
        self.UpdateConsoleInfo("-> Data collection has started.\n")
        start_time = time.time()
        exec_result = alg_ex.InitCollectData()
        exec_time = time.time() - start_time
        exec_time_str = "\t[{:.2f} seconds]\n".format(exec_time)
        total_time = exec_time
        self.UpdateConsoleInfo(exec_result + exec_time_str)
        self.UpdateConsoleInfo('****************************************************************\n')

        # Reading data
        self.UpdateConsoleInfo("-> Data reading has started.\n")
        start_time = time.time()
        exec_result = alg_ex.InitReadData()
        self.UpdateConsoleInfo(exec_result)
        exec_result = alg_ex.InitTransferData()
        exec_time = time.time() - start_time
        exec_time_str = "\t[{:.2f} seconds]\n".format(exec_time)
        total_time += exec_time
        self.UpdateConsoleInfo(exec_result + exec_time_str)

        self.UpdateConsoleInfo('****************************************************************\n')
        # Starting Shadowing Effect Algorithm
        start_time = time.time()
        self.UpdateConsoleInfo("-> Deforestation detection has started.\n")
        exec_result = alg_ex.InitDeforestationDetection()
        exec_time = time.time() - start_time
        exec_time_str = "\t[{:.2f} seconds]\n".format(exec_time)
        total_time += exec_time
        self.UpdateConsoleInfo(exec_result + exec_time_str)

        self.UpdateConsoleInfo('****************************************************************\n')
        # Plotting results
        start_time = time.time()
        self.UpdateConsoleInfo("-> Result initialization has started.\n")
        exec_result = alg_ex.InitResults(self.canvas, self.results_info)
        exec_time = time.time() - start_time
        exec_time_str = "\t[{:.2f} seconds]\n".format(exec_time)
        total_time += exec_time
        self.UpdateConsoleInfo(exec_result + exec_time_str)

        self.console_info.config(fg='blue')
        self.UpdateConsoleInfo('-> Total time taken: ' + "\t[{:.2f} seconds]\n".format(total_time))
        self.UpdateConsoleInfo('****************************************************************\n')

    def InitValidator(self):
        if not self.can_validate:
            print("cannot start algorithm yet")
            return

        # Collect inputs from fields
        date_from = self.entries[0].get()
        date_to = self.entries[1].get()
        input_roi = {'west': self.entries[2].get(), 
                    'south': self.entries[3].get(),
                    'east': self.entries[4].get(),
                    'north': self.entries[5].get()}
        
        self.dh = DataHolder()
        iv = InputValidator(self.dh)
        valid, error_msg = iv.ValidateInput(input_roi, date_from, date_to)

        self.console_info.config(text=error_msg)

        if valid:
            self.can_validate = False
            self.console_info.config(text="-> Started algorithm execution.\t[Execution time]\n")

            self.algo_thread = threading.Thread(target=self.InitAlgorithmExecutor)
            self.algo_thread.start()
            self.check_thread()

        else:
            print(error_msg)
            self.can_validate = True

    def check_thread(self):
        if self.algo_thread.is_alive():
            self.window.after(100, self.check_thread)
        else:
            print("can start algorithm")
            self.can_validate = True

