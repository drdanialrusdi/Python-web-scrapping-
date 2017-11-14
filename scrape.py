from urllib.request import urlopen 
from bs4 import BeautifulSoup 
import pandas as pd
import time

prop_name=[]
location=[]
prop_type=[]
title_type=[]
bedroom_no=[]
bathroom_no=[]
prop_size=[]
other_info=[]
prop_price=[]
fail=0

#To extract information of property from property page
def propertyfact(soup):
    prop_name.append(soup.find('h2',{"class":"roboto"}).text)
    print(str(len(prop_name))+" "+prop_name[-1])
    if len(prop_name)%50==0:
        time.sleep(15)
    elif len(prop_name)%100==0:
        time.sleep(60) 
    elif len(prop_name)%500==0:
        time.sleep(180)
    elif len(prop_name)%1000==0:
        time.sleep(300)
    location.append(soup.find('dd',{'class':'loc_dd'}).text)
    fact=soup.find('dl',{'class':'params_dl'})
    ptype='NA'
    ttype='NA'
    bed='NA'
    bath='NA'
    size='NA'
    other='NA'
    for i in range(6):
        try:
            if fact.find_all('dt')[i].text=='Property Type':
                ptype=fact.find_all('dd')[i].text
            elif fact.find_all('dt')[i].text=='Title type':
                ttype=fact.find_all('dd')[i].text
            elif fact.find_all('dt')[i].text=='Bedrooms':
                bed=fact.find_all('dd')[i].text
            elif fact.find_all('dt')[i].text=='Bathroom':
                bath=fact.find_all('dd')[i].text
            elif fact.find_all('dt')[i].text=='Size':
                size=fact.find_all('dd')[i].text
            elif fact.find_all('dt')[i].text=='Other Info':
                other=fact.find_all('dd')[i].text
        except:
            break
    prop_type.append(ptype)
    title_type.append(ttype)
    bedroom_no.append(bed)
    bathroom_no.append(bath)
    prop_size.append(size)
    other_info.append(other)
    try:
        prop_price.append(soup.find('dd',{'class':'dd-price'}).text)
    except:
        prop_price.append("NA")
#To get all link of property in one website page    
def propertyurl(soup):
    itemlist=soup.find('div',{'id':'list-view-ads','class':'list_view_ads'})
    propurl=[]
    for link in itemlist.find_all('h2',{'class':'list_title'}):
        for link2 in link('a'):
            propurl.append(link2.get('href',None))
    propurl.remove('https://www.mudah.my/honeypot.html')
    return propurl

#To get soup file
def urlreader(url):
    while True:
        try:
            
            html = urlopen(url).read()
            print("success")
        except:
            global fail
            fail=fail+1
            if fail>10:
                time.sleep(30)
                fail=0
            print("fail")
            continue
        else:
            soup = BeautifulSoup(html, "html.parser")
            break
    return soup

# To get url for next page until end page
def allpage(soup):
    test=soup.find_all('span',{'class':'non-active nohistory'})
    proppage=[]
    #print(test)
    for link in test:
        proppage.append(link.a.get('href'))
        #print(proppage)
    return proppage
#This part not finish yet, Very scare if error, please try on jupyter first
def mudahscrapper(url="",propertyarea="KL"):
    url=url
    mainsoap=urlreader(url)
    
    #Get url
    firstpage=propertyurl(mainsoap)
    #Get fact
    for house in firstpage:
        factsoap=urlreader(house)
        propertyfact(factsoap)
    
    #URl for all page  
    pagesoap=allpage(mainsoap)
    #url for property in certain page
    if len(pagesoap)!=0:
        for page in pagesoap:
            factsoap=urlreader(page)
            housesurl=propertyurl(factsoap)
            for house in housesurl:
                housesoap=urlreader(house)
                propertyfact(housesoap)
               
    mudahdata=pd.DataFrame({'Property Name':prop_name,'Property Location':location,
                   'Property Type':prop_type,'Title type':title_type,
                   'No of Bedroom':bedroom_no,'No of Bathroom':bathroom_no,
                   'Property Size':prop_size,'Bumi info':other_info,
                   'Property Price':prop_price})

    filename=propertyarea
    mudahdata.to_excel('mudahproperty-'+filename+'.xlsx', index=False)  
    
    
mudahscrapper(url=input("Please input your url: "),propertyarea=input('City name: '))
