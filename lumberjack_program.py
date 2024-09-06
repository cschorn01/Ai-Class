#!/usr/bin/env python
# coding: utf-8

# # Lumber Jack Program

# Implement a simple performance-measuring environment simulator for a lumberjack world in Python (I'm assuming current release which is 3.7.5 on Ubuntu). Your submission should be similar to the vacuum-cleaner world depicted in Figure 2.2, page 38 in the text book.
# 
# However, I would like five forest tiles instead of just two floor locations. We can conceptualize the five tiles as Center,North, East, South, and West. Thus, when the agent moves, it must move twice (once to the center, second to the cardinal direction selected). We chop instead of suck.
# 
# Please implement a simple reflex agent for the lumberjack world environment. Run the environment with this agent for all possible initial forest configurations. Assume the lumberjack agent always starts in the center and the center never has forest to chop. Record the performance score for each configuration and the overall average score.
# 
# Note: I encourage you to work together. That said, everyone must submit individually and I expect any collaboration beyond simple help/pointers to be appropriately noted in comments. Speaking of which, you should expect to receive point deductions for sloppy code, bad style, lack of comments, and so forth. Include the standard program header with your name, course, program description, etc.
# 
# 
# Note: Your implementation should be modular (object oriented would be best, user-defined functions are acceptable) so that the PEAS characteristics can be changed easily. Plan ahead because we will be implementing other agent types and adding additional AI features to this foundation as the semester progresses!

# In[37]:


import random as random


# In[38]:


class environment():
    def __init__(self):
        #using tuples as keys for dictionary in (x-coordinate,y-coordinate) with (0,0) being origin
        #note on how to access elements self.environment.env[(1,0)][1]
        self.env = {(0,0): [(1,0), (-1,0), (0,1), (0,-1),0],
                   (1,0):[(0,0),1],
                   (-1,0): [(0,0),1],
                   (0,1):[(0,0),1],
                   (0,-1) :[(0,0),1]
                   }


# In[56]:


class lumberjack():
    
    def __init__(self,env, position = (0,0), actions = 0): #add position variable
        #self.position = position
        self.environment = env
        self.position = position
        self.actions = actions
        
    #function that creates the movement of the agent
    def move(self,graph): 
        rand = random.randrange(1,4,1) #generates random number for movement
        if(rand == 1): #move north
            if(self.position == (0,0) or self.position == (0,-1)):
                self.position = (self.position[0], self.position[1]+1)
            else:
                self.position = (self.position[0], self.position[1])
            
        elif(rand == 2): #move east
            
            if(self.position == (-1,0) or self.position == (0,0)):
                self.position = (self.position[0]+1, self.position[1])
            else:
                self.position = (self.position[0], self.position[1])
        
        elif(rand == 3): #move south
            #self.environment.env['S'][1]
            if(self.position == (0,0) or self.position == (0,1)):
                self.position = (self.position[0], self.position[1]-1)
            else:
               self.position = (self.position[0], self.position[1])
        
        elif(rand == 4): #move west
            #self.environment.env['W'][1]
            if(self.position == (1,0) or self.position == (0,0)):
                self.position = (self.position[0]-1, self.position[1])
            else:
               self.position = (self.position[0], self.position[1])
            
        self.actions = self.actions + 1
        lumberjack.currentPosition(self,graph)
        lumberjack.cut(self,graph)
        print('Number of Actions: ', self.actions)
        
        
    def currentPosition(self,graph): #funtion that reports the current position of the agent        
        if(self.position == (0,0)):
            print('Current Position is Origin')
        elif(self.position == (0,1)):
            print('Current Position is North')
        elif(self.position == (0,-1)):
            print('Current Position is South')
        elif(self.position == (1,0)):
            print('Current Position is East')
        elif(self.position == (0,-1)):
            print('Current Position is West')
            
            
    def cut(self,graph):
        if(self.environment.env[self.position][1] != 0):
            self.environment.env[self.position][1] = self.environment.env[self.position][1]-1
            self.actions = self.actions + 1
            #hard coded summation of the total number of trees 
            self.trees = self.environment.env[(1,0)][1] + self.environment.env[(-1,0)][1] + self.environment.env[(0,1)][1] + self.environment.env[(0,-1)][1]
            print('Number of Trees: ', self.trees)
            lumberjack.move(self,graph)
        else:
            print('Number of Trees: ', self.trees)
            lumberjack.move(self,graph)
        


# In[57]:


world = environment()
LJ = lumberjack(world)

LJ.move(world)


# In[ ]:





# In[ ]:




