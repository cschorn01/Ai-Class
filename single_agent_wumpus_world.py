'''
Chris Schorn, Kyle Wiseman, Ty Carlson, Noah WorleyCSC3250
4/16/20
Wumpus World Knowledge Based Program

Purpose

The Wumpus world is a cave with 16 rooms (4×4). You can code these with x,y
coordinates for ease of reference (e.g. 1,1, 1,2, and so forth).
Each room is connected to others through walkways except for the outer edges.

Our agent always starts from in the same room. The cave has between 3 pits
randomly placed, a randomly placed treasure and a beast named Wumpus (also randomly placed).
The Wumpus can not move but eats the one who enters its room.
If the agent enters the pit, it gets stuck there.

The goal of the agent is to take the treasure and come out of the cave.
The agent doesn’t need to learn or remember in the sense we have engineering previous AI.
Instead, have the agent explore and update its knowledgebase.

PEAS

The list of discrete features you need to implement so that the agent can explore the cave,
find the treasure while avoiding pits and the wumpus, and exit are as follows:

Performance measures:
- Agent gets the gold and return back safe = +1000 points - Agent dies = -1000 points
- Each move of the agent = -1 point
- Agent uses the arrow = -10 points

Environment:
- A cave with 16(4×4) rooms
- Rooms adjacent (not diagonally) to the Wumpus are stinking
- Rooms adjacent (not diagonally) to the pit are breezy
- The room with the gold glitters
- Agent’s initial position – Room[1, 1] and facing right side
- Location of Wumpus, gold and 3 pits can be anywhere, except in Room[1, 1].

Actuators:
- Move forward - Turn right
- Turn left
- Shoot
- Grab
- Release

Sensors:
- Breeze
- Stench
- Glitter
- Scream (When the Wumpus is killed) - Bump (when the agent hits a wall)
'''

import random
import sys
import time

'''
(1,1)(1,2)(1,3)(1,4)
(2,1)(2,2)(2,3)(2,4)
(3,1)(3,2)(3,3)(3,4)
(4,1)(4,2)(4,3)(4,4)
'''

'''
Format:
(y,x): [wumpus, smell, pit, breeze, gold, glitter, bump]
1 if true
0 if false
tuple is the
'''
class world():
    def __init__(self):
        self.cave = {
                    (1, 1): [],
                    (1, 2): [],
                    (1, 3): [],
                    (1, 4): [],
                    (2, 1): [],
                    (2, 2): [],
                    (2, 3): [],
                    (2, 4): [],
                    (3, 1): [],
                    (3, 2): [],
                    (3, 3): [],
                    (3, 4): [],
                    (4, 1): [],
                    (4, 2): [],
                    (4, 3): [],
                    (4, 4): [],
                    }

    def random_generate(self):
        #initializing the random variables
        wumpusx = random.randint(1, 4)
        wumpusy = random.randint(1, 4)
        goldx = random.randint(1, 4)
        goldy = random.randint(1, 4)
        pit1x = random.randint(1, 4)
        pit1y = random.randint(1, 4)
        pit2x = random.randint(1, 4)
        pit2y = random.randint(1, 4)
        pit3x = random.randint(1, 4)
        pit3y = random.randint(1, 4)

        while (wumpusx == 1 and wumpusy == 1):
            wumpusx = random.randint(1, 4)
            wumpusy = random.randint(1, 4)
        print("Wumpus: ",wumpusy,wumpusx)
        while ((goldx == 1 and goldy == 1) or (wumpusx == goldx and wumpusy == goldy)):
            goldx = random.randint(1, 4)
            goldy = random.randint(1, 4)
        print("Gold: ",goldy,goldx)
        while ((pit1x == 1 and pit1y == 1) or (goldx == pit1x and goldy == pit1y) or (wumpusx == pit1x and wumpusy == pit1y)):
            pit1x = random.randint(1, 4)
            pit1y = random.randint(1, 4)
        print("Pit1: ",pit1y,pit1x)
        while ((pit2x == 1 and pit2y == 1) or (pit2y == pit1y and pit2x == pit1x) or (goldx == pit2x and goldy == pit2y) or (wumpusx == pit2x and wumpusy == pit2y)):
            pit2x = random.randint(1, 4)
            pit2y = random.randint(1, 4)
        print("Pit2: ",pit2y,pit2x)
        while ((pit3x == 1 and pit3y == 1) or (pit3y == pit1y and pit3x == pit1x) or (pit3y == pit2y and pit3x == pit2x) or (goldx == pit3x and goldy == pit3y) or (wumpusx == pit3x and wumpusy == pit3y)):
            pit3x = random.randint(1, 4)
            pit3y = random.randint(1, 4)
        print("Pit3: ",pit3y,pit3x)


        '''
        creating a nested list of 7 zeroes within the index i
        i is a tuple of (y,x) coordinates & is the key in the dictionary
        works
        '''
        for i in self.cave:
            for j in range(7):
                self.cave[i].append(0)


        #inserting bump value in each edge square of cave
        #works
        for i in [(1, 1),(1, 2),(1, 3),(1, 4),(2, 1),(2, 4),(3, 1),(3, 4),(4, 1),(4, 2),(4, 3),(4, 4)]:
            del self.cave[i][6]
            self.cave[i].append(1)
            #print(i)

        # print checking the state of world at this point
        # for i in self.cave:
        #     print(self.cave[i])

        for i in self.cave: #i is the tuple keys in the dictionary
            #print(i)
            # for j in range(7):
            #     self.cave[i].append(0)

            #inserting wumpus and smell to cave in adjacent squares to wumpus
            if(i == (wumpusy, wumpusx)):
                del self.cave[i][0]
                self.cave[i].insert(0, 1)

                self.smell_breeze_glitter(wumpusy, wumpusx, 1)


            elif(i == (goldy,goldx)):

                del self.cave[i][4]
                self.cave[i].insert(4, 1)

                self.smell_breeze_glitter(goldy, goldx, 5)


            elif(i == (pit1y,pit1x)):
                del self.cave[i][2]
                self.cave[i].insert(2, 1)

                self.smell_breeze_glitter(pit1y, pit1x, 3)


            elif(i == (pit2y,pit2x)):
                del self.cave[i][2]
                self.cave[i].insert(2, 1)

                self.smell_breeze_glitter(pit2y, pit2x, 3)


            elif(i == (pit3y,pit3x)):
                del self.cave[i][2]
                self.cave[i].insert(2, 1)

                self.smell_breeze_glitter(pit3y, pit3x, 3)


        for i in self.cave:
            print(i,":",self.cave[i])

    #function to implement smell, breeze and glitter
    def smell_breeze_glitter(self, y, x, i):
        '''
        y is y coordinate of wumpus, gold, or pits

        x is x coordinate of wumpus, gold, or pits

        i is determined by whether it's smell, breeze, or glitter
        this comes from the random_generate function and is
        the spot in which a 1 is inserted into the list at that (y,x) spot
        '''

        num_attributes = 1


        if(y == 1):
            if(x == 1):
                self.cave[(y+1, x)][i]+=1
                self.cave[(y, x+1)][i]+=1
            elif(x == 4):
                self.cave[(y+1, x)][i]+=1
                self.cave[(y, x-1)][i]+=1
            else:
                self.cave[(y+1, x)][i]+=1
                self.cave[(y, x-1)][i]+=1
                self.cave[(y, x+1)][i]+=1

        elif(y == 4):
            if(x == 1):
                self.cave[(y-1, x)][i]+=1
                self.cave[(y, x+1)][i]+=1
            elif(x == 4):
                self.cave[(y-1, x)][i]+=1
                self.cave[(y, x-1)][i]+=1
            else:
                self.cave[(y-1, x)][i]+=1
                self.cave[(y, x-1)][i]+=1
                self.cave[(y, x+1)][i]+=1

        elif(y == 2 or y == 3):
            if(x == 1):
                self.cave[(y-1, x)][i]+=1
                self.cave[(y, x+1)][i]+=1
                self.cave[(y+1, x)][i]+=1
            elif(x == 4):
                self.cave[(y-1, x)][i]+=1
                self.cave[(y, x-1)][i]+=1
                self.cave[(y+1, x)][i]+=1
            else:
                self.cave[(y-1, x)][i]+=1
                self.cave[(y, x-1)][i]+=1
                self.cave[(y+1, x)][i]+=1
                self.cave[(y, x+1)][i]+=1

class agent:
    def __init__(self, cave):
        '''
        Direction of the agent corresponding to cardinal directions
        North = 1
        East = 2
        South = 3
        West = 4
        '''
        self.direction = 2
        self.location = [1,1] #[y,x]
        self.next_spot = []
        self.done = False
        self.arrows = 1

        '''
        Format:
        (1,1): [wumpus, smell, pit, breeze, gold, glitter, bump]
        1 if true
        0 if false

        Idea: As agent lands on new tiles add them and their embedded info
        from the world dictionary to worldkb which kb can call upon
        to retrieve info. This is observation step
        '''
        self.worldkb = {}
        self.history = []
        self.adjacent_squares = {}
        self.suspect_squares = {}
        self.cave = cave

    def knowledge_base(self):
        '''
        when smell, breeze, or glitter are detected, add the squares arount
        the agent to this list as suspect squares to be compared against worldkb
        and confirmed or denied
        '''
        #inferred tuples about locations of pits, wumpus and gold
        pit1,pit2,pit3 = (0,0),(0,0),(0,0)
        gold = (0,0)
        wumpus = (0,0)
        infer1 = (0,0)
        infer2 = (0,0)

        self.tell()

        if(len(self.history) < 2):
            self.next_spot = [1,2]
            self.move_forward()
        elif(self.worldkb[(self.location[0],self.location[1])][1] > 0 or self.worldkb[(self.location[0],self.location[1])][3] > 0 or self.worldkb[(self.location[0],self.location[1])][5] > 0):
            self.creating_suspect_squares(self.worldkb[(self.location[0],self.location[1])])

            #removing suspects we have already been to
            suspect_list = self.suspect_squares.copy()
            for i in suspect_list:
                if(i in self.worldkb.keys()):
                    del self.suspect_squares[i]

            # self.get_adjacent_squares(self.location[0],self.location[1]) #adjacent_squares dictionary of current Location
            suspect_list = self.suspect_squares.copy()
            for i in suspect_list: # checks every suspect square
                print("i: ", i)
                self.get_adjacent_squares(i[0],i[1]) #adds to the adjacent_squares dicitonary the current adjacent squares, correct syntax in parentheses
                if (len(self.adjacent_squares)-len(self.adjacent_squares.keys()-self.worldkb.keys())>=2): #if our worldkb tells us that at least two adjacent squares are known, we can make an inference
                    self.inference(i) #calling the inference function
                    self.adjacent_squares.clear() #clearing the adjacent_squares dictionary
                    self.suspect_squares.clear()

            self.calculating_next_spot()
            dangerous=False
            if(self.worldkb[(self.location[0],self.location[1])][1] > 0 or self.worldkb[(self.location[0],self.location[1])][3] > 0):
                dangerous=True
            # Make sure we are moving to new square and not bouncing
            if ((self.next_spot[0],self.next_spot[1]) in self.worldkb.keys()):
                if(self.worldkb[(self.next_spot[0],self.next_spot[1])][0] > 0 or self.worldkb[(self.next_spot[0],self.next_spot[1])][2] > 0):
                    self.turn_right()
                else:
                    # self.calculating_next_spot()
                    self.move_forward()
            elif ((self.next_spot[0],self.next_spot[1]) in self.suspect_squares.keys()):
                self.turn_right()
            elif (self.next_spot[0]==0 or self.next_spot[0]==5 or self.next_spot[1]==0 or self.next_spot[1]==5):
                #bumps
                self.turn_right()
            elif(not dangerous):
                if((self.next_spot[0],self.next_spot[1]) == self.history[len(self.history)-2]): #checking to see if next spot not previous spot
                    self.turn_right()
                else:
                    # self.calculating_next_spot()
                    self.move_forward()
            else:
                # self.calculating_next_spot()
                self.move_forward()
        else:
            self.calculating_next_spot()
            self.move_forward()

        self.tell()

#updating worldkb from suspect_squares prematurely

        if((self.location[0],self.location[1]) in self.worldkb.keys()):
            if(self.worldkb[(self.location[0],self.location[1])][0] == 1):
                if(self.arrows == 0):
                    self.done = True
                    print("Agent was eaten by the Wumpus!")
                else:
                    rand = random.random()
                    if(rand > 0.1):
                        self.worldkb[(self.location[0],self.location[1])][0] = 0
                        print("Agent shot the Wumpus!")
                    else:
                        self.done = True
                        print("Agent was eaten by the Wumpus!")
                    self.arrows-=1
            elif(self.worldkb[(self.location[0],self.location[1])][2] == 1):
                self.done = True
                print("Agent fell in a pit!")
            elif(self.worldkb[(self.location[0],self.location[1])][4] == 1):
                self.done = True
                print("Agent found the gold!")
                print("Agent used an escape rope! ◓")

    '''
    function performing inference
    i parameter is the tuple key of a dictionary of suspect_squares
    '''
    def inference(self, i):
        empty=True
        print("Inference")

        self.worldkb.update({i:[0,0,0,0,0,0,0]})

        #Error on the lines with update(): Unhashable type list
        if(self.worldkb[(self.location[0],self.location[1])][5] > 0 and self.suspect_squares[i][4] > 0):
            print("Testing inference:", self.worldkb[(self.location[0],self.location[1])])
            print(self.suspect_squares[i])
            self.worldkb[i][4] += 1
            empty=False

        if(self.worldkb[(self.location[0],self.location[1])][1] > 0 and self.suspect_squares[i][0] > 0):
            self.worldkb[i][0] += 1
            print("Testing inference:", self.worldkb[(self.location[0],self.location[1])])
            print(self.suspect_squares[i])
            empty=False

        # if (self.adjacent_squares[(i[0]+1,i[1])][3] == 1 and self.adjacent_squares[(i[0],)][3] ==1) or (self.adjacent_squares[][3] == 1 and self.adjacent_squares[][3] ==1 and self.adjacent_squares[][3] ==1):
        if(self.worldkb[(self.location[0],self.location[1])][3] > 0 and self.suspect_squares[i][2] > 0): # detecting if there is a breeze in the current location to do inferrence on pits
            self.worldkb[i][2] += 1
            print("Testing inference:", self.worldkb[(self.location[0],self.location[1])])
            print(self.suspect_squares[i])
            if(self.worldkb[(self.location[0],self.location[1])][3] == 1):
                pass
                #grab the key before last of the suspect_squares dictionary and set its value to zero, and then clear suspect_squares
                # self.worldkb.update({self.suspect_squares[self.suspect_squares.keys()[len(self.suspect_squares)-2]]:[0,0,0,0,0,0,0]})
                # self.worldkb.update({self.suspect_squares[self.suspect_squares.keys().index(i)-1]:[0,0,0,0,0,0,0]})
                # self.suspect_squares.clear()
            empty=False

        if(empty):
            self.worldkb.update({i:[0,0,0,0,0,0,0]})

    # def inference(self, inf1, inf2):
    #     if (self.direction == 1 or self.direction == 3):
    #         sus = (inf1[0], inf2[1]+1)
    #     else:
    #         sus = (inf2[0]+1, inf1[1])
    #    if (self.worldkb[inf1][1] == 1 and self.worldkb[inf2][1] == 1):
    #        self.worldkb.update({(sus[0],sus[1]):[1,0,0,0,0,0,0]})
    #    elif (self.worldkb[inf1][3] == 1 and self.worldkb[inf2][3] == 1):
    #        self.worldkb.update({(sus[0],sus[1]):[0,0,1,0,0,0,0]})
    #    elif (self.worldkb[inf1][5] == 1 and self.worldkb[inf2][5] == 1):
    #        self.worldkb.update({sus[0],sus[1]}):[0,0,0,0,1,0,0]})
    #        self.move_forward(sus)
    #    else:
    #        self.worldkb.update({sus[0],sus[1]}):[0,0,0,0,0,0,0]})
    #        del self.suspect_squares[sus]
    #        self.move_forward(sus)

        '''
        Notes to selves:
            last time we setup the logic for inferrence but need to double check the syntax for all of inferrence
            create test of if statement on line 334
            create deeper inferrence
            Add logic for movement to establish inferrence
        '''


        if(i in self.worldkb.keys()): #comparing to the keys in worldkb
            if(self.worldkb[i][0] == 0 and self.worldkb[i][2] == 0 and self.worldkb[i][4] == 0): #
                del self.suspect_squares[i] #removes the squares that are confirmed to be safe
        #make guess about safe space
        # if()





    def creating_suspect_squares(self, cave_attributes):
        #cave cave_attributes is the 7 attributes of any given square
        if(cave_attributes == [0,0,0,0,0,0,0]):
            if(self.location[0] != 4 and self.location[1] != 4):
                self.worldkb.update({(self.location[0]+1,self.location[1]):[0,0,0,0,0,0,0]})
                self.worldkb.update({(self.location[0],self.location[1]+1):[0,0,0,0,0,0,0]})
            elif(self.location[0] == 4 and self.location[1] != 4):
                self.worldkb.update({(self.location[0],self.location[1]+1):[0,0,0,0,0,0,0]})
            elif(self.location[0] != 4 and self.location[1] == 4):
                self.worldkb.update({(self.location[0]+1,self.location[1]):[0,0,0,0,0,0,0]})
        if(cave_attributes[1] == 1):
            #detecting a smell and attempting to infer about it
            self.wumpus_pit_gold(self.location[0],self.location[1],0)
        if(cave_attributes[3] == 1):
            #detecting a breeze and attempting to infer about it
            self.wumpus_pit_gold(self.location[0],self.location[1],2)
        if(cave_attributes[5] == 1):
            #detecting a glitter and attempting to infer about it
            self.wumpus_pit_gold(self.location[0],self.location[1],4)

    #function to get the adjacent square
    def get_adjacent_squares(self, y, x):

        if(y == 1):
            if(x == 1):
                self.adjacent_squares.update({(y, x+1):[0,0,0,0,0,0,0]})
                self.adjacent_squares.update({(y+1, x):[0,0,0,0,0,0,0]})

            elif(x == 4):
                self.adjacent_squares.update({(y+1, x):[0,0,0,0,0,0,0]})
                self.adjacent_squares.update({(y, x-1):[0,0,0,0,0,0,0]})

            else:
                self.adjacent_squares.update({(y+1, x):[0,0,0,0,0,0,0]})
                self.adjacent_squares.update({(y, x-1):[0,0,0,0,0,0,0]})
                self.adjacent_squares.update({(y, x+1):[0,0,0,0,0,0,0]})

        elif(y == 4):
            if(x == 1):
                self.adjacent_squares.update({(y-1, x):[0,0,0,0,0,0,0]})
                self.adjacent_squares.update({(y, x+1):[0,0,0,0,0,0,0]})

            elif(x == 4):
                self.adjacent_squares.update({(y, x-1):[0,0,0,0,0,0,0]})
                self.adjacent_squares.update({(y-1, x):[0,0,0,0,0,0,0]})

            else:
                self.adjacent_squares.update({(y-1, x):[0,0,0,0,0,0,0]})
                self.adjacent_squares.update({(y, x+1):[0,0,0,0,0,0,0]})
                self.adjacent_squares.update({(y, x-1):[0,0,0,0,0,0,0]})

        elif(y == 2 or y == 3):
            if(x == 1):
                self.adjacent_squares.update({(y-1, x):[0,0,0,0,0,0,0]})
                self.adjacent_squares.update({(y, x+1):[0,0,0,0,0,0,0]})
                self.adjacent_squares.update({(y+1, x):[0,0,0,0,0,0,0]})

            elif(x == 4):
                self.adjacent_squares.update({(y-1, x):[0,0,0,0,0,0,0]})
                self.adjacent_squares.update({(y, x-1):[0,0,0,0,0,0,0]})
                self.adjacent_squares.update({(y+1, x):[0,0,0,0,0,0,0]})

            else:
                self.adjacent_squares.update({(y-1, x):[0,0,0,0,0,0,0]})
                self.adjacent_squares.update({(y, x-1):[0,0,0,0,0,0,0]})
                self.adjacent_squares.update({(y+1, x):[0,0,0,0,0,0,0]})
                self.adjacent_squares.update({(y, x+1):[0,0,0,0,0,0,0]})

    # def make_choice(self, y, x, direction):
    #     pass


    # def get_orientation(self):
    #     if(self.direction == 1):
    #         north = self.location[0]
    #     elif(self.direction == 2):
    #     elif(self.direction == 3):
    #     elif(self.direction == 4):




    #function to implement wumpus_pit_gold
    def wumpus_pit_gold(self, y, x, i):
        '''
        y is y coordinate of smell, breeze, or glitter

        x is x coordinate of smell, breeze, or glitter

        i is determined by whether it's wumpus, pit, or gold
        this comes from the random_generate function and is
        the spot in which a 1 is inserted into the list at that (y,x) spot
        '''
        if(y == 1):
            if(x == 1):
                if((y+1,x) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y+1,x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y+1, x)][i]

                self.suspect_squares[(y+1, x)].insert(i, 1)

                if((y, x+1) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y, x+1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x+1)][i]
                self.suspect_squares[(y, x+1)].insert(i, 1)

            elif(x == 4):
                if((y+1,x) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y+1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y+1, x)][i]
                self.suspect_squares[(y+1, x)].insert(i, 1)

                if((y, x-1) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y, x-1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x-1)][i]
                self.suspect_squares[(y, x-1)].insert(i, 1)

            else:
                if((y+1,x) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y+1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y+1, x)][i]
                self.suspect_squares[(y+1, x)].insert(i, 1)

                if((y, x-1) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y, x-1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x-1)][i]
                self.suspect_squares[(y, x-1)].insert(i, 1)

                if((y, x+1) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y, x+1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x+1)][i]
                self.suspect_squares[(y, x+1)].insert(i, 1)

        elif(y == 4):
            if(x == 1):
                if((y-1, x) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y-1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y-1, x)][i]
                self.suspect_squares[(y-1, x)].insert(i, 1)

                if((y, x+1) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y, x+1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x+1)][i]
                self.suspect_squares[(y, x+1)].insert(i, 1)

            elif(x == 4):
                if((y, x-1) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y, x-1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x-1)][i]
                self.suspect_squares[(y, x-1)].insert(i, 1)

                if((y-1, x) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y-1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y-1, x)][i]
                self.suspect_squares[(y-1, x)].insert(i, 1)

            else:
                if((y-1, x) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y-1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y-1, x)][i]
                self.suspect_squares[(y-1, x)].insert(i, 1)

                if((y, x+1) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y, x+1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x+1)][i]
                self.suspect_squares[(y, x+1)].insert(i, 1)

                if((y, x-1) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y, x-1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x-1)][i]
                self.suspect_squares[(y, x+-1)].insert(i, 1)

        elif(y == 2 or y == 3):
            if(x == 1):
                if((y-1, x) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y-1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y-1, x)][i]
                self.suspect_squares[(y-1, x)].insert(i, 1)

                if((y, x+1) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y, x+1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x+1)][i]
                self.suspect_squares[(y, x+1)].insert(i, 1)

                if((y+1, x) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y+1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y+1, x)][i]
                self.suspect_squares[(y+1, x)].insert(i, 1)

            elif(x == 4):
                if((y-1, x) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y-1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y-1, x)][i]
                self.suspect_squares[(y-1, x)].insert(i, 1)

                if((y, x-1) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y, x-1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x-1)][i]
                self.suspect_squares[(y, x-1)].insert(i, 1)

                if((y+1, x) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y+1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y+1, x)][i]
                self.suspect_squares[(y+1, x)].insert(i, 1)

            else:
                if((y-1, x) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y-1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y-1, x)][i]
                self.suspect_squares[(y-1, x)].insert(i, 1)

                if((y, x-1) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y, x-1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x-1)][i]
                self.suspect_squares[(y, x-1)].insert(i, 1)

                if((y+1, x) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y+1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y+1, x)][i]
                self.suspect_squares[(y+1, x)].insert(i, 1)

                if((y, x+1) not in self.suspect_squares.keys()):
                    self.suspect_squares.update({(y, x+1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x+1)][i]
                self.suspect_squares[(y, x+1)].insert(i, 1)

    def tell(self):
        if((self.location[0],self.location[1]) not in  self.worldkb.keys()):
            self.worldkb.update({(self.location[0],self.location[1]):self.cave[(self.location[0],self.location[1])]})
            print("self.cave[" + str(self.location[0]) +", " + str(self.location[1]) + "]:", self.cave[(self.location[0],self.location[1])])
        self.history.append((self.location[0],self.location[1]))

        # update({(location[0],location[1]): []})
        #
        # if((location[0],location[1]) not in  self.worldkb.keys()):
        #     self.worldkb.update({(location[0],location[1]): self.cave[(location[0],location[1])]})
        # self.history.update({(location[0],location[1]): self.cave[(location[0],location[1])]})


    def turn_right(self):
        if(self.direction == 4):
            self.direction = 1
        else:
            self.direction = self.direction + 1

    def turn_left(self):
        if(self.direction == 1):
            self.direction = 4
        else:
            self.direction = self.direction - 1

    def move_forward(self):
        self.location[0] = self.next_spot[0]
        self.location[1] = self.next_spot[1]


        #moving out of bounds; use greater than and less than operators
    def calculating_next_spot(self):
        if(self.direction == 1 and self.location[0] != 1):
            self.next_spot = [self.location[0]+1,self.location[1]]
        elif(self.direction == 2 and self.location[1] != 4):
            self.next_spot = [self.location[0],self.location[1]+1]
        elif(self.direction == 2 and self.location[1] == 4):
            self.turn_right()
            self.next_spot = [self.location[0]+1, self.location[1]]
        elif(self.direction == 3 and self.location[0] != 4):
            self.next_spot = [self.location[0]+1,self.location[1]]
        elif(self.direction == 3 and self.location[0] == 4):
            self.turn_right()
            self.next_spot = [self.location[0],self.location[1]-1]
        elif(self.direction == 4 and self.location[1] != 1):
            self.next_spot = [self.location[0],self.location[1]-1]
        elif(self.direction == 4 and self.location[1] == 1):
            self.turn_right()
            self.turn_right()
            self.turn_right()
            self.next_spot = [self.location[0]+1, self.location[1]]






cave = world()
cave.random_generate()
legolas = agent(cave.cave)
#legolas.move_forward()
while(legolas.done != True):
    legolas.knowledge_base()
    time.sleep(2)
    print(legolas.location)
    # print(legolas.worldkb)
    print("Direction: ", legolas.direction)
