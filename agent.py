
import numpy as np
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
import data_parser
from sklearn import svm

featureNum = {"sell" : 51, "bid" : 65}
modelTypes = {	"svm": "Support Vector Machine",
				"nn" : "Neural Networ",
				"lr" : "Linear Regression" }

def set_up_agents(model = "svm"):
	sellAgent = SVMAgent("sell")
	bidAgent = SVMsAgent("bid")
	return sellAgent, bidAgent

def preprocess_feature(X):
	# Preprocess the Features
	scaler = StandardScaler().fit(X)
	X = scaler.transform(X)	# Rescale the data
	return X

class SVMAgent:
	def __init__(self, targetType = "sell"):

		self.targetType = targetType
		self.dataPath = "sellingData.txt" if targetType=='sell' else "biddingData.txt"
		self.modelPath = "selling_model/svm.pkl" if targetType=='sell' else "bidding_model/svm.pkl"

	def train(self):
		# Parse the raw data to get the updated data
		data_parser.parse_raw_data()
		# Load data from the txt file
		with open(self.dataPath, 'r') as file:
			dataset = np.loadtxt(file, delimiter=" ")

		num = featureNum[self.targetType]
		X = dataset[:,0:num]	# Features
		y = dataset[:,num]		# Target

		# print "dataset: "
		# print dataset.shape
		# print "X: "
		# print X.shape
		# print type(X)
		# print "y:"
		# print y.shape

		X = preprocess_feature(X)
		# Train the Support Vector Machine model
		model = svm.SVC()
		model.fit(X,y)

		# Store the model
		joblib.dump(model, self.modelPath)

	def predict(self,agent_input):
		feature = data_parser.parse_input(agent_input)
		# print "Feature for prediction:\n"
		# print feature
		model = joblib.load(self.modelPath)
		feature = preprocess_feature(feature)
		predict = model.predict(feature)

		return int(predict[0]) # return the decision


if __name__ == "__main__":
	sellAgent = SVMAgent(targetType = "sell")
	sellAgent.train()
	print "Selling Agent trainning done\n"

	bidAgent = SVMAgent(targetType = "bid")
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

	outputDic = {'card_to_sell': 'DOG', 'bid_to_add': 2}

	sell = sellAgent.predict(inputDic)
	inputDic["stage"] = 2
	bid = bidAgent.predict(inputDic)

	print "Sell: " + str(sell) + "\nBid: " + str(bid) + "\n"


