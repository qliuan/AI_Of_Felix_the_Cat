COMP 3211 Final Project
"Felix the Cat"

'''''
The directory tree for recording the data
## scripts
## raw_data
	## games_played.txt (games_counter = N, selling_counter = 10N, bidding_counter = B)
	## game1
		## player0
			## decision_counts.txt
			## selling.txt (all selling decisions of player0)
			## bidding.txt (all bidding decisions of player0)
		## player1
		## player2
		## player3
		## result.txt (result for this game)
	## game2
	...
	## gameN


Train Reinforcement Learning Model
Step 1: call game_recorder.py to clear former data
Step 2: set the parameters in felix.py and run it to get new data
Step 3: run rl_agent.py to train the model and display the cost curve
Step 4: run felix.py to check the winning rate