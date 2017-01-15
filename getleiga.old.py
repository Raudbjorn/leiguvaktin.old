# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from mechanize import Browser
from lxml import etree

def getLeiga():
	b = Browser()
	b.set_handle_robots(False)
	b.addheaders = [('Referer', 'http://www.leiga.is/'), ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	
	results = []
	
	b.open('http://www.leiga.is/ajax/search.aspx', "pagenumber=1&area=&type=&searchType=1&keywords=&housefund=&electricity=&heating=&pets=&smoking=&roommate=&gender=")
	root = etree.fromstring(b.response().read().decode('ISO-8859-1'), etree.HTMLParser())
	apts = root.findall('.//div[@class="holder"]')
	
	counter = 2
	
	while(apts != []):
		for apt in apts:
		
			longstring = apt.find('.//a/h2').text
			
			addrAndLoc = longstring.split(", ")
			
			
			
			addr = addrAndLoc[0]
			
			loc = addrAndLoc[1][:4]
			
			link = "http://www.leiga.is"+apt.find('.//a').attrib['href']
			
			price = apt.find('.//h3').text
			price = price[price.find(": ")+2:price.find(" kr.")]
			
			rooms = apt.find('..//dl/dd[1]').text
			
			size = apt.find('..//dl/dd[2]').text
		
			results.append([addr, loc, price, size, rooms, link])
			
		b.open('http://www.leiga.is/ajax/search.aspx', "pagenumber="+str(counter)+"&area=&type=&searchType=1&keywords=&housefund=&electricity=&heating=&pets=&smoking=&roommate=&gender=")
		root = etree.fromstring(b.response().read().decode('ISO-8859-1'), etree.HTMLParser())
		apts = root.findall('.//div[@class="holder"]')
		counter += 1
		
	return results
