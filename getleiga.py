# -*- coding: utf-8 -*-

from lxml import etree
from mechanize import Browser

def getLeiga():
	browser = Browser()
	browser.set_handle_robots(False)
	browser.addheaders = [('Referer', 'http://www.leiga.is/'), ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	
	#NEEDS TO LOOK LIKE: ADDRESS, LOCATION, PRICE, SIZE, ROOMS, LINK
	results = []
	
	browser.open("http://www.leiga.is/eignir")
	root = etree.fromstring(browser.response().read(), etree.HTMLParser())
	apts = root.findall('.//li/a')
	
	pageCounter = 1
	
	while(True):
		for apt in apts:
			href = apt.attrib['href']	
			if '/eignir/' in href:
				isFinalPage = False
				
				link = "http://www.leiga.is" + href
				
				details = apt.find('.//span')
				price = details.find('.//span[@class="price"]').text.replace(' kr.', '').strip()
				address = details.find('.//strong').text.strip()
				
				tmp = details.find('.//em').text
				location = tmp[:tmp.find(' ')].strip()
				
				tmp = details.find('.//span[@class="detail"]').text	
				rooms = tmp[:tmp.find('|')].replace('herbergi', '').strip()
				size = tmp[tmp.rfind('|')+1:].replace('m', '').strip()
				
				
				#FIXES GO HERE:
				if not price[0].isdigit():
					price = "?"
				if not size[0].isdigit():
					size = "?"
				if not rooms[0].isdigit():
					rooms = "?"
				if not location[0].isdigit():
					location = "?"
				
				result = [address, location, price, size, rooms, link]
				results.append(result)
		
		if(isFinalPage):
			break
		
		pageCounter = pageCounter + 1
		nextPageLink = "?page="+str(pageCounter)+"&order=date&property=0"
		browser.open(nextPageLink)
		
		root = etree.fromstring(browser.response().read(), etree.HTMLParser())
		apts = root.findall('.//li/a')
		isFinalPage = True

	return results
