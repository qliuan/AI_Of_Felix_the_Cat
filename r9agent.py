import numpy as np
import random
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
import data_parser
from sklearn.svm import SVC, NuSVC, LinearSVC 		# For Support Vector Machine

featureNum = {"sell" : 52*8 + 51, "bid" : 66*8 + 65}

# Transform from Target to Deck
TtoD = {'0':'+3','1': '+5','2': '+8','3': '+11','4': '+15','5': '0','6': '-5','7': '-8','8': 'dog','9': 'DOG'}

# Preprocess data
import os
import numpy as np
featureNum = {"sell" : 51, "bid" : 65}
## Transform from Boolean T/F to Integer 1/0
BtoI = {'True': 1, 'False': 0}

## Transform the Deck to Target
DtoT = {'+3': 0, '+5': 1, '+8': 2, '+11': 3, '+15': 4, '0': 5, '-5': 6, '-8': 7, 'dog': 8, 'DOG': 9, '*': 10}

def empty_data(path):
	open(path, 'w').close()

def parse_raw_data():
	rawDataPath = "raw_data"
	sellingDataPath = "selling_data/r9sellingData.txt"
	biddingDataPath = "bidding_data/r9biddingData.txt"
	empty_data(biddingDataPath)
	empty_data(sellingDataPath)

	for folder in os.listdir(rawDataPath):
		if '.' in folder: # Skip "result.txt" and files starting with "."
			continue
		folderPath = rawDataPath + "/" + folder
		resultPath = folderPath + "/result.txt"
		with open(resultPath, 'r') as resultFile:
			winner = resultFile.readline().rstrip() # Get the winner index
		winnerPath = folderPath + "/player" + winner
		sellingPath = winnerPath + "/selling.txt"
		biddingPath = winnerPath + "/bidding.txt"

		# print "SellingPath: " + sellingPath
		# print "BiddingPath: " + biddingPath

		# Handling the parsing of selling data
		parse_file(sellingPath, sellingDataPath)

		# Handling the parsing of selling data
		parse_file(biddingPath, biddingDataPath)

def parse_file(rawDataFile, dataFile):
	data = open(dataFile, 'a')
	raw  = open(rawDataFile, 'r')
	episode = ""
	print("raw data file: " + rawDataFile)

	while(True):
		skip = False
		text = raw.readline()
		# text = "## Round information\n"
		if text == '':
			break
		roundLine = raw.readline().rstrip() + " "
		roun = roundLine

		if (roundLine.split(" ")[1] != "9"):
			# print("Skipping round " + episode.split(" ")[1] )
			skip = True

		raw.readline() # "## Player information\n"
		roun += raw.readline().rstrip() + " "
		roun += raw.readline().rstrip() + " "
		roun += raw.readline().rstrip() + " "
		roun += raw.readline().rstrip() + " "
		roun += raw.readline().rstrip() + " "
		raw.readline() # "## Decision"
		roun += raw.readline().rstrip() + " "
		raw.readline() # "\n"

		episode += roun

		# print "Episode Done:\n" + episode
		# raw_input('Enter your input:')
		if (skip):
			# print(roun.split(" "))
			# print("Length of the round: " + str(len(roun.split(" "))))
			continue

		# print(episode.split(" "))
		# print("Length: " + str(len(episode.split(" "))) )
		# input("Input")
		data.write(episode + "\n")
		break

def preprocess_feature(X):
	# Preprocess the Features
	scaler = StandardScaler().fit(X)
	X = scaler.transform(X)	# Rescale the data
	return X






if __name__ == "__main__":
	parse_raw_data()