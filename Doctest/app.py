from lxml import html  
import requests
from time import sleep


import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def parse(ticker,iside):
    url = "http://finance.yahoo.com/quote/%s?p=%s"%(ticker,ticker)
    response = requests.get(url, verify=False)
    print ("Parsing %s"%(url))
    sleep(4)
    parser = html.fromstring(response.text)
    #summary_table = parser.xpath('//div[contains(@data-test,"summary-table")]//tr')
    if(iside=='B'):
       ask =  parser.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[4]/td[2]/span/text()')
       #ask = [i.replace('[', '') for i in ask]
       oside=ask[0]
       aa,bb=ask[0].split('x')
       aa=float(aa)
       bb=int(bb)
       print(ask[0])
       xx=aa*bb
       print(xx)          
    else:       
       bid = parser.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[3]/td[2]/span/text()')
       oside=bid
       #print(bid)
    
    
    return oside

if __name__=="__main__":
    ticker='aapl'
    iside='B'
    print ("Fetching data for %s"%(ticker))
    price = parse(ticker,iside)
    print(price,iside)
    
