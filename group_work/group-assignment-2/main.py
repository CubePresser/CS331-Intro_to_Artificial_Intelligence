import os, string
from sys import argv

def readFromFile(fileName):
    file = open(fileName, "r") #open our given file with read only permissions
    for line in file:
        return #delete this its just for now
        #TODO: separate line into words and num
        #alphebetize words in master list
        
    return

def stripPunctuation(sentence):
    sentence = sentence.translate(None, string.punctuation)
    return sentence

if __name__ == "__main__": #treat this as a main function and keep at bottom of file
    fileName = argv[1] #first arguement after script name should be what file is wanted
    readFromFile(fileName)

    words = "This isn't a punctuation test. WOW! ..,, Coor's"
    print(stripPunctuation(words).lower())