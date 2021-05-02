# -*- coding: utf-8 -*-

from typing import Callable
import tkinter


class MyGUI(tkinter.Frame):

    def __init__(self, compare_func: Callable = None):
        assert compare_func is not None, "must provide a compare func"
        self.compare_func = compare_func
        tkinter.Frame.__init__(self)
        self.pack()
        self.text_a = tkinter.Text(self)
        self.text_a.grid()
        self.text_b = tkinter.Text(self)
        self.text_b.grid()
        self.button = tkinter.Button(self, text="compare", command=self.compare_text)
        self.button.grid()
        self.result_label = tkinter.Label(self, text="result: ")
        self.result_label.grid()
        # self.button.

    def compare_text(self):
        text_a = self.text_a.get("1.0", "end")
        text_b = self.text_b.get("1.0", "end")
        result = self.compare_func(text_a, text_b)
        label_text = "result: {}%".format(result * 100)
        return self.result_label.setvar(value=label_text)


def compare(text_a: str, text_b: str) -> float:
    print(text_a)
    print(text_b)
    print("...")
    return 0.85


my_gui = MyGUI(compare)
my_gui.master.title('文档比对')
my_gui.mainloop()
