import os
import tkinter as tk
from tkinter import ttk
import pandas as pd
from PIL import ImageTk, Image
from DataFrameHandler import DataFrameHandler
from config import *


class RankCheckerGUI:

    def __init__(self):

        self.counter = 0
        self.selected_no = ""
        self.selected_query = ""

        self.base = tk.Tk()
        self.domain_label = tk.Label(self.base)
        self.lang_label = tk.Label(self.base)
        self.tree = ttk.Treeview(self.base)
        self.query_entry = tk.Entry(self.base)

        self.window = None
        self.domain_entry = None
        self.lang = None

    def main_window(self):

        self.base.title("RankChecker")
        self.base.geometry("800x800")

        # Settings Button
        setting_button = tk.Button(
            master=self.base,
            text="Settings",
            width=15,
            bg="lightblue",
            command=self.setting_window
        )

        setting_button.pack()

        settings = load_obj()

        # Label
        self.domain_label["text"] = "Domain【" + settings["domain"] + "】"
        self.domain_label.pack()

        self.lang_label["text"] = "Search Engine Language【" + settings["lang"] + "】"
        self.lang_label.pack()

        # Query Textbox
        self.query_entry.pack()

        # Add Button
        add_button = tk.Button(
            master=self.base,
            text="Add",
            width=15,
            bg="lightblue",
            command=self.add_click
        )
        add_button.pack()

        # Delete Button
        delete_button = tk.Button(
            master=self.base,
            text="Delete",
            width=15,
            bg="lightblue",
            command=self.delete_click
        )
        delete_button.pack()

        # Update Button
        update_button = tk.Button(
            master=self.base,
            text="Update",
            width=15,
            bg="lightblue",
            command=self.update_click
        )
        update_button.pack()

        # TreeView
        # Making Columns
        self.tree["column"] = (1, 2, 3, 4, 5, 6, 7)
        self.tree["show"] = "headings"

        # Header Text
        self.tree.heading(1, text="No.")
        self.tree.heading(2, text="Search Word")
        self.tree.heading(3, text="Ranking")
        self.tree.heading(4, text="Previous")
        self.tree.heading(5, text="Difference")
        self.tree.heading(6, text="Domain")
        self.tree.heading(7, text="Time")

        # columns width
        self.tree.column(1, width=10)
        self.tree.column(2, width=100)
        self.tree.column(3, width=10)
        self.tree.column(4, width=10)
        self.tree.column(5, width=50)
        self.tree.column(6, width=50)
        self.tree.column(7, width=50)

        # Double Click
        # self.tree.bind("<Double-1>", self.on_double_click)

        # TreeView Select
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Pack TreeView
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.load_pkl_insert_treeview()

        self.base.mainloop()

    def update_label(self):

        settings = load_obj()

        self.domain_label["text"] = "Domain【" + settings["domain"] + "】"
        self.lang_label["text"] = "Search Engine Language【" + settings["lang"] + "】"

    def on_tree_select(self, event):

        for item in self.tree.selection():
            row = self.tree.item(item, "values")
            print(row)
            self.selected_no = int(row[0])
            self.selected_query = row[1]

    def on_double_click(self, event):

        item = self.tree.identify('item', event.x, event.y)
        row = self.tree.item(item, "values")

        self.selected_no = int(row[0])
        self.selected_query = row[1]

    def load_pkl_insert_treeview(self):

        if not os.path.exists(RANKINGS_FILE):
            return

        df = pd.read_pickle(RANKINGS_FILE)

        if df.empty:
            return

        for i in df.index:
            diff = df.loc[i, "Diff"]

            color = ""
            if diff is None:
                pass
            elif isinstance(diff, str):
                pass
            elif diff > 0:
                color = "green"
            elif diff < 0:
                color = "red"

            self.tree.insert("", "end", values=(i, df['SearchTerm'][i], df['Ranking'][i], df['Pre'][i], df['Diff'][i],
                                                df['TargetSite'][i], df['Date'][i]), tags=color)

        self.tree.tag_configure("red", foreground='red')
        self.tree.tag_configure("green", foreground='green')

    def add_click(self):

        query = self.query_entry.get()

        handler = DataFrameHandler(query)

        if not os.path.exists(RANKINGS_FILE):
            print("This is the 1st Search")
            handler.create()
        else:
            handler.add()

        self.query_entry.delete(0, 'end')

        self.refresh()

    def delete_click(self):

        handler = DataFrameHandler()
        handler.delete(self.selected_no)

        self.refresh()

    def update_click(self):

        handler = DataFrameHandler(self.selected_query)
        handler.update(self.selected_no)

        self.refresh()

    def refresh(self):

        for i in self.tree.get_children():
            self.tree.delete(i)

        self.load_pkl_insert_treeview()

    def setting_window(self):

        self.counter += 1

        self.window = tk.Toplevel(self.base)
        self.window.wm_title("RankChecker")

        load = Image.open(IMAGE_PATH)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self.window, image=render)
        img.image = render
        img.pack()

        label = tk.Label(self.window, text="Please input domain to search.(ex:myblog.com)")
        label.pack()

        self.domain_entry = tk.Entry(self.window)
        self.domain_entry.pack()

        label = tk.Label(self.window, text="Please select search engine language.")
        label.pack()

        self.lang = tk.StringVar()
        r1 = tk.Radiobutton(self.window, text='Japanese', variable=self.lang, value='jp')
        r1.pack()
        r2 = tk.Radiobutton(self.window, text='English', variable=self.lang, value='en')
        r2.pack()

        # Domain Register Button
        button = tk.Button(
            master=self.window,
            text="Register",
            width=15,
            bg="lightblue",
            command=self.register_setting
        )

        button.pack()

    def register_setting(self):

        lang = self.lang.get()
        domain = self.query_entry.get()

        setting = {
            "lang": lang,
            "domain": domain
        }

        save_obj(setting)

        self.window.destroy()

        self.update_label()
