# This is a template for a Python scraper on Morph (https://morph.io)
# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

# Set entity_id
entity_id = 'E4201_BMBC_gov'

# # Read in a page
url = 'http://www.bolton.gov.uk/website/pages/Expenditurereports.aspx'
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)

# # Find something on the page using css selectors
box = soup.find('div',{'id':'pageDownloads'})
blocks = box.findAll('li')

# # Set up functions
# # convert strings to numbers for months
def convert_mth_strings ( mth_string ):
	month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
	#loop through the months in our dictionary
	for k, v in month_numbers.items():
		#then replace the word with the number
		mth_string = mth_string.replace(k, v)
	return mth_string
	

for block in blocks:
	link = block.find('a').get('href').encode('utf8')
	link = link.replace(' ','%20')
	title = block.a.getText().encode('utf8').strip() #  get the text, encode and rmv whitespace
	year = title.rsplit(' ',1)[1] #  gets the last word from the file title
	month = title.rsplit(' ',2)[1] #  gets the penultimate word from the file title
	
	month_stem = month.upper()[:3]
	month_val = convert_mth_strings(month_stem)
	filename = entity_id + "_" + year + "_" + month_val
	
	todays_date = str(datetime.now())
	
	scraperwiki.sqlite.save(unique_keys=['l'], data={"l": link, "f": filename, "d": todays_date })
	
	print filename
