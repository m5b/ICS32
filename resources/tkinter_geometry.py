import tkinter as tk

root = tk.Tk()
root.geometry("400x400")

# tutorial!
# https://tkdocs.com/tutorial/index.html

# packing example


frm_1 = tk.Frame(master=root, height=100, width=100, background="red")
#frm_1.pack(fill=tk.Y, side=tk.LEFT)
frm_1.pack()

frm_2 = tk.Frame(master=root, height=100, width=100, background="green")
#frm_2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
frm_2.pack()

frm_3 = tk.Frame(master=root, height=100, width=100, background="blue")
#frm_3.pack(fill=tk.Y, side=tk.RIGHT)
frm_3.pack()



root.mainloop()