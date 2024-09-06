#Chris Schorn
#CSC 3250
#3/5/20
#Creating a learning decision tree algorithm to create 
# a decision tree, just like the one in the book

import math

class decision_tree():

    def __init__(self):
        #importance dictionary, key: [
        self.importance = {'alt': [],
                           'bar': [],
                           'friday': [],
                           'hungry': [],
                           'patrons': [],
                           'price': [],
                           'rain': [],
                           'reservation': [],
                           'type': [],
                           'willwait': []
                           }

        self.population = {'alt': [],
                           'bar': [],
                           'friday': [],
                           'hungry': [],
                           'patrons': [],
                           'price': [],
                           'rain': [],
                           'reservation': [],
                           'type': [],
                           'willwait': []
                           }

    def data_read(self):
        input_file = open('restaurant.csv','r')

        #input_file.readlines()
        #while(input_file.readline() != ""):
        for i in range(12):
            training_list = input_file.readline().split(", ")
            #print(type(training_list))
            for j in list(self.population):
                self.population[j].append(training_list.pop(0))
                #print(self.population[j])

            training_list.clear()

        #print(self.population)

        input_file.close()

    def B(self,p,n):
        q = p/(p+n)
        return -(q*math.log(q,2)+(1-q)*math.log(1-q,2))

    def importance(self):
        h_goal = 1
        gain = 0
        states = []
        
        for i in list(self.population):
            for j in range(len(self.population[i])):
                pass
                #print(self.population[i][j], j)
                #if(not(self.population[i][j] in states)):
                #    states.append(self.population[i][j])
                #    print(states)
            #states.clear()
            #for k in range(len(self.population)):
                


    def decision_tree_learning(self):
        pass
        #if the examples have run out in the populaiton tree
        # then return the plurality-value of the parent-examples

        #elif all the examples have the same classificaions
        # then return the classification

        #elif the attributes are empty
        # then return the plurality-value of the examples

        #else

decisions = decision_tree()
decisions.data_read()
decisions.importance()
