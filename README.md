# In-depth Analysis of Felix: the Cat in the Sack
## COMP 3211 Final Project

This is an AI project for the board game "Felix the Cat". Supervised models are built to play the game
using "Support Vector Machine", "Neural Networks", "Naive Bayes'" and "Linear Regression" classifiers from
"sklearn". Unsupervised model is built using "Deep Q-Learning Networks" based on "tensorflow" as well.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
What things you need to install
* [numpy](http://www.numpy.org/) - For data manipulation
* [sklearn](http://scikit-learn.org/stable/) - For building supervised learning models
* [tensorflow](https://www.tensorflow.org/) - For building unsupervised learning model

## Running the program

Explain how to get the system running

### Before each run

The testing settings are all included in the begining of "felix.py", so check the settings before running is required.
```
(1) check the settings in the beginning of the file "felix.py".
(2) “Num_OF_PLAYER” is typically set to be 4, since the original game is for 4 gamers.
(3) “AGENT_MODES” stores the types of agents for each player you wish to assign.
(4) “AGENT_NAMES” stores the names of explicit agents to use for each player.
(5) “PRINT_MODE” decides what information to be printed.
(6) “GAME_RECORD” decides whether we store all the game information for later training.
```

### Running examples

Please note that all the demo calls are terminal commands executed at the project folder.

```
(1) Play a single game manually with random agents:
	- set “AGENT_MODES” : [0, 1, 1, 1],
	- set “NUM_OF_GAME_PLAY”: 1,
	- set “PRINT_MODE”: “a”,
	- set “GAME_RECORD”: False,
	- then execute python felix.py
```
```
(2) Set “svm” agent playing 100 games with random agents and display the winning rate:
	- set “AGENT_MODES” : [3, 1, 1, 1],
	- set “AGENT_NAMES”: [“svm”, “”, “”, “”]
	- set “NUM_OF_GAME_PLAY”: 100,
	- set “PRINT_MODE”: “g”,
	- set “GAME_RECORD”: False,
	- then execute python felix.py
```
```
(3) Set “rl” agent playing 1000 games with random agents and display the winning rate:
	- set “AGENT_MODES” : [4, 1, 1, 1],
	- set “AGENT_NAMES”: [“rl”, “”, “”, “”]
	- set “NUM_OF_GAME_PLAY”: 1000,
	- set “PRINT_MODE”: “g”,
	- set “GAME_RECORD”: False,
	- then execute python felix.py
```
```
(4) Train “svm” agent with 1000 new games played by 4 random agents:
	- first execute python "game_recorder.py" to clear all former data,
	- set “AGENT_MODES” : [1, 1, 1, 1],
	- set “NUM_OF_GAME_PLAY”: 1000,
	- set “PRINT_MODE”: “g”,
	- set “GAME_RECORD”: True,
	- then execute python felix.py to get game informations,
	- run python agent.py to train the agent,
	- use (2) to check the winning rate of the new agent.
```
```
(5) Train “rl” agent with 1000 new games played by 4 random agents:
	- first execute python "game_recorder.py" to clear all former data,
	- set “AGENT_MODES” : [1, 1, 1, 1],
	- set “NUM_OF_GAME_PLAY”: 1000,
	- set “PRINT_MODE”: “g”,
	- set “GAME_RECORD”: True,
	- then execute python felix.py to get game informations,
	- run python rl_agent.py to train the agent,
	- use (3) to check the winning rate of the new agent.
```

## Functions in each file
```
"felix.py" : Game core for playing the game.
```
```
"game_recorder.py" : Records the decisions made by the agents in "raw_data" folder while the game is played.
```
```
"data_parser.py" : Called by "agent.py" before training the machie learning models to parse "raw_data"folder and prepare 
data for feeding the models indesired format in "sellingData.txt" and "biddingData.txt"; Or called by "rl_agent.py" before 
training the reinforcement learning models to parse"raw_data" folder and prepare data for feeding the models in desired 
format in "rlsellingData.txt" and "rlbiddingData.txt";
```
```
"agent.py" : Builds the machine learning models of both selling and bidding decisions using "sklearn"and saves the model 
files to "selling_model" and "bidding_model" folders for later access.
```
```
"rl_agent.py" : Builds the reinforcement learning models of selling decisions using "tensorflow" andsaves the model to 
"DQN_model" folder.
```

## Contributors
* **LIU Qinhan** - *Model Building* - [qliuan](https://github.com/qliuan)
* **LIANG Zhibo** - *Model Building* - 
* **LIAO Kunjian** 
* **ZHANG Ziyao** - *Game Core* -
* **ZHANG Zizheng** - *Game Core* -
