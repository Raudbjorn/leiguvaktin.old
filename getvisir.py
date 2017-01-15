# -*- coding: utf-8 -*-

from lxml import etree
from mechanize import Browser


def getVisir():
	b = Browser()
	b.set_handle_robots(False)
	
	b.addheaders = [('Referer', 'http://fasteignir.visir.is/'), ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	
	b.open('http://fasteignir.visir.is/ajaxsearch/getresults?category=1,2,4,7,17&room=0,10&area=0,1000&price=0,500000&stype=rent&itemcount=60&sort=created')
	
	
	
	
	root = etree.fromstring(b.response().get_data().decode('ISO-8859-1'), etree.HTMLParser())
	
	
	
	eignir = root.findall('.//div[@class="b-products-item-details"]')
	results = []
	#eignir = [eign for eign in eignir if 'property' in eign.attrib['href']]
	
	for eign in eignir:
		
		neweign = []
		addr = eign.find('.//h2/a').text.encode('ISO-8859-1').strip().decode('UTF-8')
		link = "http://fasteignir.visir.is"+eign.find('.//h2/a').attrib['href']
		loc = eign.find('.//h2/a/span').text.encode('ISO-8859-1').strip().decode('UTF-8')
		price = eign.find('.//td[1]/strong').text.encode('ISO-8859-1').strip().decode('UTF-8')
		size = eign.find('.//td[2]/strong').text.encode('ISO-8859-1').strip().decode('UTF-8')
		
		roomElement = eign.find('.//td[4]/strong')
		if roomElement is not None:
			rooms = eign.find('.//td[4]/strong').text.encode('ISO-8859-1').strip().decode('UTF-8')+" herb"
		else:
			rooms = ""
		
		addr = addr.replace(",", "").strip()
		size = size.replace(size[size.find(" "):], "")
		rooms = rooms.replace(" herb", "")
		
		#FIXES HERE
		if rooms == "": rooms = "?"
		
		
		#NEEDS TO LOOK LIKE: ADDRESS, LOCATION, PRICE, SIZE, ROOMS, LINK
		results.append([addr, loc, price, size, rooms, link])
		
	return results