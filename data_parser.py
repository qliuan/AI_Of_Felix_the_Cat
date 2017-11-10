import os
import numpy as np
featureNum = {"sell" : 51, "bid" : 65}
## Transform from Boolean T/F to Integer 1/0
BtoI = {'True': 1, 'False': 0}

## Transform the Deck to Target
DtoT = {'+3': 0, '+5': 1, '+8': 2, '+11': 3, '+15': 4, '0': 5, '-5': 6, '-8': 7, 'dog': 8, 'DOG': 9, '*': 10}

def parse_raw_data():
	rawDataPath = "raw_data"
	sellingDataPath = "sellingData.txt"
	biddingDataPath = "biddingData.txt"
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

	while(True):
		text = raw.readline()
		# print "Text: " + text # text = "## Round information\n"
		if text == '':
			break
		episode = raw.readline().rstrip() + " "
		raw.readline() # "## Player information\n"
		episode += raw.readline().rstrip() + " "
		episode += raw.readline().rstrip() + " "
		episode += raw.readline().rstrip() + " "
		episode += raw.readline().rstrip() + " "
		episode += raw.readline().rstrip() + " "
		raw.readline() # "## Decision"
		episode += raw.readline().rstrip() + "\n"
		raw.readline() # "\n"

		# print "Episode Done:\n" + episode
		# raw_input('Enter your input:')
		data.write(episode)

def empty_data(path):
	open(path, 'w').close()

def parse_input(agent_input):
	featureStr = ""
	if(agent_input['stage'] == 1):
		## Selling stage
		targetType = 'sell'
		featureStr += 	str(agent_input['starting_player_index']) + " " + str(agent_input['round']) + " " + str(agent_input['my_index']) + " "

		for i in range(4):
			featureStr += str(agent_input['players_public'][i]['token']) + " " + str(agent_input['players_public'][i]['score']) + " "

			featureStr +=	str(BtoI[ str( '+3' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " "
			featureStr +=	str(BtoI[ str( '+5' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " "
			featureStr +=	str(BtoI[ str( '+8' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " "
			featureStr +=	str(BtoI[ str( '+11' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " "
			featureStr +=	str(BtoI[ str( '+15' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " "
			featureStr +=	str(BtoI[ str( '0' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " "
			featureStr +=	str(BtoI[ str( '-5' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " "
			featureStr +=	str(BtoI[ str( '-8' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " "
			featureStr +=	str(BtoI[ str( 'dog' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " "
			featureStr +=	str(BtoI[ str( 'DOG' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " "

	else:
		targetType = 'bid'
		featureStr += str(agent_input['starting_player_index']) + " " + str(agent_input['round']) + " " + str(agent_input['current_highest_bid']) + " " + str(agent_input['reward_pointer']) + " " + str(DtoT[ agent_input['central_series_public'][0] ]) + " " + str(DtoT[ agent_input['central_series_public'][1] ]) + " " + str(DtoT[ agent_input['central_series_public'][2] ]) + " " + str(DtoT[ agent_input['central_series_public'][3] ]) + " " + str(agent_input['my_index']) + " "

		for i in range(4):
			featureStr += str(agent_input['players_public'][i]['token']) + " " + str(agent_input['players_public'][i]['score']) + " " + str(BtoI[ str( agent_input['players_public'][i]['skipped'] ) ]) + " " + str(agent_input['players_public'][i]['bid']) + " "

			featureStr += str(BtoI[ str( '+3' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " "
			featureStr += str(BtoI[ str( '+5' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " "
			featureStr += str(BtoI[ str( '+8' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " "
			featureStr += str(BtoI[ str( '+11' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " "
			featureStr += str(BtoI[ str( '+15' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " "
			featureStr += str(BtoI[ str( '0' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " "
			featureStr += str(BtoI[ str( '-5' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " "
			featureStr += str(BtoI[ str( '-8' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " "
			featureStr += str(BtoI[ str( 'dog' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " "
			featureStr += str(BtoI[ str( 'DOG' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " "

	# print "Feature String:\n" + featureStr.rstrip()

	with open("feature.txt", 'w') as file:
		file.write(featureStr.rstrip())

	feature = np.loadtxt("feature.txt", delimiter=" ")
	num = featureNum[targetType]
	print "feature: "
	print feature.shape

	X = feature.reshape(1,num) # Features

	print "X: "
	print X.shape

	return X



def test():

	inputDic = {'my_index': 0,
		'stage': 1,
		'current_highest_bid': 8,
		'starting_player_index': 3,
		'round': 4,
		'central_series_public': ['+8', 'DOG', '-5', '+15'],
		'reward_pointer': 2,
		'players_public':
		[
		{'token': 4, 'skipped': True, 'score': 20, 'bid': 0, 'show_deck_public': ['+3', '+11', 'dog', 'DOG', '-5', '0', '+5', '+8', '-8']},
		{'token': 15, 'skipped': False, 'score': 0, 'bid': 4, 'show_deck_public': ['+3', '+11', '+15', 'dog', '-5', '0', '+5', '+8', '-8']},
		{'token': 15, 'skipped': False, 'score': 0, 'bid': 8, 'show_deck_public': ['+3', '+11', '+15', 'dog', 'DOG', '-5', '0', '+5', '+8']},
		{'token': 15, 'skipped': False, 'score': 0, 'bid': 6, 'show_deck_public': ['+3', '+11', '+15', 'dog', 'DOG', '-5', '+5', '+8', '-8']}
		]
	}

	parse_input(inputDic)
	inputDic['stage'] = 2
	parse_input(inputDic)

if __name__ == '__main__':
	parse_raw_data()
	# test()