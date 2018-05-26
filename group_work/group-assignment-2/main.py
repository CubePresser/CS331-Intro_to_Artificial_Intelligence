import os, string
from sys import argv

def buildDictionary(fileName):
	file = open(fileName, "r") #open our given file with read only permissions
	dictionary = []	
	for line in file:
		nakedLine = stripPunctuation(line).lower() #remove punctuation and make lowercase
		nakedLine = nakedLine.split('\t') #separate words from number

		dictionary = dictionary + nakedLine[0].split(' ') #add words to dictionary

	return sorted(list(set(dictionary))) #this removes duplicates and creates a sorted list

def makePreProccessed(fileName, dictionary):
	file = open(fileName, "r") #open our given file with read only permissions
	values = [] #1s and 0s that mean if a dictionary word is in the sentences or not
	for line in file: #for every line in the file
		line = line.split(' \t') #split it into individual words
		preStuff = [] #this is the sub array for each sentence

		#TODO: this is not going to work because the dictionary is way to long compared to the sentences
		#need to find a way to get which location the word is in the dictionary and set that index to 1
		for x in range(len(dictionary)): #for each word in the dictionary
			if line[x] == dictionary[x]: #check to see if they're the same
				preStuff.append(1) # if they are put a 1
			else:
				preStuff.append(0) #otherwise put a 0


	return values


def stripPunctuation(sentence):
	sentence = sentence.translate(None, string.punctuation)
	return sentence

if __name__ == "__main__": #treat this as a main function and keep at bottom of file
	fileName = argv[1] #first arguement after script name should be what file is wanted
	dictionary = buildDictionary(fileName)
	values = makePreProccessed(fileName, dictionary)
	print(dictionary)