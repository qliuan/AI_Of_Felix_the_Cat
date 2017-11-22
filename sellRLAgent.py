from RL_brain import DeepQNetwork
import numpy as np
import data_parser

SELL_ACTIONS = 10
SELL_FEATURES = 51

def train_from_data():
	rldataPath = "rlsellingData.txt"

	with open(rldataPath, 'r') as file:
		dataset = np.loadtxt(file, delimiter=" ")

	for i in range(dataset.shape[0]):
		episode = dataset[i,:]
		np.reshape(episode,104)
		# print(episode.shape)
		# State: 0-50, Action: 51, Reward: 52, Next State: 53-103

		# RL.store_transition(state, action, reward, state_)
		RL.store_transition(episode)

		if (i > 200) and (i % 5 == 0):
			print("RL Learning " + str(float(i)/dataset.shape[0]))
			RL.learn()
			if(i % 1000 == 0):
				RL.save()


	RL.save()
	return




def test():
	RL.load()

	inputDic = {'my_index': 1,
		'stage': 1,
		'current_highest_bid': 8,
		'starting_player_index': 3,
		'round': 2,
		'central_series_public': ['*', '*', '*', '*'],
		'reward_pointer': 2,
		'players_public':
		[
		{'token': 4, 'skipped': False, 'score': 20, 'bid': 0, 'show_deck_public': ['+3', '+11', 'dog', 'DOG', '-5', '0', '+5', '+8', '-8']},
		{'token': 15, 'skipped': False, 'score': 0, 'bid': 0, 'show_deck_public': ['+3', '+11', '+15', 'dog', '-5', '0', '+5', '+8', '-8']},
		{'token': 15, 'skipped': False, 'score': 0, 'bid': 0, 'show_deck_public': ['+3', '+11', '+15', 'dog', 'DOG', '-5', '0', '+5', '+8']},
		{'token': 15, 'skipped': False, 'score': 0, 'bid': 0, 'show_deck_public': ['+3', '+11', '+15', 'dog', 'DOG', '-5', '+5', '+8', '-8']}
		]
	}

	action = decide(inputDic)

	print(action)
	input("Testing Action")



if __name__ == "__main__":

    # Parse the data properly
	# data_parser.rl_parse_raw_data()

	RL = DeepQNetwork(SELL_ACTIONS, SELL_FEATURES,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      output_graph=False
                      )

	test()

	train_from_data()

	print("Displaying the cost...")
	RL.plot_cost()