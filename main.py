'''
	A Python Script to Fetch the Weekly Top 15 songs from the given URL and Compare it with the last week's list
	Author: Aneesh Bhatnagar
	URL: www.aneeshbhatnagar.com
'''
import urllib
from lxml import html
import os.path

def fetchDataFromWeb(url):
	return urllib.urlopen(url).read()	

def readHTMLFromFile(filename):
	f = open(filename)
	lines = ''.join(f.readlines())
	f.close()
	return lines

def findDetailsInHTML(data):
	page = html.fromstring(data)
	songs = []
	albums = []
	data = []

	for song in page.xpath("//p[contains(@class, 'song-name')]"):
		songs.append(song.text)
	for album in page.xpath("//p[contains(@class, 'album-name')]"):
		albums.append(album.text)
	for i in xrange(len(songs)):
		data.append([songs[i],albums[i]])
	return data

def writeListToFile(data, filename):
	f = open(filename, 'w')
	for item in data:
		f.write("%s\t%s\n" % (item[0], item[1]))
	f.close()

def readListFromFile(filename):
	f = open(filename)
	lines = f.readlines()
	output = []
	for line in lines:
		x = line.strip().split("\t")
		output.append([x[0],x[1]])
	f.close()
	return output

def findDifferenceInData(old,new):
	oldHashMap = {x[0]+","+x[1]:i+1 for i,x in enumerate(old)}
	newHashMap = {x[0]+","+x[1]:i+1 for i,x in enumerate(new)}
	addedTracks = []
	removedTracks = []
	movedTracks = []
	for track in newHashMap.keys():
		if track not in oldHashMap:
			temp = track.split(",")
			addedTracks.append([temp[0],temp[1]])
		else:
			if oldHashMap[track] != newHashMap[track]:
				temp = track.split(",")
				movedTracks.append([temp[0],temp[1],oldHashMap[track],newHashMap[track]])
	for track in oldHashMap.keys():
		if track not in newHashMap:
			temp = track.split(",")
			removedTracks.append([temp[0],temp[1]])
	return addedTracks, removedTracks, movedTracks


if __name__ == '__main__':
	oldData = []
	oldDataFlag = False
	# if os.path.isfile('newdata.txt'):
	# 	oldData = readListFromFile('newdata.txt')
	# 	writeListToFile(oldData,'oldData.txt')
	# 	oldDataFlag = True
	oldData = readListFromFile('oldData.txt')
	oldDataFlag = True
	url = "https://www.saavn.com/s/featured/hindi/Weekly+Top+Songs"
	newData = findDetailsInHTML(readHTMLFromFile('test.txt'))
	if oldDataFlag:
		print findDifferenceInData(oldData, newData)