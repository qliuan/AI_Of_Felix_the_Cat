
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
	modelPath = "selling_model/svm.pkl"
		self.targetType = targetType
		self.modelType = modelType
		self.dataPath = "sellingData.txt" if targetType=='sell' else "biddingData.txt"
		self.modelPath = "selling_model/"+modelType+".pkl" if targetType=='sell' else "bidding_model/"+modelType+".pkl"

	def train(self):
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
		joblib.dum(model, modelPath)

	def load_model():
		return joblib.load(modelPath)

	def predict(angent_input):
		feature = data_parser.parse_input(agent_input)
		model = load_model()
		return int(model.predict(feature))

	def svm_fit(X,y):
		from sklearn import svm
		model = svm.SVC()
		model.fit(X,y)


def set_up_agents(model = "svm"):
	sellAgent = Agent("sell", model)
	bidAgent = agent = Agent("bid", model)
	return sellAgent, bidAgent

if __name__ == "__main__":
	sellAgent = Agent(targetType = "sell", modelType = "svm")
	sellAgent.train()

	bidAgent = Agent(targetType = "bid", modelType = "svm")
	bidAgent.train()


