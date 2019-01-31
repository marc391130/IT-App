import tkinter as tk
from tkinter import filedialog as tkd
import Classes as ct
import json

t = 5

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.basket = []

    def create_widgets(self):
        self.header = tk.Label(self)
        self.header["text"] = "Vare"
        self.header.config(font=("Courier", 44))
        self.header.pack()

        self.scroll = tk.Scrollbar(self)
        self.orderList = tk.Listbox(self, yscrollcommand = self.scroll.set)
        self.orderList["width"] = 55
        self.orderList["height"] = 20

        self.basketList = tk.Listbox(self, yscrollcommand = self.scroll.set)
        self.basketList["width"] = 55
        self.basketList["height"] = 20

        self.removeFromBasketBut = tk.Button(self, text="Fjern", fg="red", command=self.deleteFromBasket)
        self.removeFromBasketBut["width"] = 10

        self.totalAmount = tk.Label(self)

        self.backToMain = tk.Button(self, text="Tilbage", fg="blue", command=self.mainMenu)
        self.backToMain["width"] = 10

        self.checkPlease = tk.Button(self, text="Kvitterring", fg="green", command=self.getCheck)
        self.checkPlease["width"] = 10

        self.viewData = tk.Text(self)
        self.viewData["width"] = 85

        file = open("data.json","r")
        orders = json.loads(file.read())
        self.rawOrders = orders["products"]
        self.orders = []

        for index in range(len(self.rawOrders)):
            entry = self.rawOrders[index]
            name = str(entry["name"])
            price = str(entry["price"])
            stars = str(entry["stars"])

            self.orders.append(ct.Order(entry["name"], entry["price"], entry["stars"]))
            self.orderList.insert(self.orderList.size(), name + " .. " + price + " kr. .. Stars: " + stars)
        
        self.orderList.pack()
        self.scroll.config(command = self.orderList.yview)

        self.addToBasketBut = tk.Button(self, text="Tilføj", fg="green", command=self.addToBasket)
        self.addToBasketBut["width"] = 10

        self.goToBasket = tk.Button(self, text="Indkøbskurv", fg="blue", command=self.basketMenu)
        self.goToBasket["width"] = 10

        self.goToViewData = tk.Button(self, text="Vis Data", command=self.viewMenu)
        self.goToViewData["width"] = 10

        self.quit = tk.Button(self, text="Afslut", fg="red", command=self.master.destroy)
        self.quit["width"] = 10

        self.mainMenu()

    def addToBasket(self):
        id = int(str(self.orderList.curselection())[1:-2])
        self.basket.append(self.orders[id])

    def deleteFromBasket(self):
        temp = []
        id = int(str(self.basketList.curselection())[1:-2])
        for line in range(len(self.basket)):
            if(line != id):
                temp.append(self.basket[line])
        
        self.basket = temp
        self.basketMenu()

    def mainMenu(self):
        self.unpackAll()

        self.header["text"] = "Varer"

        self.orderList.pack(pady=t)
        self.addToBasketBut.pack(pady=t)
        self.goToBasket.pack(pady=t)
        self.goToViewData.pack(pady=t)
        self.quit.pack(pady=t)
    
    def getAmount(self):
        total = 0
        for line in range(len(self.basket)):
            total += int(self.basket[line].getPrice())

        return str(total)

    def basketMenu(self):
        self.unpackAll()

        self.header["text"] = "Indkøbskurv"

        self.totalAmount["text"] = str("Total beløb: " + self.getAmount() + " kr")

        self.basketList.delete(0,"end")

        for line in range(len(self.basket)):
            self.basketList.insert(self.basketList.size(), str(self.basket[line].getName()) + " .. kr: " + str(self.basket[line].getPrice()))

        self.basketList.pack(pady=t)
        self.totalAmount.pack(pady=t)
        self.removeFromBasketBut.pack(pady=t)
        self.checkPlease.pack(pady=t)
        self.backToMain.pack(pady=t)

    def viewMenu(self):
        self.unpackAll()

        self.header["text"] = "Data"
        self.viewData.pack(pady=t)
        self.backToMain.pack(pady=t)

        file = open("data.json", "r")

        self.viewData.insert("end-1c", file.read())
        

    def unpackAll(self):
        self.orderList.pack_forget()
        self.addToBasketBut.pack_forget()
        self.goToBasket.pack_forget()
        self.basketList.pack_forget()
        self.backToMain.pack_forget()
        self.removeFromBasketBut.pack_forget()
        self.totalAmount.pack_forget()
        self.checkPlease.pack_forget()
        self.quit.pack_forget()
        self.viewData.pack_forget()
        self.goToViewData.pack_forget()

    def getCheck(self):
        f = tkd.asksaveasfile(mode="w", defaultextension=".txt")
        if f is None:
            return
        text2save = "Bestilte varer: \n \n"

        for line in range(len(self.basket)):
            text2save += str(self.basket[line].getName() + " .. kr: " + self.basket[line].getPrice() + " .. stars: " + self.basket[line].getStars() + "\n")

        text2save += str("\n" + "-- Totalbeløb: " + self.getAmount() + " kr")
        f.write(text2save)
        f.close()

root = tk.Tk()
root.geometry("1060x600")
app = Application(master=root)
app.mainloop()
