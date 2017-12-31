'''
	A Python Script to Fetch the Weekly Top 15 songs from the given URL and Compare it with the last week's list
	Author: Aneesh Bhatnagar
	URL: www.aneeshbhatnagar.com
'''
import urllib
from lxml import html
import os.path
import datetime as dt
from tabulate import tabulate

class colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'

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
			newTracks.append([newHashMap[track],colors.BLUE + temp[0],temp[1],"Newly Added" + colors.ENDC,"-"])
		else:
			temp = track.split(",")
			if oldHashMap[track] != newHashMap[track]:
				newPosition = ''
				if oldHashMap[track] < newHashMap[track]:
					newPosition = colors.RED + str(newHashMap[track]) + colors.ENDC
				else:
					newPosition = colors.GREEN + str(newHashMap[track]) + colors.ENDC
				newTracks.append([newHashMap[track],temp[0],temp[1],newPosition,oldHashMap[track]])
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
		print tabulate(data, headers = [colors.YELLOW + 'Position','Song Title', 'Album' + colors.ENDC])
	else:
		data = sorted(data, key = lambda d:d[0])
		print tabulate(data, headers = [colors.YELLOW + 'Positon','Song Title', 'Album', 'Current Position','Old Position' + colors.ENDC])
		if removedData:
			print "Some songs were removed. Here is a list of those"
			print tabulate(removedData, headers = ['S.No','Song Title','Album'])


if __name__ == '__main__':
	oldData = []
	oldDataFlag = False
	date = dt.datetime.today().strftime("%m-%d-%Y")
	if os.path.isfile('newData.txt'):
	 	oldData = readListFromFile('newData.txt')
	 	oldDataFlag = True
	url = "https://www.saavn.com/s/featured/hindi/Weekly+Top+Songs"
	#newData = findDetailsInHTML(readHTMLFromFile('test.txt'))
	newData = findDetailsInHTML(fetchDataFromWeb(url))
	if oldDataFlag:
		if oldData == newData:
			print "The Saavn list is not updated yet. You have the latest playlist already."
			displayList(newData)
		else:
			print "The Saavn list has been updated. Here is the new list."
		 	writeListToFile(oldData,'oldData-%s.txt'%date)
		 	writeListToFile(newData, 'newData.txt')
			difference, removed = findDifferenceInData(oldData, newData)
			displayList(difference, removed)
	else:
		print "Here is this week's Saavn Top 30 Bollywood songs list."
		displayList(newData)