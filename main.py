'''
	A Python Script to Fetch the Weekly Top 15 songs from the given URL and Compare it with the last week's list
	Author: Aneesh Bhatnagar
	URL: www.aneeshbhatnagar.com
'''
import urllib
from lxml import html

# url = "https://www.saavn.com/s/featured/hindi/Weekly+Top+Songs"
#content = urllib.urlopen(url).read()
f = open('test.txt')
lines = f.readlines()
f.close()
lines = ''.join(lines)
page = html.fromstring(lines)
songs = []
albums = []

for song in page.xpath("//p[contains(@class, 'song-name')]"):
	songs.append(song.text)
for album in page.xpath("//p[contains(@class, 'album-name')]"):
	albums.append(album.text)
for i in xrange(len(songs)):
	print songs[i] + '\t' + albums[i]