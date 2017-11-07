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
	num = get_games_played(increment = True)
	# print("games_played " + str(num))
	path = "raw_data/game" + str(num+1)
	if not os.path.exists(path):
		os.makedirs(path)
		os.makedirs(path + "/player0")
		os.makedirs(path + "/player1")
		os.makedirs(path + "/player2")
		os.makedirs(path + "/player3")

	return

def get_games_played(increment = True):
	# Read the number of games played and update it
	with open("raw_data/games_played.txt", 'r') as f:
		num = int(f.read())

	if (increment):
		with open("raw_data/games_played.txt", 'w') as file:
			file.write(str(num+1))

	return num

## Recording a decision
def decision_recorder(agent_input, agent_output):
	num = get_games_played(increment = False)
	gamePath = "raw_data/game" + str(num)
	player = agent_input['my_index']
	if(agent_input['stage'] == 1):
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

				str(DtoT[ agent_output['card_to_sell'] ]) +

				"\n\n" # One Epison ends
			)

	return

# Record the result of the game
# result = {'winner':1, 'score':[30,40,64,120]}
def result_recorder(result):
	num = get_games_played(increment = False)
	gamePath = "raw_data/game" + str(num)
	with open(gamePath + "/result.txt", 'a') as reFile:
		reFile.write(str(result['winner']) + "\n")
		reFile.write(str(result['score'][0]) + " " + str(result['score'][1]) + " " +
					str(result['score'][2]) + " " + str(result['score'][3]) + "\n")



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

	# import ast
	# dic = {"a":1, "b":2}
	# s = str(dic)
	# input = ast.literal_eval(input)
	# output = ast.literal_eval(output)
	# print("Input:\n")
	# print(inputDic)
	# print("Output:\n")
	# print(outputDic)

	decision_recorder(inputDic,outputDic)
	inputDic['stage'] = 2
	decision_recorder(inputDic,outputDic)

	# decision_printer(inputDic,outputDic)
	# inputDic['stage'] = 2
	# decision_printer(inputDic,outputDic)

def decision_printer(agent_input, agent_output):

	if(agent_input['stage'] == 1):
		## Selling stage
		print(
				"## Round information\n" +

				str(agent_input['starting_player_index']) + " " +
				str(agent_input['round']) + "\n" +

				"## Player information\n" +

				str(agent_input['my_index']) + "\n"
			)

		for i in range(4):
			print(
				str(agent_input['players_public'][i]['token']) + " " +
				str(agent_input['players_public'][i]['score']) + " "
			)

			print(
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

		print(
			"## Decision\n" +

			str(DtoT[ agent_output['card_to_sell'] ]) +

			"\n\n" # One Epison ends
		)
	else:
		print(
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
			print(
				str(agent_input['players_public'][i]['token']) + " " +
				str(agent_input['players_public'][i]['score']) + " " +
				str(BtoI[ str( agent_input['players_public'][i]['skipped'] ) ]) + " " +
				str(agent_input['players_public'][i]['bid']) + " "
			)

			print(

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

		print(
			"## Decision\n" +

			str(DtoT[ agent_output['card_to_sell'] ]) +

			"\n\n" # One Epison ends
		)

if __name__ == '__main__':
	# set_recording()
	test()
