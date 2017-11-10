## Record the game information
## The directory tree:
## raw_data
##		games_played.txt
##		game1
##			selling.txt
##			bidding.txt
##			result.txt

import os

## Transform from Boolean T/F to Integer 1/0
BtoI = {'True': 1, 'False': 0}

## Transform the Deck to Target
DtoT = {'+3': 0, '+5': 1, '+8': 2, '+11': 3, '+15': 4, '0': 5, '-5': 6, '-8': 7, 'dog': 8, 'DOG': 9, '*': 10}

## Set the game folder for recording
def set_recording():
	num = get_games_played(game_incre = True)
	# print("games_played " + str(num))
	path = "raw_data/game" + str(num+1)
	if not os.path.exists(path):
		os.makedirs(path)
		os.makedirs(path + "/player0")
		os.makedirs(path + "/player1")
		os.makedirs(path + "/player2")
		os.makedirs(path + "/player3")

	return

def get_games_played(game_incre = True, sell_incre = 0, bid_incre = 0):
	# Read the number of games played and update it
	with open("raw_data/games_played.txt", 'r') as f:
		count_list = f.read().split('\n')
		game = int(count_list[0])
		sell = int(count_list[1])
		bid  = int(count_list[2])

	with open("raw_data/games_played.txt", 'w') as file:
		if (game_incre):
			file.write(str(game+1) + '\n')
		else:
			file.write(str(game) + '\n')

		file.write(str(sell + sell_incre) + '\n')
		file.write(str(bid  + bid_incre))

	return game

def decision_count(gamePath, player, sell_incre = False, bid_incre = False):
	# Read the number of decisions and update it
	filePath = gamePath + "/player" + str(player) + '/decision_counts.txt'
	if not os.path.exists(filePath):
		with open(filePath, 'w') as f:
			f.write('0\n0')

	with open(filePath, 'r') as f:
		count_list = f.read().split('\n')
		sell = int(count_list[0])
		bid  = int(count_list[1])

	with open(filePath, 'w') as file:
		if (sell_incre):
			file.write(str(sell+1) + '\n')
		else:
			file.write(str(sell) + '\n')
		if (bid_incre):
			file.write(str(bid+1))
		else:
			file.write(str(bid))

	return sell,bid


## Recording a decision
def decision_recorder(agent_input, agent_output):
	num = get_games_played(game_incre = False)
	gamePath = "raw_data/game" + str(num)
	player = agent_input['my_index']
	if(agent_input['stage'] == 1):
		## Increment the counter
		decision_count(gamePath, player, sell_incre = True, bid_incre = False)
		## Selling stage
		with open(gamePath + "/player" + str(player) + "/selling.txt", 'a') as sellFile:
			sellFile.write(
				"## Round information\n" +

				str(agent_input['starting_player_index']) + " " +
				str(agent_input['round']) + "\n" +

				"## Player information\n" +

				str(agent_input['my_index']) + "\n"
			)

			for i in range(4):
				sellFile.write(
					str(agent_input['players_public'][i]['token']) + " " +
					str(agent_input['players_public'][i]['score']) + " "
				)

				sellFile.write(
					str(BtoI[ str( '+3' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " " +
					str(BtoI[ str( '+5' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " " +
					str(BtoI[ str( '+8' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " " +
					str(BtoI[ str( '+11' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " " +
					str(BtoI[ str( '+15' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " " +
					str(BtoI[ str( '0' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " " +
					str(BtoI[ str( '-5' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " " +
					str(BtoI[ str( '-8' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " " +
					str(BtoI[ str( 'dog' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " " +
					str(BtoI[ str( 'DOG' in agent_input['players_public'][i]['show_deck_public'] ) ]) + "\n"
				)

			sellFile.write(
				"## Decision\n" +

				str(DtoT[ agent_output['card_to_sell'] ]) +

				"\n\n" # One Epison ends
			)


	else:
		## Increment the counter
		decision_count(gamePath, player, sell_incre = False, bid_incre = True)
		## Bidding stage
		with open(gamePath + "/player" + str(player) + "/bidding.txt", 'a') as bidFile:
			bidFile.write(
				"## Bidding information\n" +

				str(agent_input['starting_player_index']) + " " +
				str(agent_input['round']) + " " +
				str(agent_input['current_highest_bid']) + " " +
				str(agent_input['reward_pointer']) + " " +
				str(DtoT[ agent_input['central_series_public'][0] ]) + " " +
				str(DtoT[ agent_input['central_series_public'][1] ]) + " " +
				str(DtoT[ agent_input['central_series_public'][2] ]) + " " +
				str(DtoT[ agent_input['central_series_public'][3] ]) + "\n" +

				"## Player information\n" +

				str(agent_input['my_index']) + "\n"
			)

			for i in range(4):
				bidFile.write(
					str(agent_input['players_public'][i]['token']) + " " +
					str(agent_input['players_public'][i]['score']) + " " +
					str(BtoI[ str( agent_input['players_public'][i]['skipped'] ) ]) + " " +
					str(agent_input['players_public'][i]['bid']) + " "
				)

				bidFile.write(

					str(BtoI[ str( '+3' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " " +
					str(BtoI[ str( '+5' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " " +
					str(BtoI[ str( '+8' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " " +
					str(BtoI[ str( '+11' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " " +
					str(BtoI[ str( '+15' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " " +
					str(BtoI[ str( '0' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " " +
					str(BtoI[ str( '-5' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " " +
					str(BtoI[ str( '-8' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " " +
					str(BtoI[ str( 'dog' in agent_input['players_public'][i]['show_deck_public'] ) ]) + " " +
					str(BtoI[ str( 'DOG' in agent_input['players_public'][i]['show_deck_public'] ) ]) + "\n"
				)

			bidFile.write(
				"## Decision\n" +

				str(agent_output['bid_to_exceed']) +

				"\n\n" # One Epison ends
			)

	return

# result = {'winner':1, 'total_scores':[30,40,64,120]}
def result_recorder(result):
	# Record the result of the game
	num = get_games_played(game_incre = False)
	gamePath = "raw_data/game" + str(num)
	with open(gamePath + "/result.txt", 'w') as reFile:
		reFile.write(str(result['winner']) + "\n")
		reFile.write(str(result['total_scores'][0]) + " " + str(result['total_scores'][1]) + " " +
					str(result['total_scores'][2]) + " " + str(result['total_scores'][3]))
	# Count the winner to the games_played file
	player = result['winner']
	sell,bid = decision_count(gamePath,player,0,0)
	get_games_played(game_incre = False, sell_incre = sell, bid_incre = bid)



def test():
	# show_deck_public = ['+3', '+11', '+15', 'dog', 'DOG', '-5', '0', '+5', '+8', '-8']
	# print('+3' in show_deck_public)
	# print(BtoI[str('+3' in show_deck_public)])

	inputDic = {'my_index': 0,
		'stage': 1,            # 1 for Selling Stage, 2 for Bidding Stage
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

	outputDic = {'card_to_sell': 'DOG', 'bid_to_add': 2}

	resultDic = {'winner': 0, 'total_scores': [40,129,52,41]}

	# import ast
	# dic = {"a":1, "b":2}
	# s = str(dic)
	# input = ast.literal_eval(input)
	# output = ast.literal_eval(output)
	# print("Input:\n")
	# print(inputDic)
	# print("Output:\n")
	# print(outputDic)

	for i in range(10):
		inputDic['stage'] = 1
		decision_recorder(inputDic,outputDic)
		inputDic['stage'] = 2
		decision_recorder(inputDic,outputDic)

	result_recorder(resultDic)

	# import decision_printer
	# decision_printer(inputDic,outputDic)
	# inputDic['stage'] = 2
	# decision_printer(inputDic,outputDic)

if __name__ == '__main__':
	test()
	# get_games_played(True,True,True)