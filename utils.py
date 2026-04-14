import tkinter as tk


def gui_print(log_widget, text=""):
    log_widget.insert(tk.END, f"{text}\n")
    log_widget.see(tk.END)


def clearlog(log_widget):
    log_widget.delete("1.0", tk.END)


def clear_table(table):
    for row in table.get_children():
        table.delete(row)
