# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

from app.similarity import TextSimilarity

MODE_LIST = [
    "TF",
    "TF-IDF",
    "Levenshtein",
    "TF-IDF + Levenshtein"
]


class MyGUI(tkinter.Frame):

    def __init__(self):
        tkinter.Frame.__init__(self)
        self.pack()
        self.text_a = tkinter.Text(self)
        self.text_a.grid()
        self.text_b = tkinter.Text(self)
        self.text_b.grid()
        self.select_mode = ttk.Combobox(self, value=MODE_LIST)
        self.select_mode.current(0)
        self.select_mode.grid()
        self.button = tkinter.Button(self, text="compare", command=self.compare_text)
        self.button.grid()
        self.result_label = tkinter.Label(self, text="result: ")
        self.result_label.grid()

    def compare_text(self):
        similarity_float = 0.0
        current_mode = self.select_mode.get()
        if current_mode in {"TF", "TF-IDF", "Levenshtein"}:
            similarity_float = TextSimilarity(
                self.text_a.get("1.0", "end"),
                self.text_b.get("1.0", "end")
            ).similarity(current_mode)
        elif self.select_mode.get() == "TF-IDF + Levenshtein":
            similarity_float = TextSimilarity(
                self.text_a.get("1.0", "end"),
                self.text_b.get("1.0", "end")
            ).similarity_for_weight(
                {
                    "TF-IDF": 99,
                    "Levenshtein": 1
                }
            )
        label_text = "result: {}%".format(round(similarity_float * 100, 4))
        return self.result_label.configure(text=label_text)


my_gui = MyGUI()
my_gui.master.title('文档比对')
my_gui.mainloop()
