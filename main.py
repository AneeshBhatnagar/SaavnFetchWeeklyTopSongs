'''
	A Python Script to Fetch the Weekly Top 15 songs from the given URL and Compare it with the last week's list
	Author: Aneesh Bhatnagar
	URL: www.aneeshbhatnagar.com
'''
import urllib
from lxml import html

url = "https://www.saavn.com/s/featured/hindi/Weekly+Top+Songs"
page = html.fromstring(urllib.urlopen(url).read())