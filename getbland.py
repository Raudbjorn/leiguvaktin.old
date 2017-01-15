# -*- coding: utf-8 -*-

from lxml import etree
from mechanize import Browser
from BeautifulSoup import BeautifulSoup


def getBland():

	b = Browser()
	b.set_handle_robots(False)
	b.addheaders = [('Referer', 'http://www.bland.is/'), ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	
	while(True):
		try:
			b.open('https://bland.is/classified/?categoryId=59&page=1', timeout=15.0)
			break
		except:
			pass
	
	
	root = etree.fromstring(BeautifulSoup(b.response().read()).prettify(), etree.HTMLParser())
	apts = root.findall('.//div[@class="searchResultContent"]')
	
	counter = 2
	
	hrefs = []
	
	while(apts != []):
		
		for apt in apts:
			try:
				if apt.find('.//p/span[3]/a').text.strip() == "Til leigu":
					hrefs.append(apt.find('.//h3/a').attrib['href'])
			except:
				pass
			
		
		while(True):
			try:
				b.open('https://bland.is/classified/?categoryId=59&page='+str(counter), timeout=15.0)
				break
			except:
				pass
		
		root = etree.fromstring(BeautifulSoup(b.response().read()).prettify(), etree.HTMLParser())
		apts = root.findall('.//div[@class="searchResultContent"]')
		counter += 1
		
		
	results = []
	
	for href in hrefs:
		while(True):
			try:
				b.open("https://bland.is"+href, timeout=15.0)
				break
			except:
				pass
		
		root = etree.fromstring(BeautifulSoup(b.response().read()).prettify(), etree.HTMLParser())
		
		try:	
			addr = root.find('.//span[@class="product_headline"]').text.strip()
		except:
			continue

		try:
			loc = root.find('.//table[@class="table table-striped"]/tbody/tr[2]/td[2]').text.strip()
		except:
			loc = "?"
		
		try:
			price = root.find('.//h5[@class="buyNow_price"]').text.strip().replace(" kr.", "")
		except:
			price = "?"
			
		try:
			size = root.find('.//table[@class="table table-striped"]/tbody/tr[1]/td[5]').text.strip()
		except:
			size = "?"
		
		try:
			rooms = root.find('.//table[@class="table table-striped"]/tbody/tr[2]/td[5]').text.strip()
		except:
			rooms = "?"
		
		link = "https://bland.is"+href
		
		
		
		#NEEDS TO LOOK LIKE: ADDRESS, LOCATION, PRICE, SIZE, ROOMS, LINK
		results.append([addr, loc, price, size, rooms, link])
		
	return results
