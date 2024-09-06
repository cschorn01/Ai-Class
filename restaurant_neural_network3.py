# Names: Chris Schorn & Kyle Wiseman
# Date: 03/05/2020
# Class: CSC-3250-01
# Description: A neural network to predict the answer
#              to the restaurant problem
# Went through tutorial for Neural Network code where we received the program skeleton
# Weights retrieved from Ty Carlson's backprop training, for accuracy

import sys
import random
import numpy as np

class NeuralNetwork:
    def __init__(self, x, y):
        self.input      = x #x is a numpy array of ten elements which are our input nodes
        #wights on the 40 edges from the input layer of 10 nodes to the hidden layer of 4 nodes
        self.weights1   = np.array([[ 1.80211363, -1.50873888, -0.94147185, -0.79831498],
                                    [-0.13147908, -0.80839076, -0.62059839, -0.3137698 ],
                                    [ 1.42927657, -0.08204222, -1.29081023, -0.30977364],
                                    [-1.74793046,  2.88818072, -2.40292266, -0.49925852],
                                    [-0.6660301,  1.41518973, -3.26328919, -0.56915666],
                                    [ 0.3412899,  -0.9110038,  -1.06635527, -0.25594204],
                                    [ 1.5580474,   2.65406701,  2.94757246, -1.27703115],
                                    [-1.22800068,  0.28542618, -1.85904094, -0.55042992],
                                    [ 2.9430186,  -3.88059606,  1.05579981, -0.70401264],
                                    [-0.31349907, -0.16537433, -0.98171172, -0.24985569]])
        #weights on the edges from the hidden layer of 4 nodes to the output layer of 1 nodes
        self.weights2   = np.array([-4.0621176,7.11836102, -5.43405124, 1.25319457])
        self.y          = y
        self.output     = np.zeros(self.y.shape)

    # sigmoid activation function
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    # feed forward function that passes the dot product of weights and input to the layer
    def feedforward(self):
        #dot product of input layer and their weights to hidden layer passed to sigmoid function
        self.layer1 = self.sigmoid(np.dot(self.input, self.weights1))
        #dot product of hidden layer and their weights to output layer passed to sigmoid function
        self.output = self.sigmoid(np.dot(self.layer1, self.weights2))

        #printing the result of output
        print(self.output)

# Function to turn user answers into number form for yes/no questions
def convertBinary(answer):
    if(answer == "yes"):
        return 1
    elif(answer == "no"):
        return 0
    else:
        print("Error: Invalid input.")
        return 0
# Function to turn user answers for patrons into numbers
def convertPatrons(answer):
    if(answer == "full"):
        return .5
    elif(answer == "some"):
        return 1
    elif(answer == "none"):
        return 0
    else:
        print("Error: Invalid input.")
        return 0
# Function to convert price answer to number
def convertPrice(answer):
    if(answer == "$"):
        return 1
    elif(answer == "$$"):
        return .5
    elif(answer == "$$$"):
        return 0
    else:
        print("Error: Invalid input.")
        return 0
# Function to convert answer to number
def convertType(answer):
    if(answer == "french"):
        return .33
    elif(answer == "thai"):
        return 1
    elif(answer == "burger"):
        return 0
    elif(answer == "italian"):
        return .66
    else:
        print("Error: Invalid input.")
        return 0
# Function to convert answer to estimate
def convertEst(answer):
    if(answer == "0-10"):
        return 1
    elif(answer == "10-30"):
        return .33
    elif(answer == "30-60"):
        return .66
    elif(answer == ">60"):
        return 0
    else:
        print("Error: Invalid input.")
        return 0

# training_inputs = np.array([
#                    [1, 0, 0, 1, .5,  1, 0, 1, .33, 0],
#                    [1, 0, 0, 1,  1,  0, 0, 0,   1, 0],
#                    [0, 1, 0, 0, .5,  0, 0, 0,   0, 0],
#                    [1, 0, 1, 1,  1,  0, 1, 0,   1, 0],
#                    [1, 0, 1, 0,  1,  1, 0, 1, .33, 0],
#                    [0, 1, 0, 1, .5, .5, 1, 1, .66, 0],
#                    [0, 1, 0, 0,  0,  0, 1, 0,   0, 0],
#                    [0, 0, 0, 1, .5, .5, 1, 1,   1, 0],
#                    [0, 1, 1, 0,  1,  0, 1, 0,   1, 0],
#                    [1, 1, 1, 1,  1,  1, 0, 1, .66, 0],
#                    [0, 0, 0, 0,  0,  0, 0, 0,   1, 0],
#                    [1, 1, 1, 1,  1,  0, 0, 0,   0, 0]
#                   ])
#
#
# # training_outputs = np.array([[1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1]]).T
#
# # for j in range(500):
# for i in range(12):
#     x = training_inputs[i]
#     y = np.zeros(4)
#     NN = NeuralNetwork(x, y)
#     NN.feedforward()

# Prompting user for all attributes related to data and decision
alt = (convertBinary(input("Is there an alternative? (yes/no): ")))
bar = (convertBinary(input("Is there a bar? (yes/no): ")))
fri = (convertBinary(input("Is it Friday? (yes/no): ")))
hun = (convertBinary(input("Are you hungry? (yes/no): ")))
pat = (convertPatrons(input("How many patrons are there? (full/some/none): ")))
price = (convertPrice(input("How expensive is the restaurant? ($/$$/$$$): ")))
rain = (convertBinary(input("Is it raining? (yes/no): ")))
res = (convertBinary(input("Does the restaurant accept reservations? (yes/no): ")))
type = (convertType(input("What type of food does the restaurant have? (french/thai/burger/italian): ")))
est = (convertEst(input("What is the estimated wait time? (0-10/10-30/30-60/>60): ")))

# Creating an array of answers to pass to neural network
x = np.array([alt, bar, fri, hun, pat, price, rain, res, type, est])
y = np.zeros(4)

# Calling neural network to make the prediction
NN = NeuralNetwork(x, y)
NN.feedforward()
