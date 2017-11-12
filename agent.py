import numpy as np
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
import data_parser
from sklearn.svm import SVC, NuSVC, LinearSVC 		# For Support Vector Machine
from sklearn.neural_network import MLPClassifier 	# For Neural Network
from sklearn.naive_bayes import GaussianNB			# For Naive Bayes
from sklearn.tree import DecisionTreeClassifier  	# For Decision Tree
from sklearn.linear_model import LinearRegression	# For Linear Regression

featureNum = {"sell" : 51, "bid" : 65}
modelTypes = {	"svm": "Support Vector Machine",
				"nn" : "Neural Networ",
				"nb" : "Naive Bayes",
				"dt" : "Decision Tree",
				"lr" : "Linear Regression" }

# Transform from Target to Deck
TtoD = {'0':'+3','1': '+5','2': '+8','3': '+11','4': '+15','5': '0','6': '-5','7': '-8','8': 'dog','9': 'DOG'}

def set_up_agents(model = "svm"):
	sellAgent = SVMAgent("sell")
	bidAgent = SVMsAgent("bid")
	return sellAgent, bidAgent

def preprocess_feature(X):
	# Preprocess the Features
	scaler = StandardScaler().fit(X)
	X = scaler.transform(X)	# Rescale the data
	return X

# Base class of all agents
class Agent:
	def __init__(self, targetType, modelPath):
		# print("Init the base class")
		self.targetType = targetType
		self.modelPath = modelPath

	def predict(self,agent_input):
		feature = data_parser.parse_input(agent_input)
		# print "Feature for prediction:\n"
		# print feature
		model = joblib.load(self.modelPath)
		feature = preprocess_feature(feature)
		predict = model.predict(feature)

		# return the decision
		if (self.targetType == 'bid'):
			return int(predict[0])
		else:
			return TtoD[str(int(predict[0]))]


class SVMAgent(Agent):
	def __init__(self, targetType = "sell"):
		# print("Init the derived class")
		self.targetType = targetType
		self.dataPath = "sellingData.txt" if targetType=='sell' else "biddingData.txt"
		self.modelPath = "selling_model/svm.pkl" if targetType=='sell' else "bidding_model/svm.pkl"
		Agent.__init__(self, self.targetType, self.modelPath)

	def train(self):
		# Parse the raw data to get the updated data
		data_parser.parse_raw_data()
		# Load data from the txt file
		with open(self.dataPath, 'r') as file:
			dataset = np.loadtxt(file, delimiter=" ")

		num = featureNum[self.targetType]
		X = dataset[:,0:num]	# Features
		y = dataset[:,num]		# Target

		X = preprocess_feature(X)
		# Train the Support Vector Machine model with different classes
		model = SVC(kernel = 'linear').fit(X, y)
		# model = SVC(kernel = 'rbf'	 ).fit(X, y)

		# model = NuSVC(kernel = 'linear').fit(X,y)
		# model = NuSVC(kernel = 'rbf'   ).fit(X,y)

		# model = LinearSVC(multi_class = 'ovr').fit(X,y)
		# model = LinearSVC(multi_class = 'crammer_singer').fit(X,y)

		# Store the model
		joblib.dump(model, self.modelPath)


class NNAgent(Agent):
	def __init__(self, targetType = "sell"):
		self.targetType = targetType
		self.dataPath = "sellingData.txt" if targetType=='sell' else "biddingData.txt"
		self.modelPath = "selling_model/nn.pkl" if targetType=='sell' else "bidding_model/nn.pkl"
		Agent.__init__(self, self.targetType, self.modelPath)

	def train(self):
		# Parse the raw data to get the updated data
		data_parser.parse_raw_data()
		# Load data from the txt file
		with open(self.dataPath, 'r') as file:
			dataset = np.loadtxt(file, delimiter=" ")

		num = featureNum[self.targetType]
		X = dataset[:,0:num]	# Features
		y = dataset[:,num]		# Target

		X = preprocess_feature(X)
		# Train the Neural Network model
		model = MLPClassifier(solver='adam', activation='relu', hidden_layer_sizes = (10,), max_iter = 10000, alpha = 1e-5).fit(X, y)

		# Store the model
		joblib.dump(model, self.modelPath)


class NBAgent(Agent):
	def __init__(self, targetType = "sell"):
		self.targetType = targetType
		self.dataPath = "sellingData.txt" if targetType=='sell' else "biddingData.txt"
		self.modelPath = "selling_model/nb.pkl" if targetType=='sell' else "bidding_model/nb.pkl"
		Agent.__init__(self, self.targetType, self.modelPath)

	def train(self):
		# Parse the raw data to get the updated data
		data_parser.parse_raw_data()
		# Load data from the txt file
		with open(self.dataPath, 'r') as file:
			dataset = np.loadtxt(file, delimiter=" ")

		num = featureNum[self.targetType]
		X = dataset[:,0:num]	# Features
		y = dataset[:,num]		# Target

		X = preprocess_feature(X)
		# Train the Naive Bayes model
		model = GaussianNB().fit(X, y)

		# Store the model
		joblib.dump(model, self.modelPath)


class DTAgent(Agent):
	def __init__(self, targetType = "sell"):
		self.targetType = targetType
		self.dataPath = "sellingData.txt" if targetType=='sell' else "biddingData.txt"
		self.modelPath = "selling_model/dt.pkl" if targetType=='sell' else "bidding_model/dt.pkl"
		Agent.__init__(self, self.targetType, self.modelPath)

	def train(self):
		# Parse the raw data to get the updated data
		data_parser.parse_raw_data()
		# Load data from the txt file
		with open(self.dataPath, 'r') as file:
			dataset = np.loadtxt(file, delimiter=" ")

		num = featureNum[self.targetType]
		X = dataset[:,0:num]	# Features
		y = dataset[:,num]		# Target

		X = preprocess_feature(X)
		# Train the Decision Tree model
		model = DecisionTreeClassifier().fit(X, y)

		# Store the model
		joblib.dump(model, self.modelPath)



class LRAgent(Agent):
	def __init__(self, targetType = "sell"):
		self.targetType = targetType
		self.dataPath = "sellingData.txt" if targetType=='sell' else "biddingData.txt"
		self.modelPath = "selling_model/lr.pkl" if targetType=='sell' else "bidding_model/lr.pkl"
		Agent.__init__(self, self.targetType, self.modelPath)

	def train(self):
		# Parse the raw data to get the updated data
		data_parser.parse_raw_data()
		# Load data from the txt file
		with open(self.dataPath, 'r') as file:
			dataset = np.loadtxt(file, delimiter=" ")

		num = featureNum[self.targetType]
		X = dataset[:,0:num]	# Features
		y = dataset[:,num]		# Target

		X = preprocess_feature(X)
		# Train the Linear Regression model
		model = LinearRegression().fit(X, y)

		# Store the model
		joblib.dump(model, self.modelPath)


if __name__ == "__main__":
	# "svm": "Support Vector Machine",
	# "nn" : "Neural Networ",
	# "nb" : "Naive Bayes",
	# "dt" : "Decision Tree",
	# "lr" : "Linear Regression"
	sellAgent = NBAgent(targetType = "sell")
	# sellAgent.train()
	# print("Selling Agent trainning done\n")

	bidAgent = NBAgent(targetType = "bid")
	# bidAgent.train()
	# print("Bidding Agent trainning done\n")

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

	print("Sell: " + sell + "\nBid: " + str(bid) + "\n")


