import tkinter as tk
import tkinter.ttk as ttk
from tkinter import StringVar
from tkinter import messagebox
import sqlite3
import os.path

listOfMovies = []
window = tk.Tk()

class Movie:
    def __init__(self, name, category, description, price):
        self.__name = name
        self.__category = category
        self.__description = description
        self.__price = price

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def getCategory(self):
        return self.__category

    def setCategory(self, category):
        self.__category = category

    def getDescription(self):
        return self.__description

    def setDescription(self, description):
        self.__description = description

    def getPrice(self):
        return self.__price

    def setPrice(self, price):
        self.__price = price

    def getPriceWithGST(self):
        return(round(self.__price*1.07, 2))


def initDatabase(Movie):
    conn = sqlite3.connect('spMovieApp.db')
    sql = "CREATE TABLE movielist(name text primary key, category text, description text, price real)"
    conn.execute(sql)

    file = open('movieList.txt', 'r')
    lines = file.readlines()
    movieLists = []

    for eachLine in lines:
        eachLine = eachLine.replace("\n", "")
        cols = eachLine.split("|")
        name = cols[0]
        category = cols[1]
        description = cols[2]
        price = float(cols[3])
        movieList = Movie(name, category, description, price)
        movieLists.append(movieList)

        sql = "INSERT INTO movielist(name,category,description,price) Values(?,?,?,?)"
        conn.execute(sql,(name, category, description, price))
        conn.commit()

    window.geometry("300x300")
    messagebox.showinfo("Success", "Database initialized!")
    file.close()
    conn.close()
    return movieLists


def insert():
    name = txtNameFilter.get()
    category = txtCategory.get()
    description = txtDescription.get()
    price = txtPrice.get()

    window.geometry("350x350")
    if name == "" or category == "" or description == "" or price == "":
        messagebox.showerror("Error", "Please key in all details!")
    else:
        conn = sqlite3.connect('spMovieApp.db')
        sql = "INSERT INTO movielist(name,category,description,price) Values(?,?,?,?)"
        conn.execute(sql, (name, category, description, price))
        messagebox.showinfo("Success", "Insert Successful!")
        conn.commit()
        conn.close()


def delete():
    global listOfMovies
    name=txtNameFilter.get().upper()

    if name != "":
        conn = sqlite3.connect('spMovieApp.db')
        sql = "DELETE FROM movielist WHERE name=?"
        conn.execute(sql,(name,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Delete Successful!")
    else:
        messagebox.showerror("Error", "Delete not successful!")
    
    
if not os.path.exists('spMovieApp.db'):
    listOfMovies=initDatabase(Movie)

# Main GUI

window.title("SP Movie Admin")
window.geometry("325x325")
window.resizable(0, 0)
window.configure(background='lavender')  

labelAppName = ttk.Label(window, text="SP Movie Admin", padding=2)
labelAppName.config(font=("Helvetica", 20))
labelAppName.grid(row=0, column=0, columnspan=3, pady=10)

labelName = ttk.Label(window, text="Name", padding=2)
labelName.grid(row=1, column=0, sticky=tk.W)
txtNameFilter = StringVar()
textName = ttk.Entry(window, textvariable=txtNameFilter)
textName.grid(row=1, column=1, pady=2)

labelCategory = ttk.Label(window, text="Category", padding=2)
labelCategory.grid(row=2, column=0, sticky=tk.W)
txtCategory = StringVar()
textCategory = ttk.Entry(window, textvariable=txtCategory)
textCategory.grid(row=2, column=1, pady=2)

labelDescription = ttk.Label(window, text="Description", padding=2)
labelDescription.grid(row=3, column=0, sticky=tk.W)
txtDescription = StringVar()
textDescription = ttk.Entry(window, textvariable=txtDescription)
textDescription.grid(row=3, column=1, pady=2)

labelPrice = ttk.Label(window, text="Price", padding=2)
labelPrice.grid(row=4, column=0, sticky=tk.W)
txtPrice = StringVar()
textPrice = ttk.Entry(window, textvariable=txtPrice)
textPrice.grid(row=4, column=1, pady=2)

button1 = ttk.Button(window, text="Insert", command=insert)
button1.grid(row=5, column=1, sticky=tk.W, pady=10)

button2 = ttk.Button(window, text="Delete", command=delete)
button2.grid(row=5, column=1, sticky=tk.E, pady=10)

window.mainloop()  # main loop to wait for events
