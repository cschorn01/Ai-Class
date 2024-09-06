'''
Chris Schorn
CSC3250
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
        if(y == 1):
            if(x == 1):
                del self.cave[(y+1, x)][i]
                self.cave[(y+1, x)].insert(i, 1)

                del self.cave[(y, x+1)][i]
                self.cave[(y, x+1)].insert(i, 1)

            elif(x == 4):
                del self.cave[(y+1, x)][i]
                self.cave[(y+1, x)].insert(i, 1)

                del self.cave[(y, x-1)][i]
                self.cave[(y, x-1)].insert(i, 1)

            else:
                del self.cave[(y+1, x)][i]
                self.cave[(y+1, x)].insert(i, 1)

                del self.cave[(y, x-1)][i]
                self.cave[(y, x-1)].insert(i, 1)

                del self.cave[(y, x+1)][i]
                self.cave[(y, x+1)].insert(i, 1)

        elif(y == 4):
            if(x == 1):
                del self.cave[(y-1, x)][i]
                self.cave[(y-1, x)].insert(i, 1)

                del self.cave[(y, x+1)][i]
                self.cave[(y, x+1)].insert(i, 1)

            elif(x == 4):
                del self.cave[(y-1, x)][i]
                self.cave[(y-1, x)].insert(i, 1)

                del self.cave[(y, x-1)][i]
                self.cave[(y, x-1)].insert(i, 1)

            else:
                del self.cave[(y-1, x)][i]
                self.cave[(y-1, x)].insert(i, 1)

                del self.cave[(y, x-1)][i]
                self.cave[(y, x-1)].insert(i, 1)

                del self.cave[(y, x+1)][i]
                self.cave[(y, x+1)].insert(i, 1)

        elif(y == 2 or y == 3):
            if(x == 1):
                del self.cave[(y-1, x)][i]
                self.cave[(y-1, x)].insert(i, 1)

                del self.cave[(y, x+1)][i]
                self.cave[(y, x+1)].insert(i, 1)

                del self.cave[(y+1, x)][i]
                self.cave[(y+1, x)].insert(i, 1)

            elif(x == 4):
                del self.cave[(y-1, x)][i]
                self.cave[(y-1, x)].insert(i, 1)

                del self.cave[(y, x-1)][i]
                self.cave[(y, x-1)].insert(i, 1)

                del self.cave[(y+1, x)][i]
                self.cave[(y+1, x)].insert(i, 1)

            else:
                del self.cave[(y-1, x)][i]
                self.cave[(y-1, x)].insert(i, 1)

                del self.cave[(y, x-1)][i]
                self.cave[(y, x-1)].insert(i, 1)

                del self.cave[(y+1, x)][i]
                self.cave[(y+1, x)].insert(i, 1)

                del self.cave[(y, x+1)][i]
                self.cave[(y, x+1)].insert(i, 1)

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
        self.history = {}
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

        self.tell(self.location)
        if(self.history[(self.location[0],self.location[1])][1] == 1 or self.history[(self.location[0],self.location[1])][3] == 1 or self.history[(self.location[0],self.location[1])][5] == 1):
            self.creating_suspect_squares(self.worldkb[(self.location[0],self.location[1])])

            # self.get_adjacent_squares(self.location[0],self.location[1]) #adjacent_squares dictionary of current Location
            for i in self.suspect_squares: # checks every suspect square
                self.get_adjacent_squares(i[0],i[1]) #adds to the adjacent_squares dicitonary the current adjacent squares
                if (len(self.adjacent_squares)-len(self.adjacent_squares.item()-self.worldkb.item())>=2): #if our worldkb tells us that at least two adjacent squares are safe, we can make an inference
                    self.inference(i) #calling the inference function
                self.adjacent_squares.clear() #clearing the adjacent_squares dictionary



            #move back to safe space
            if(self.next_spot[0],self.next_spot[1]) in self.suspect_squares.keys():
                self.turn_right()
            else:
                self.move_forward()

    def inference(self, i):
        if self.worldkb[][3] == 1 and self.worldkb[][3] ==1:
            self.worldkb.update({(self.suspect_squares[i]:[0,0,1,0,0,0,0]})
        elif self.worldkb[][5] == 1 and self.worldkb[][5] == 1:
            self.worldkb.update({(self.suspect_squares[i]:[0,0,0,0,1,0,0]})
        elif self.worldkb[][1] == 1 and self.worldkb[][1] == 1:
            self.worldkb.update({(self.suspect_squares[i]:[1,0,0,0,0,0,0]})


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
            wumpus_pit_gold(self.location[0],self.location[1],0)
        if(cave_attributes[3] == 1):
            #detecting a breeze and attempting to infer about it
            wumpus_pit_gold(self.location[0],self.location[1],2)
        if(cave_attributes[5] == 1):
            #detecting a glitter and attempting to infer about it
            wumpus_pit_gold(self.location[0],self.location[1],4)

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
                self.adjacent_squares.update({(y, x-1):[0,0,0,0,0,0,0]})

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

    def make_choice(self, y, x, direction):
        pass


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
                if(self.suspect_squares[(y+1,x)].index(1) == ValueError):
                    self.suspect_squares.update({(y+1,x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y+1, x)][i]
                self.suspect_squares[(y+1, x)].insert(i, 1)

                if(self.suspect_squares[(y, x+1)].index(1) == ValueError):
                    self.suspect_squares.update({(y, x+1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x+1)][i]
                self.suspect_squares[(y, x+1)].insert(i, 1)

            elif(x == 4):
                if(self.suspect_squares[(y+1, x)].index(1) == ValueError):
                    self.suspect_squares.update({(y+1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y+1, x)][i]
                self.suspect_squares[(y+1, x)].insert(i, 1)

                if(self.suspect_squares[(y, x-1)].index(1) == ValueError):
                    self.suspect_squares.update({(y, x-1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x-1)][i]
                self.suspect_squares[(y, x-1)].insert(i, 1)

            else:
                if(self.suspect_squares[(y+1, x)].index(1) == ValueError):
                    self.suspect_squares.update({(y+1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y+1, x)][i]
                self.suspect_squares[(y+1, x)].insert(i, 1)

                if(self.suspect_squares[(y, x-1)].index(1) == ValueError):
                    self.suspect_squares.update({(y, x-1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x-1)][i]
                self.suspect_squares[(y, x-1)].insert(i, 1)

                if(self.suspect_squares[(y, x+1)].index(1) == ValueError):
                    self.suspect_squares.update({(y, x+1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x+1)][i]
                self.cavsuspect_squarese[(y, x+1)].insert(i, 1)

        elif(y == 4):
            if(x == 1):
                if(self.suspect_squares[(y-1, x)].index(1) == ValueError):
                    self.suspect_squares.update({(y-1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y-1, x)][i]
                self.suspect_squares[(y-1, x)].insert(i, 1)

                if(self.suspect_squares[(y, x+1)].index(1) == ValueError):
                    self.suspect_squares.update({(y, x+1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x+1)][i]
                self.suspect_squares[(y, x+1)].insert(i, 1)

            elif(x == 4):
                if(self.suspect_squares[(y, x-1)].index(1) == ValueError):
                    self.suspect_squares.update({(y, x-1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y-1, x)][i]
                self.suspect_squares[(y-1, x)].insert(i, 1)

                if(self.suspect_squares[(y-1, x)].index(1) == ValueError):
                    self.suspect_squares.update({(y-1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x-1)][i]
                self.suspect_squares[(y, x-1)].insert(i, 1)

            else:
                if(self.suspect_squares[(y-1, x)].index(1) == ValueError):
                    self.suspect_squares.update({(y-1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y-1, x)][i]
                self.suspect_squares[(y-1, x)].insert(i, 1)

                if(self.suspect_squares[(y, x+1)].index(1) == ValueError):
                    self.suspect_squares.update({(y+1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x-1)][i]
                self.suspect_squares[(y, x-1)].insert(i, 1)

                if(self.suspect_squares[(y+1, x-1)].index(1) == ValueError):
                    self.suspect_squares.update({(y+1, x-1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x+1)][i]
                self.suspect_squares[(y, x+1)].insert(i, 1)

        elif(y == 2 or y == 3):
            if(x == 1):
                if(self.suspect_squares[(y-1, x)].index(1) == ValueError):
                    self.suspect_squares.update({(y-1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y-1, x)][i]
                self.suspect_squares[(y-1, x)].insert(i, 1)

                if(self.suspect_squares[(y, x+1)].index(1) == ValueError):
                    self.suspect_squares.update({(y, x+1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x+1)][i]
                self.suspect_squares[(y, x+1)].insert(i, 1)

                if(self.suspect_squares[(y+1, x)].index(1) == ValueError):
                    self.suspect_squares.update({(y+1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y+1, x)][i]
                self.suspect_squares[(y+1, x)].insert(i, 1)

            elif(x == 4):
                if(self.suspect_squares[(y-1, x)].index(1) == ValueError):
                    self.suspect_squares.update({(y-1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y-1, x)][i]
                self.suspect_squares[(y-1, x)].insert(i, 1)

                if(self.suspect_squares[(y, x-1)].index(1) == ValueError):
                    self.suspect_squares.update({(y, x-1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x-1)][i]
                self.suspect_squares[(y, x-1)].insert(i, 1)

                if(self.suspect_squares[(y+1, x)].index(1) == ValueError):
                    self.suspect_squares.update({(y+1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y+1, x)][i]
                self.suspect_squares[(y+1, x)].insert(i, 1)

            else:
                if(self.suspect_squares[(y-1, x)].index(1) == ValueError):
                    self.suspect_squares.update({(y-1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y-1, x)][i]
                self.suspect_squares[(y-1, x)].insert(i, 1)

                if(self.suspect_squares[(y, x-1)].index(1) == ValueError):
                    self.suspect_squares.update({(y, x-1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x-1)][i]
                self.suspect_squares[(y, x-1)].insert(i, 1)

                if(self.suspect_squares[(y+1, x)].index(1) == ValueError):
                    self.suspect_squares.update({(y+1, x):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y+1, x)][i]
                self.suspect_squares[(y+1, x)].insert(i, 1)

                if(self.suspect_squares[(y, x+1)].index(1) == ValueError):
                    self.suspect_squares.update({(y, x+1):[0,0,0,0,0,0,0]})
                del self.suspect_squares[(y, x+1)][i]
                self.suspect_squares[(y, x+1)].insert(i, 1)

    def tell(self):
        if((self.location[0],self.location[1]) not in  self.worldkb.keys()):
            self.worldkb.update({(location[0],location[1]):self.cave[(location[0],location[1])]})
            print("self.cave[(location[0],location[1])]: ", self.cave[(location[0],location[1])])
        self.history.update({(location[0],location[1]):self.cave[(location[0],location[1])]})

        # update({(location[0],location[1]): []})
        #
        # if((location[0],location[1]) not in  self.worldkb.keys()):
        #     self.worldkb.update({(location[0],location[1]): self.cave[(location[0],location[1])]})
        # self.history.update({(location[0],location[1]): self.cave[(location[0],location[1])]})


    def turn_right(self):
        ifself.direction == 4):
            self.direction = 1
        else:
            self.direction = self.direction + 1

    def turn_left(self):
        if(self.direction == 1):
            self.direction = 4
        else:
            self.direction = self.direction - 1

    def move_forward(self, next_spot):
        self.location[0] = self.next_spot[0]
        self.location[1] = self.next_spot[1]

    def calculating_next_spot(self):
        if(self.direction == 1 and self.location[0] != 1):
            self.next_spot = [self.location[0]+1,self.location[1]]
        elif(self.direction == 2 and self.location[0] != 4):
            self.next_spot = [self.location[0],self.location[1]+1]
        elif(self.direction == 3 and self.location[0] != 1):
            self.next_spot = [self.location[0]-1,self.location[1]]
        elif(self.direction == 4 and self.location[0] != 4):
            self.next_spot = [self.location[0],self.location[1]-1]




cave = world()
cave.random_generate()
legolas = agent(cave.cave)
#legolas.move_forward()
legolas.actions()
