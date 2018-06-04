#####################################################
## Jonathan Jones and Brett Case                   ##
## (jonesjon, jonesjonathan) and (casebr, Brallen) ##
## Assignment 3                                    ##
## CS331 Spring 2018                               ##
#####################################################

import os, string
from sys import argv
from math import log10

#Object containing a word, its probabilities for ff, ft, tf, tt and the total number of positive and negative class labels
class BayesNode():
	def __init__(self, word, index):
		self.word = word
		self.probability = {}
		self.positive_cls = self.negative_cls = 0

##################################################
 # Function: buildDictionary
 # Description: gets all unique words in the training data
 # Params: the file with the training data
 # Returns: sorted list of unique words in file
 # Pre-conditions: training data must be strings of words
 # Post-conditions: the unique words in a file will be returned in a list
##################################################
def buildDictionary(fileName):
	file = open(fileName, "r") #open our given file with read only permissions
	dictionary = []	
	for line in file:
		nakedLine = stripPunctuation(line).lower() #remove punctuation and make lowercase
		nakedLine = nakedLine.split('\t') #separate words from number

		dictionary = dictionary + nakedLine[0].split(' ') #add words to dictionary

	return sorted(list(set(dictionary))) #this removes duplicates and creates a sorted list

##################################################
 # Function: makePreProcessed
 # Description: Reads through every line in the data set and generates a feature for each line (Word appearances and class label)
 # Params: File name of data set, dictionary of words from data set
 # Returns: Features from the data set
 # Pre-conditions: Dictionary has already been filled with words from the data set
 # Post-conditions: A feature for every line of the data set has been generated
##################################################
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

##################################################
 # Function: stripPunctuation
 # Description: Removes the punctuation from the given string and returns it.
 # Params: String
 # Returns: String without punctuation
 # Pre-conditions: None
 # Post-conditions: String contains no punctuation.
##################################################
def stripPunctuation(sentence):
	translator = str.maketrans('', '', string.punctuation)
	sentence = sentence.translate(translator)
	return sentence

##################################################
 # Function: generateFiles
 # Description: puts the values from preprocessing into files
 # Params: the test data list, the training data list
 # Returns:  N/A
 # Pre-conditions: pre processing needs to be done on both lists 
 # Post-conditions: the values will be placed into their respective files
##################################################
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

##################################################
 # Function: calculate_word_probabilities
 # Description: Given a list of features and a list of words this funciton will determine the probability that a word is positive or negative when
 # 1. It is not in the sentence and the sentence is negative (FF)
 # 2. It is not in the sentence and the sentence is positive (FT)
 # 3. It is in the sentence and the sentence is negative (TF)
 # 4. It is in the sentence and the sentence is positive (TT)
 # These probabilities are stored in a map structure that uses a word as its key and the probabilities as its values (A 2D array of probabilities)
 # Params: Dictionary of words in data, feature data
 # Returns: Map of words and probabilities (Bayes nodes)
 # Pre-conditions: Data has been processed, dictionary filled, features filled
 # Post-conditions: Probabilities calculated for every word in the dictionary
##################################################
def calculate_word_probabilities(dictionary, features):
	Nodes = {} #Map of BayesNode objects
	for index, word in enumerate(dictionary): #For every word in the dictionary and its index position
		bNode = BayesNode(word, index) #Generate a new bayes node object with the word and index values
		ff = ft = tf = tt = 0
		for feature in features: #For each feature
			if int(feature[-1]) == 1: #If the class label is equal to 1 (_T)
				bNode.positive_cls += 1 #Count number of positive labels
				if int(feature[index]) == 0:
					ft += 1
				else:
					tt += 1
			else: #If the class label is equal to 0 (_F)
				bNode.negative_cls += 1 #Count number of negative labels
				if int(feature[index]) == 0:
					ff += 1
				else:
					tf += 1

		#Calculate the ff, ft, tf and ff probabilities and store them as a 2D array					
		bNode.probability = [[float(float(ff + 1)/float(bNode.negative_cls + 2)),
							float(float(ft + 1)/float(bNode.positive_cls + 2))], 
							[float(float(tf + 1)/float(bNode.negative_cls + 2)), 
							float(float(tt + 1)/float(bNode.positive_cls + 2))]]
		
		#Map a BayesNode to a word and append it to the map structure
		Nodes[word] = bNode

	return Nodes

##################################################
 # Function: classify
 # Description: calculates if a sentence is positive or negative
 # Params: the possible words, the probabilities for those words, the sentence you want, initial probability of good, initial positivity of bad
 # Returns: int of the guess if positive or negative (1 = postive, 0 = negative)
 # Pre-conditions: all data must be pre-processed
 # Post-conditions: the guess of the value of the class label
##################################################
def classify(dictionary, bayes_data, feature, positive, negative):
	for index in range(len(dictionary)): #loop through all the words in the dictionary
		positive += log10(float(bayes_data[dictionary[index]].probability[int(feature[index])][1])) #find postitives
		negative += log10(float(bayes_data[dictionary[index]].probability[int(feature[index])][0])) #find negatives

	if positive >= negative: # if it more likely to be positive, return 1
		return 1
	else:
		return 0

##################################################
 # Function: calculate_accuracy
 # Description: calculates the guesses and how accurate they are and puts them into a file
 # Params: the possible words, the probabilities for those words, the sentence you want to guess, the training file name, the test file name
 # Returns: N/A
 # Pre-conditions: All data must be pre processed
 # Post-conditions: The accuracy of the guesses will be printed to screen and put into results file
##################################################
def calculate_accuracy(dictionary, bayes_data, values, trainFile, testFile):
	num_predictions = num_correct = 0
	num_positives = bayes_data[dictionary[0]].positive_cls #Number of positive class labels
	num_negatives = bayes_data[dictionary[0]].negative_cls #Number of negative class labels

	#Probability that any feature is positive or negative
	positive_prob = log10(num_positives / (num_positives + num_negatives))
	negative_prob = log10(num_negatives / (num_positives + num_negatives))
	
	#for each value calculate the guess and see if it was correct or not
	for val in values:
		num_predictions += 1
		if  classify(dictionary, bayes_data, val, positive_prob, negative_prob) == int(val[-1]): #If the predicted class value is equal to the actual class value
			num_correct += 1

	results = open("results.txt", "a+") #add the current results to the file of results. this is appending to see all old ones too
	#Get accuracy and print to screen and file
	print("Trained from", trainFile, "\nand ran on", testFile)
	results.write("Trained from " + trainFile + "\nand ran on " + testFile +"\n")
	print('ACCURACY: '+str((float(num_correct / num_predictions))*100)+'%')
	results.write('ACCURACY: '+str((float(num_correct / num_predictions))*100)+'%\n\n')

	results.close()
	
if __name__ == "__main__": #treat this as a main function and keep at bottom of file
	trainFile = argv[1] #first arguement after script name should be what file is wanted (Should always be trainingSet.txt for this assignment)
	testFile = argv[2] #Second argument should be the file that we are testing our training data on

	#Build a dictionary of words from the training data
	trainDic = buildDictionary(trainFile)
	trainDic.append('classLabel')

	#Build a dictionary of words from the testing data
	testDic = buildDictionary(testFile)
	testDic.append('classLabel')
	
	#preproccess the all the data
	trainValues = makePreProccessed(trainFile, trainDic)
	testValues = makePreProccessed(testFile, testDic)
	
	#get the probabilities for the training data
	bayes_data = calculate_word_probabilities(trainDic, trainValues)
	
	#calculate how accurate the guesses are
	calculate_accuracy(trainDic, bayes_data, trainValues, trainFile, trainFile)
	calculate_accuracy(trainDic, bayes_data, testValues, trainFile, testFile)

	#add in the dictionary words to the front of the values before we put them into a file
	trainValues.insert(0, trainDic)
	testValues.insert(0, testDic)

	#put the values into a file
	generateFiles(trainValues, testValues)