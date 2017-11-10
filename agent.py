
import numpy as np
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
import data_parser

featureNum = {"sell" : 51, "bid" : 65}
modelTypes = {	"svm": "Support Vector Machine",
				"nn" : "Neural Networ",
				"lr" : "Linear Regression" }

class Agent:
	def __init__(self, targetType = "sell", modelType = "svm"):
		print "\nInit the agent\n"

		self.targetType = targetType
		self.modelType = modelType
		self.dataPath = "sellingData.txt" if targetType=='sell' else "biddingData.txt"
		self.modelPath = "selling_model/"+modelType+".pkl" if targetType=='sell' else "bidding_model/"+modelType+".pkl"

		print "\nInit the agent DONE\n"

	def train(self):
		print "\nTrain the agent\n"
		# Parse the raw data to get the updated data
		data_parser.parse_raw_data()
		# Load data from the txt file
		with open(self.dataPath, 'r') as file:
			dataset = np.loadtxt(file, delimiter=" ")
		num = featureNum[self.targetType]
		X = dataset[:,0:num-1]	# Features
		y = dataset[:,num]		# Target

		# Preprocess the Features
		scaler = StandardScaler().fit(X)
		X = scaler.transform(X)	# Rescale the data


		if self.modelType == "svm" :
			# Train the Support Vector Machine model
			model = svm_fit(X,y)

		# Store the model
		joblib.dump(model, self.modelPath)

		print "\nTrain the agent DONE\n"

	def predict(self,agent_input):
		feature = data_parser.parse_input(agent_input)
		model = joblib.load(self.modelPath)

		return int(model.predict(feature))

def svm_fit(X,y):
	from sklearn import svm
	model = svm.SVC()
	model.fit(X,y)


def set_up_agents(model = "svm"):
	sellAgent = Agent("sell", model)
	bidAgent = Agent("bid", model)
	return sellAgent, bidAgent

if __name__ == "__main__":
	sellAgent = Agent(targetType = "sell", modelType = "svm")
	sellAgent.train()
	print "Selling Agent trainning done\n"

	bidAgent = Agent(targetType = "bid", modelType = "svm")
	bidAgent.train()
	print "Bidding Agent trainning done\n"

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

	sell = sellAgent.predict(inputDic)
	inputDic["stage"] = 2
	bid = bidAgent.predict(inputDic)

	print "Sell: " + str(sell) + " Bid: " + str(bid)


