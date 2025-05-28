import tkinter as tk
import os
from tkinter import messagebox

path = os.getenv('temp')
filename = os.path.join(path, 'info.txt')

root = tk.Tk()
root['height'] = 400
root['width'] = 400

labelName = tk.Label(root, text='学号', justify=tk.RIGHT, anchor='e', width=80)
labelName.place(x=20, y=20, width=60, height=20)

varName = tk.StringVar(root, value='')
entryName = tk.Entry(root, width=80, textvariable=varName)
entryName.place(x=100, y=20, width=150, height=20)

labelTel = tk.Label(root, text='姓名', justify=tk.RIGHT, anchor='e', width=80)
labelTel.place(x=20, y=50, width=60, height=20)

varTel = tk.StringVar(root, value='')
entryTel = tk.Entry(root, width=80, textvariable=varTel)
entryTel.place(x=100, y=50, width=150, height=20)

def add_contact():
    num = entryName.get()
    name = entryTel.get()
    contact_info = f'学号：{num}，姓名：{name}'
    listbox_contacts.insert(tk.END, contact_info)

def save_contacts():
    with open(filename, 'w') as fp:
        for i in range(listbox_contacts.size()):
            fp.write(listbox_contacts.get(i) + '\n')

def delete_contacts():
    selection = listbox_contacts.curselection()
    if selection:
        listbox_contacts.delete(selection[0])

def check_contacts():
    student_id = varName.get().strip()
    found = False
    for i in range(listbox_contacts.size()):
        if student_id in listbox_contacts.get(i):
            listbox_contacts.selection_clear(0, tk.END)
            listbox_contacts.selection_set(i)
            listbox_contacts.see(i)
            found = True
            break
    if not found:
        messagebox.showinfo("E")

buttonAdd = tk.Button(root, text='add', command=add_contact)
buttonAdd.place(x=20, y=120, width=80, height=30)

buttonSave = tk.Button(root, text='save', command=save_contacts)
buttonSave.place(x=110, y=120, width=80, height=30)

buttonDelete = tk.Button(root, text='delete', command=delete_contacts)
buttonDelete.place(x=200, y=120, width=80, height=30)

buttonCheck = tk.Button(root, text='check', command=check_contacts)
buttonCheck.place(x=290, y=120, width=80, height=30)

listbox_contacts = tk.Listbox(root)
listbox_contacts.place(x=20, y=160, width=350, height=100)

label_info = tk.Label(root, text='', justify=tk.LEFT, anchor='w', width=180)
label_info.place(x=20, y=350, width=350, height=20)

def show_contact(event):
    selection = listbox_contacts.curselection()
    if selection:
        selected_contact = listbox_contacts.get(selection[0])
        label_info.config(text=selected_contact)

listbox_contacts.bind('<<ListboxSelect>>', show_contact)

if __name__ == "__main__":
    root.mainloop()