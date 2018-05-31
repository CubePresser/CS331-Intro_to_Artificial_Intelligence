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
	len_dictionary = len(dictionary)
	for line in file: #for every line in the file
		line = stripPunctuation(line)
		line = line.split(' \t') #split it into individual words
		preStuff = [0]*len_dictionary #this is the sub array for each sentence 

		for x in range(len_dictionary): #for each word in the dictionary
			for y in line: 
				if y == dictionary[x]: #check to see if they're the same
					preStuff[x] = 1 # if they replace the 0 with a 1 
		preStuff[len_dictionary - 1] = line[-1] #put the class label as the last spot
		values.append(preStuff)
	return values


def stripPunctuation(sentence):
	translator = str.maketrans('', '', string.punctuation)
	sentence = sentence.translate(translator)
	return sentence

def generateFiles(testData, trainingData):
	f1 = open("preprocessed_test.txt", "w+")
	f2 = open("preprocessed_train.txt", "w+")

	for line in testData:
		f1.write(str(line))

	for line in trainingData:
		f2.write(str(line))

	f1.close()
	f2.close()

if __name__ == "__main__": #treat this as a main function and keep at bottom of file
	fileName = argv[1] #first arguement after script name should be what file is wanted
	dictionary = buildDictionary(fileName)
	dictionary.append('classLabel')
	values = makePreProccessed(fileName, dictionary)
	#print(values[1])
	generateFiles(values, values)
	#print(dictionary)