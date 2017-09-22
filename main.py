'''
	A Python Script to Fetch the Weekly Top 15 songs from the given URL and Compare it with the last week's list
	Author: Aneesh Bhatnagar
	URL: www.aneeshbhatnagar.com
'''
import urllib
from lxml import html
import os.path
from tabulate import tabulate

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
	removedTracks = []
	newTracks = []
	for track in newHashMap.keys():
		if track not in oldHashMap:
			temp = track.split(",")
			newTracks.append([newHashMap[track],temp[0],temp[1],"Newly Added","-"])
		else:
			temp = track.split(",")
			if oldHashMap[track] != newHashMap[track]:
				newTracks.append([newHashMap[track],temp[0],temp[1],oldHashMap[track],newHashMap[track]])
			else:
				newTracks.append([newHashMap[track],temp[0],temp[1],"-","-"])
	i = 1
	for track in oldHashMap.keys():
		if track not in newHashMap:
			temp = track.split(",")
			removedTracks.append([i, temp[0],temp[1]])
			i+=1
	return newTracks, removedTracks

def displayList(data, removedData = None):
	if removedData == None:
		for i in xrange(len(data)):
			data[i].insert(0,i+1)
		print tabulate(data, headers = ['Position','Song Title','Album'])
	else:
		data = sorted(data, key = lambda d:d[0])
		print tabulate(data, headers = ['Positon','Song Title', 'Album', 'Current Position', 'Old Position'])
		if removedData:
			print "Some songs were removed. Here is a list of those"
			print tabulate(removedData, headers = ['S.No','Song Title','Album'])


if __name__ == '__main__':
	oldData = []
	oldDataFlag = False
	if os.path.isfile('newData.txt'):
	 	oldData = readListFromFile('newData.txt')
	 	oldDataFlag = True
	url = "https://www.saavn.com/s/featured/hindi/Weekly+Top+Songs"
	newData = findDetailsInHTML(readHTMLFromFile('test.txt'))
	if oldDataFlag:
		if oldData == newData:
			print "The Saavn list is not updated yet. You have the latest playlist already."
			displayLatestList(newData)
		else:
			print "The Saavn list has been updated. Here is the new list."
		 	#writeListToFile(oldData,'oldData.txt')
		 	#writeListToFile(newData, 'newData.txt')
			difference, removed = findDifferenceInData(oldData, newData)
			displayList(difference, removed)
	else:
		print "Here is this week's Saavn Top 30 Bollywood songs list."
		displayList(newData)