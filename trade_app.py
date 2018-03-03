from functools import partial
import datetime

from time import sleep
from lxml import html
import requests
from time import sleep

import urllib3

from prettytable import PrettyTable

from collections import defaultdict

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

global new_cash
new_cash = 0
global new_position
new_position = 0



def process_input():
     while True:
          try:
               line = input(' >> ')
          except EOFError:
               return
          if line=='':
               return
          return line





class Account:


     def __init__(self, name, balance):
          self.name = name
          self.balance = balance
          self.transactions = []
          self.stocks = defaultdict(float)

     @property
     def balance(self):
          return self._balance

     @balance.setter
     def balance(self, value):
          # print('set balance')
          if not (type(value) == int or type(value) == float):
               raise ValueError('Balance must be a number.')

          value = float(value)
          if value < 0:
               raise ValueError('Balance must stay positive.')
          else:
               self._balance = value



     def execute_trade(self, side, stock, amount, price, total, timestamp):
          assert side == 'Sell' or side == 'Buy', 'Invalid side'
          assert amount > 0, 'Amount must be > 0'
          assert price > 0, 'Price must be > 0'
          assert total > 0, 'Total must be > 0'

          if side == 'Sell':
               new_balance = self.balance + total
               new_stocks = self.stocks[stock] - amount

          elif side == 'Buy':
               new_balance = self.balance - total
               new_stocks = self.stocks[stock] + amount
               #####
               total = -total

          if new_balance < 0:
               raise ValueError('Not enought money')
          if new_stocks < 0:
               raise ValueError('Not enough stocks')

          self.balance = new_balance
          self.stocks[stock] = new_stocks
          self.transactions.append([side, stock, amount, price, total, timestamp])



class Menu:

     def __init__(self, greeting, options, ret=False):
          self.greeting = greeting
          self.options = options
          # self.parent_menu = parent_menu
          self.ret = ret

     def __call__(self):

          while True:

               print(self.greeting)
               print('Please make your choice')
               for i, op in enumerate(self.options, start=1):
                    print(f'[{i}] {op[0]}')
               print('[9] Back')
               print('[0] Quit')

               #choice = input(' >> ')
               
          
               choice = process_input()
               
               
               try:
                    
                                     
                    ch = int(choice)
                   

                    if ch == 9:
                         break
                         # self.parent_menu()

                    if ch == 0:
                         print('Exiting')
                         quit()

                    selected = self.options[ch-1][1]
                    #print(ch)
                    #print(selected)
                    

               except (KeyError, ValueError, IndexError):
                    print('Invalid choice.')

               else:
                    if self.ret:
                         return selected()
                    else:
                         selected()



def make_return_self_list(l):
     return [(s, partial((lambda x: x), s)) for s in l]

def trade():

     print('{:=^30}'.format('TRADE'))

     stock_list = ['QQQ', 'AAPL', 'INTC','MSFT', 'FB']
     stock = None
     side = None
     amount = None
     price = None
     total = None

     # get stock
     stock_select_m = Menu(
             'Select the Stock',
                make_return_self_list(stock_list),
                ret=True)
     stock = stock_select_m()
     if stock == None: return
     print(stock)

     # get buy/sell
     buy_sell_m = Menu(
             'Sell or buy?',
                make_return_self_list(['Sell', 'Buy']),
                ret=True)
     side = buy_sell_m()
     if side == None: return
     print(side)

     # get amount
     while amount == None:
          print('How much do you want to Trade?')
          print('[0] Cancel')
          try:
               amount = float(input('  >>  '))
               if amount == 0:
                    break
               if amount < 0:
                    raise ValueError('Amount must be positive')
          except ValueError:
               print('Invalid number, please try again.')
               amount = None
     if amount == None: return

     # get price
     price = get_price(stock, side)

     total = price * amount

     # get confirmation
     print(f'{side} {amount} of {stock} for {price} each and a total of {total}?')
     if not input('Yes/No? ').lower().startswith('y'):
          return


     dt_obj = datetime.datetime.now()
     ts = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
     #ts = str(datetime.datetime.now())

     global acc
     try:
          acc.execute_trade(
                     side=side,
                        stock=stock,
                        amount=amount,
                        price=price,
                        total=total,
                        timestamp=ts
                )
     except (AssertionError, ValueError) as e:
          print(e)
     else:
          print('transaction completed')


def print_blotter():
     global acc
     print('{:=^30}'.format('Transactions'))
     print('side\t\tticker\t\tquant\t\tprice\t\tmoney i/o\t\ttimestamp')
     for t in acc.transactions:
          print(*t, sep='\t\t')


greet = '{:=^30}'.format('MAIN MENU')

def not_implemented():
     print('Not implemented')
     
     

#def get_price(stock, iside):
     #prc = float(input('exec price  >>  '))
     #return prc
     

def  get_price(stock, iside):
     url = "https://finance.yahoo.com/quote/%s?p=%s" % (stock, stock)
     ##https://finance.yahoo.com/quote/IBM?p=IBM
     response = requests.get(url, verify=False)
     #print("Parsing %s" % (url))
     parser = html.fromstring(response.text)
     try:
          if (iside == 'Buy'):
               ask = parser.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[4]/td[2]/span/text()')
               aprice, asize = ask[0].split('x')
               aprice = float(aprice)
               asize = int(asize)
               oside = aprice

          elif(iside == 'Sell'):
               bid = parser.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[3]/td[2]/span/text()')
               bprice, bsize = bid[0].split('x')
               bprice = float(bprice)
               bsize = int(bsize)
               oside = bprice
            
          elif(iside == 'M'):
               ask = parser.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[4]/td[2]/span/text()')
               aprice, asize = ask[0].split('x')
               aprice = float(aprice)

               bid = parser.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[3]/td[2]/span/text()')
               bprice, bsize = bid[0].split('x')
               bprice = float(bprice)
               mkt = (bprice + aprice) /2
               mkt = round(float(mkt),2)
               oside = mkt
     except:
          print("Failed to get price. Returning to menu")
          trade()
          #return {"error": "Failed to get web response"}
     #print(oside)
     return oside




def print_pl():
     global acc
     temp_lst = []
     stock_pl = []

     print('{:=^30}'.format('Transactions'))
     print("Profit/Loss\n")

     stock_uni = []
       
     for a in acc.transactions:
          stock_uni.append(a[1])
     
     stock_list = list(set(stock_uni))

     #  transactions([side, stock, amount, price, total, timestamp])

     for stock in stock_list:
          temp_lst = get_pl(stock)
          stock_pl.append(temp_lst)
     
     #print(stock_pl)
                    
     #table = PrettyTable(['side','ticker','Quantity', 'Exec Price', 'Cash IO','timestamp','Remain Cash', 
                    #'Position','WAP','UPL','RPL', 'pmv','pwap','twap','tmkv'])

     table = PrettyTable(['ticker','Tot chg Cash', 'Position','Mkt Price','WAP','UPL','RPL'])	
     
     for t in stock_pl:
          table.add_row(t)
     print(table)
     
     
     

def get_pl(ticker):
     
     new = []
     new_pl = []
     new_cash = 0
     new_position = 0
     wap = 0
     
     for x in acc.transactions:
          if x[1] == ticker:	
     
               #mkt_prc = prc = float(input('mkt price  >>  '))  ######################  for testing
               
               mkt_prc = get_price(ticker, 'M')
               
               if x[0] == 'Sell':
                    new_cash += x[4]
                    new_position -= x[2]
                    trade_mkt_val = x[3] * x[2]
               elif x[0] == 'Buy':
     
                    new_cash += x[4]
                    new_position += x[2]
                    trade_mkt_val = mkt_prc * x[2]
               if new_position > 0:
                    wap = abs(round((new_cash / new_position),2))
               else:
                    wap = abs(round((x[4]/ x[2]),2))
     
               position_mkt_val = mkt_prc * new_position
     
               position_wap = wap * new_position
               trade_wap = wap * x[2]
     
               #trade_mkt_wap = trade_mkt_val  - trade_wap
     
               upl = position_mkt_val  - position_wap
     
               if x[0] == 'Sell':
                    rpl = trade_mkt_val - trade_wap
               else:
                    rpl = 0
                    #Ticker	cash out Position 	Current Market Price	WAP 	UPL 	RPL 
     
               #new.append([x[0],x[1],x[2],x[3],x[4],x[5],new_cash,new_position,wap,upl,rpl,position_mkt_val,position_wap, trade_wap,trade_mkt_val])	
               new.append([x[1],new_cash,new_position,mkt_prc, wap,upl,rpl])	
     
     tail = new[-1:]
     
     if tail:
          new_pl = new[-1]
     return new_pl
                   
    


options = [
     ('Trade', trade),
        ('Blotter', print_blotter),
        ('Profit/Loss', print_pl)
]




acc = Account('test', 1000000000)
# print(acc.balance)

main_m = Menu(greet, options)
main_m()
