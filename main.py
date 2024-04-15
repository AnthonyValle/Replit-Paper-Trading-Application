import tkinter as tk
from tkinter import *
from tkinter import messagebox

import os
import time
import requests
import threading
from bs4 import BeautifulSoup



'''VARIABLES'''
COLOR = '#404040'
WHITE = 'white'
FONT = ('Times New Roman', 12)
FONT1 = ('Times New Roman', 10)
FONT2 = ('Times New Roman', 7)

balance = 10000000

objects = {
  # name : marketPrice
}
urls = {
  # name : url
}
portfolio = {
  # index : [name, buyPrice, Quantity]
}
activityLog = {
  # index : [action(buy/sell), quantity, (buy/sell) price, total value]
}


'''FUNCTIONS'''
def priceScrape(url):
  print('Scraping ...')
  response = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'})
  time.sleep(1)
  soup = BeautifulSoup(response.text, 'html.parser')
  price = soup.find('div', class_='YMlKec fxKbKc').text
  price = price.replace(',', '')
  price = price.replace('$', '')
  return float(price)

def nameScrape(url):
  response = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'})
  time.sleep(1)
  soup = BeautifulSoup(response.text, 'html.parser')
  name = soup.find('div', class_='zzDege').text
  return name

def scrape():
  os.system('clear')
  global objects
  print('Scraping ...')
  for i in urls:
    objects[i] = priceScrape(urls[i])


def buy():
  global balance

  if len(list(objects)) == 0:
    messagebox.showinfo('No Tickers', 'Add a ticker!')
  else:
    os.system('clear')
    global balance
  
    try:
      string = marketListBox.get(marketListBox.curselection())
    except:
      print('ERROR - Must be selecting an object in the list box')
      return
  
    name = string
    price = priceScrape(urls[name])

    print(f'{name} @ {price}')
  
    choice = input('Choose a quantity>>>')
  
    try:
      choice = int(choice)
    except:
        print('ERROR - Must type an integer')
        return
  
    buyPrice = choice * price

    if buyPrice > balance:
      print('Error - Not enough cash')
    else:
      balance -= buyPrice
      balance = round(float(balance), 2)
      balanceLabel.configure(text=f'Balance\n{balance}')
      
      portfolio[len(list(portfolio))+1] = [name, price, choice]
  
      activityLog[len(list(activityLog))+1] = ['buy', choice, price, buyPrice]
  
      string = f'{choice} x {name} @ {price}'
  
      positionsListBox.insert(0, string)


    
    

def sell():
  global balance
  os.system('clear')

  try:
    elementIndex = positionsListBox.curselection()[0]
    string = positionsListBox.get(positionsListBox.curselection())
  except:
      print('ERROR - Must be selecting an object in the list box')
      return

  quantity = int(string.split(' x ')[0])
  name = string.split(' @ ')[0].split(' x ')[1]
  buyPrice = float(string.split(' @ ')[-1])

  sellPrice = priceScrape(urls[name])

  print('How much would you like to sell?')
  print(f'Max - {quantity}')
  try:
    choice = int(input('>>>'))
  except:
    print('ERROR - Must type an Integer')
    return
    
  if choice > quantity:
    print('ERROR - Qunatity too high')
  else:
    gain = sellPrice * choice

    balance += gain
    balance = round(float(balance), 2)
    balanceLabel.configure(text=f'Balance\n{balance}')
    

    val = [name, buyPrice, quantity]

    index = list(portfolio.keys())[list(portfolio.values()).index(val)]

    quantLeft = quantity - choice
    
    if quantLeft != 0:
      portfolio[index] = [name, buyPrice, quantLeft]
      positionsListBox.delete(elementIndex)
      newString = f'{quantLeft} x {name} @ {buyPrice}'
      positionsListBox.insert(0, newString)
    else:
      del portfolio[index]
      positionsListBox.delete(elementIndex)

    activityLog[len(list(activityLog))+1] = ['sell', choice, sellPrice, gain]

      
          

        


   

def winLoss():
  os.system('clear')
  if len(list(portfolio)) == 0:
    print('There is nothing in your portfolio')
    time.sleep(1)
  else:
    scrape()
    while True:
      os.system('clear')
      for i in portfolio:
        name = portfolio[i][0]
        quantity = portfolio[i][2]
        buyPrice = portfolio[i][1]
        marketValue = objects[name]
        myValue = quantity * buyPrice
        sellValue = quantity * marketValue
        winLoss = round((sellValue-myValue), 2)
        print(f'{i} - {quantity} X {name} | W/L - {winLoss}')
        print(f'My Value - {myValue} | Sell Value - {sellValue}\n')


      print('Put Q/q to quit')
      print('\n')
      choice = input('Choose >>>')
      if choice == 'q' or choice == 'Q':
        break
      else:
        print('ERROR - Invalid input')
        time.sleep(1)


def activityLogFunc():
  os.system('clear')
  if len(list(activityLog)) == 0:
    print('There is nothing in your activity log')
    time.sleep(1)
  else:
    while True:
      for activity in activityLog:
        print(f'{activity} - {activityLog[activity]}\n')

      print('Put Q/q to quit')
      print('\n')
      choice = input('Choose >>>')
      if choice == 'q' or choice == 'Q':
        break
      else:
        print('ERROR - Invalid input')
        time.sleep(1)

def addTicker():
  os.system('clear')
  print('This application uses Google Finance (https://www.google.com/finance/?hl=en) as the main source of live asset prices')
  print('\n')
  print('Paste the URL of your asset onto the console and press ENTER/RETURN')
  print('\n')
  print('Put Q/q to quit')
  print('\n')
  choice = input('Choose >>>')

  if choice == 'Q' or choice == 'q':
    pass
  else:
    try:
      response = requests.get(choice)

      if response.status_code == 200:
        try:
          name = nameScrape(choice)
          price = priceScrape(choice)
          objects[name] = price
          urls[name] = choice
          
          string = f'{name}'
          
          marketListBox.insert(0, string)
                
        except:
          print('ERROR - URL most likely invalid, try again')
      else:
        print('ERROR - URL most likely invalid, try again')
      time.sleep(1)
    except:
      print('ERROR - Invalid Input')
      time.sleep(1)

def changeBalance():
  os.system('clear')
  global balance
  try:
    choice = float(input("To what would you like to change your balance too? >>>"))
  except:
    print('ERROR - Must type a number')
    return
  balance = round(float(choice), 2)
  balanceLabel.configure(text=f'Balance\n{balance}')


def remove():
  selection = marketListBox.curselection()
  marketListBox.delete(selection)


def bgColor():
  color = bgColorEntry.get()
  try:
    ant.configure(bg=color)
    marketLabel.configure(bg=color)
    positionLabel.configure(bg=color)
    balanceLabel.configure(bg=color)
    spaceHolder1.configure(bg=color)
    spaceHolder2.configure(bg=color)
    spaceHolder3.configure(bg=color)
    
    return
  except:
    print('ERROR - Color not identified')
    return

def fgColor():
  color = fgColorEntry.get()
  try:
    marketLabel.configure(fg=color)
    positionLabel.configure(fg=color)
    balanceLabel.configure(fg=color)
    return
  except:
    print('ERROR - Color not identified')
    return



'''TKINTER STUFF'''
ant = tk.Tk()
ant.title('Ant Trade')
ant.geometry('550x400')
ant.config(bg=COLOR)

ant.columnconfigure(0, weight=2)
ant.columnconfigure(1, weight=2)
ant.columnconfigure(2, weight=0)
ant.columnconfigure(3, weight=2)
ant.columnconfigure(4, weight=2)
ant.columnconfigure(5, weight=1)

ant.rowconfigure(0, weight=1)
ant.rowconfigure(1, weight=1)
ant.rowconfigure(2, weight=1)

'''ROW 0'''

marketLabel = tk.Label(ant, text='Market', font=FONT, bg=COLOR, fg=WHITE)
marketLabel.grid(row=0, column=0, columnspan=2, padx=15)

spaceHolder1 = tk.Canvas(ant, bg=COLOR, width=5, highlightthickness=0)
spaceHolder1.grid(row=0, column=2)

positionLabel = tk.Label(ant, text='Positions', font=FONT, bg=COLOR, fg=WHITE)
positionLabel.grid(row=0, column=3, columnspan=2, padx=15)

balanceLabel = tk.Label(ant, text=f'Balance\n{balance}', font=FONT2, bg=COLOR, fg=WHITE)
balanceLabel.grid(row=0, column=5, padx=5)

'''ROW 1'''

marketListBox = tk.Listbox(ant, height=30, width=20)
marketListBox.grid(row=1, column=0, columnspan=2, pady=5)

spaceHolder2 = tk.Canvas(ant, bg=COLOR, width=5, highlightthickness=0)
spaceHolder2.grid(row=1, column=2)

positionsListBox = tk.Listbox(ant, height=30, width=20)
positionsListBox.grid(row=1, column=3, columnspan=2, pady=5)

changeBalanceButton = tk.Button(ant, text='Change Balance', font=FONT2, command=changeBalance)
changeBalanceButton.grid(row=1, column=5, sticky=N)

ALButton = tk.Button(ant, text='Activity Log', font=FONT2, command=activityLogFunc)
ALButton.grid(row=1, column=5, sticky=N, pady=(40,0))

WLButton = tk.Button(ant, text='View Win/Loss', font=FONT2, command=winLoss)
WLButton.grid(row=1, column=5, sticky=N, pady=(80,0))

'''ROW 2'''

buyButton = tk.Button(ant, text='Buy', font=FONT1, command=buy)
buyButton.grid(row=2, column=0, padx=(15,0))

removeButton = tk.Button(ant, text='Remove', font=FONT1, command=remove)
removeButton.grid(row=2, column=1, padx=(0, 10))

spaceHolder3 = tk.Canvas(ant, bg=COLOR, width=5, highlightthickness=0)
spaceHolder3.grid(row=2, column=2)

sellButton = tk.Button(ant, text='Sell', font=FONT1, command=sell)
sellButton.grid(row=2, column=3, columnspan=2)


'''ROW 3'''

addTickerButton = tk.Button(ant, text='Add Ticker', font=FONT1, command=addTicker)
addTickerButton.grid(row=3, column=0, columnspan=2, pady=(0, 15))

'''ABSOLUTE POSITIONS'''

bgColorEntry = tk.Entry(ant, width=10)
bgColorEntry.place(x=450, y=340)

bgColorButton = tk.Button(ant, text='Change BG', command=bgColor, font=FONT2)
bgColorButton.place(x=452, y=360)

fgColorEntry = tk.Entry(ant, width=10)
fgColorEntry.place(x=450, y=290)

fgColorButton = tk.Button(ant, text='Change FG', command=fgColor, font=FONT2)
fgColorButton.place(x=452, y=310)



ant.mainloop()