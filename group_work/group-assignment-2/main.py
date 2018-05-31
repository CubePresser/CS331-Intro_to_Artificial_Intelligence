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
		line = line.strip()
		line = line.split() #split it into individual words
		preStuff = [0]*len_dictionary #this is the sub array for each sentence 
		preStuff[len_dictionary - 1] = int(line[-1].strip()) #put the class label as the last spot
		for x in range(len_dictionary): #for each word in the dictionary
			for y in line: 
				if y == dictionary[x]: #check to see if they're the same
					preStuff[x] = 1 # if they replace the 0 with a 1 
		values.append(preStuff) #add this sentence information to the total array
	return values


def stripPunctuation(sentence):
	translator = str.maketrans('', '', string.punctuation)
	sentence = sentence.translate(translator)
	return sentence

def generateFiles(testData, trainingData):
	#Open preprocess files for writing into
	f1 = open("preprocessed_test.txt", "w+")
	f2 = open("preprocessed_train.txt", "w+")

	#For each line in the test and training data, write into the appropriate file, stripping any brackets and adding a newline
	for line in testData:
		f1.write(str(line)[1:-1]+"\n")

	for line in trainingData:
		f2.write(str(line)[1:-1]+"\n")

	#Close the files
	f1.close()
	f2.close()

if __name__ == "__main__": #treat this as a main function and keep at bottom of file
	fileName = argv[1] #first arguement after script name should be what file is wanted
	dictionary = buildDictionary(fileName)
	dictionary.append('classLabel')
	values = makePreProccessed(fileName, dictionary)
	values.insert(0, dictionary)
	generateFiles(values, values)
	#print(dictionary)