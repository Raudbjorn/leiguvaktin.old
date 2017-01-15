# -*- coding: utf-8 -*-

from lxml import etree
from mechanize import Browser
from BeautifulSoup import BeautifulSoup


def getMbl():
	b = Browser()
	b.set_handle_robots(False)
	b.addheaders = [('Referer', 'http://www.mbl.is/'), ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	
	b.open('http://www.mbl.is/leiga/leit/?area=165&rooms=&min_price=&max_price=&text_query=')
	root = etree.fromstring(b.response().read().decode('ISO-8859-1'), etree.HTMLParser())
	eignir = root.findall('.//div[@class="rental-itemlist-property clearfix"]')
	pagecounter = 2
	soup = BeautifulSoup(b.response().read())
	mydivs = soup.findAll("div", { "class" : "rental-itemlist-maininfo" })
	
	#NEEDS TO LOOK LIKE: ADDRESS, LOCATION, PRICE, SIZE, ROOMS, LINK
	results = []

	while(eignir != []):
		
		sizeAndRooms = []
		
		for div in mydivs:
			div = str(div).strip()
			div  = div.replace('<div class="meta span-3 last">', '')
			div = div.replace('\n', '')
			div = div.replace('</div>', '')
			div = div.replace('  ', '')	
			div = div.split('<br />')
			sizeAndRooms.append(div)
		
		for eign in eignir:
			
			split =  eign.find('.//a[@class="rental-itemlist-headline"]').text.encode('ISO-8859-1').strip().decode('UTF-8').split(",")
			
			addr = split[0].strip()
			link = "http://www.mbl.is"+eign.find('.//a[@class="rental-itemlist-headline"]').attrib['href']
			loc = split[1].strip()
			price = eign.find('.//div[@class="rental-itemlist-price"]').text.encode('ISO-8859-1').strip().decode('UTF-8')
			size = sizeAndRooms[eignir.index(eign)][2]
			rooms = sizeAndRooms[eignir.index(eign)][1]
			
			price = price.replace(price[price.find(" "):], "")+".000"
			size = size.replace(" fm", "")
			rooms = rooms.replace(" herbergi", "")
			
			
			#FIXES GO HERE:
			if rooms == "None": rooms = "?"
			if price == "0.000": price = "?"
			if size == "0": size = "?"
			
			
			results.append([addr, loc, price, size, rooms, link])
			
		
		b.open('http://www.mbl.is/leiga/leit/?page='+str(pagecounter)+'&area=165&rooms=&min_price=&max_price=&text_query=')
		root = etree.fromstring(b.response().read().decode('ISO-8859-1'), etree.HTMLParser())
		eignir = root.findall('.//div[@class="rental-itemlist-property clearfix"]')
		pagecounter += 1
		
		soup = BeautifulSoup(b.response().read())
		mydivs = soup.findAll("div", { "class" : "rental-itemlist-maininfo" })
	
	return results
	