# -*- coding: utf-8 -*-

from lxml import etree
from mechanize import Browser

def getListinn():

	b = Browser()
	b.set_handle_robots(False)
	b.addheaders = [('Referer', 'http://www.leigulistinn.is/'), ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	
	#NEEDS TO LOOK LIKE: ADDRESS, LOCATION, PRICE, SIZE, ROOMS, LINK
	results = []
	counter = 0
	
	while(counter != 5):
		b.open('http://leigulistinn.is/synishorn')
		
		
		root = etree.fromstring(b.response().read().decode('ISO-8859-1'), etree.HTMLParser())
		
		eignir = root.findall('.//tbody[@id="reseter"]/tr')
		
		
		
		for eign in eignir:
		
			addr = eign.find('.//td[2]').text.encode('ISO-8859-1').strip().decode('UTF-8')
			loc = eign.find('.//td[3]').text.encode('ISO-8859-1').strip().decode('UTF-8')
			price = eign.find('.//td[6]').text.encode('ISO-8859-1').strip().decode('UTF-8').replace(" kr", "")
			size = eign.find('.//td[5]').text.encode('ISO-8859-1').strip().decode('UTF-8')
			rooms = eign.find('.//td[4]').text.encode('ISO-8859-1').strip().decode('UTF-8').replace(" Herb", "")
			link = 'http://leigulistinn.is/synishorn'
			
			
			#FIXES GO HERE
			if rooms == "Herbergi": rooms = "1"
			if rooms == "Stúdíó".decode('ISO-8859-1'): rooms = "1"
			
			if([addr, loc, price, size, rooms, link] not in results):
				results.append([addr, loc, price, size, rooms, link])
			
			
		counter += 1
		
	return results
		

	