'''
Chris Schorn & Kyle Wiseman
CSC 3250
4/7/20
reinforcement learning program

https://medium.com/swlh/introduction-to-reinforcement-learning-coding-q-learning-part-3-9778366a41c0
https://www.geeksforgeeks.org/q-learning-in-python/

'''

import sys
import time
import os
import gym
import random
from contextlib import closing

import numpy as np
from six import StringIO, b

from gym import utils
from gym.envs.toy_text import discrete

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

MAPS = {
    "4x4": [
        "SFFF",
        "FBFB",
        "FFFB",
        "BFFG"
    ],
    "8x8": [
        "SFFFFFFF",
        "FFFFFFFF",
        "FFFBFFFF",
        "FFFFFBFF",
        "FFFBFFFF",
        "FBBFFFBF",
        "FBFFBFBF",
        "FFFBFFFG"
    ],
}


def generate_random_map(size=8, p=0.8):
    """Generates a random valid map (one that has a path from start to goal)
    :param size: size of each side of the grid
    """
    valid = False

    # DFS to check that it's a valid path.
    def is_valid(res):
        frontier, discovered = [], set()
        frontier.append((0,0))
        while frontier:
            r, c = frontier.pop()
            if not (r,c) in discovered:
                discovered.add((r,c))
                directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
                for x, y in directions:
                    r_new = r + x
                    c_new = c + y
                    if r_new < 0 or r_new >= size or c_new < 0 or c_new >= size:
                         continue
                    if res[r_new][c_new] == 'G':
                        return True
                    if (res[r_new][c_new] not in '#B'):
                        frontier.append((r_new, c_new))
        return False

    while not valid:
        p = min(1, p)
        res = np.random.choice(['F', 'B'], (size, size), p=[p, 1-p])
        res[0][0] = 'S'
        res[-1][-1] = 'G'
        valid = is_valid(res)
    return ["".join(x) for x in res]


class FrozenLakeEnv(discrete.DiscreteEnv):
    """
    The lumberjack is here. His goal is to find his axe to accomplish
    his goal of chopping down the forest. He must find his axe, because
    it was a family heirloom handed down for generations. But along his
    perilous journey, he must also look out for the bears that have been
    feuding with his family for centuries.
    The surface is described using a grid like the following
        SFFF
        FHFH
        FFFH
        HFFG
    S : starting point, safe
    F : forest, safe
    H : hole, fall to your doom
    B:  bear, be eaten by bear
    G : goal, where the axe is located
    The episode ends when you reach the goal or fall in a hole.
    You receive a reward of 1 if you reach the goal, and zero otherwise.
    """

    metadata = {'render.modes': ['human', 'ansi']}

    def __init__(self, desc=None, map_name="4x4",is_slippery=True):
        if desc is None and map_name is None:
            desc = generate_random_map()
        elif desc is None:
            desc = MAPS[map_name]
        self.desc = desc = np.asarray(desc,dtype='c')
        self.nrow, self.ncol = nrow, ncol = desc.shape
        self.reward_range = (0, 1)

        nA = 4
        nS = nrow * ncol

        isd = np.array(desc == b'S').astype('float64').ravel()
        isd /= isd.sum()

        P = {s : {a : [] for a in range(nA)} for s in range(nS)}

        def to_s(row, col):
            return row*ncol + col

        def inc(row, col, a):
            if a == LEFT:
                col = max(col-1,0)
            elif a == DOWN:
                row = min(row+1,nrow-1)
            elif a == RIGHT:
                col = min(col+1,ncol-1)
            elif a == UP:
                row = max(row-1,0)
            return (row, col)

        for row in range(nrow):
            for col in range(ncol):
                s = to_s(row, col)
                for a in range(4):
                    li = P[s][a]
                    letter = desc[row, col]
                    if letter in b'GB':
                        li.append((1.0, s, 0, True))
                    else:
                        '''
                        if is_slippery:
                            for b in [(a-1)%4, a, (a+1)%4]:
                                newrow, newcol = inc(row, col, b)
                                newstate = to_s(newrow, newcol)
                                newletter = desc[newrow, newcol]
                                done = bytes(newletter) in b'GB'
                                rew = float(newletter == b'G')
                                li.append((1.0/3.0, newstate, rew, done))
                        else:
                        '''
                        newrow, newcol = inc(row, col, a)
                        newstate = to_s(newrow, newcol)
                        newletter = desc[newrow, newcol]
                        done = bytes(newletter) in b'GB'
                        rew = float(newletter == b'G')
                        li.append((1.0, newstate, rew, done))

        super(FrozenLakeEnv, self).__init__(nS, nA, P, isd)

    def render(self, mode='human'):
        outfile = StringIO() if mode == 'ansi' else sys.stdout

        row, col = self.s // self.ncol, self.s % self.ncol
        desc = self.desc.tolist()
        desc = [[c.decode('utf-8') for c in line] for line in desc]
        desc[row][col] = utils.colorize(desc[row][col], "red", highlight=True)
        if self.lastaction is not None:
            outfile.write("  ({})\n".format(["Left","Down","Right","Up"][self.lastaction]))
        else:
            outfile.write("\n")
        outfile.write("\n".join(''.join(line) for line in desc)+"\n")

        if mode != 'human':
            with closing(outfile):
                return outfile.getvalue()

total = 0
size = 8 # Size of the map
prob = .96 # Probability of a tile being forest
env = FrozenLakeEnv(generate_random_map(size, prob))

epsilon = 0.9 # For using a greedy epsilon algorithm
total_episodes = 10000 # Number of times the agent will explore all ticks
action_limit = 100 # Max number of steps the agent can take

learning_rate = 0.90 #ammount the agent relies on previous knowledge
discount = 0.96 #ammount the agent values future rewards

Q = np.zeros((env.observation_space.n, env.action_space.n))

def choose_action(state):
    action=1
    if np.random.uniform(0, 1) < epsilon:
        if(env.nrow == 0):
            action = random.randint(1,3)
        elif(env.ncol == 0):
            action = random.randint(0,2)
        elif(env.nrow == 7):
            rand = rand.randint(1,2)
            if(rand == 1):
                action = random.randint(0,1)
            else:
                action = 3
        elif(env.ncol == 7):
            rand = rand.randint(1,2)
            if(rand == 1):
                action = random.randint(2,3)
            else:
                action = 0
        else:
            action = env.action_space.sample()
    else:
        action = np.argmax(Q[state, :])

    return action

def learn(state, observation, reward, action):
    predict = Q[state, action]
    target = reward + discount * np.max(Q[observation, :])
    Q[state, action] = Q[state, action] + learning_rate * (target - predict)

succesful_episodes = []

# Runs through each episode of the environment
for i in range(total_episodes):
    state = env.reset()
    # Number of turns the agent has taken
    t = 0

    if (learning_rate > 0):
        learning_rate -= 0.0001 #reseting learning rate for each episode
    else:
        learning_rate = 0

    while t < action_limit:
        #env.render()

        action = choose_action(state)

        '''
        step function built into openAI gym, returns a tuple with the below
        values in int, float, boolean, dictionary
        '''
        observation, reward, done, info = env.step(action)
        #print(env.step(action))

        learn(state, observation, reward, action)
        total += reward
        state = observation
        if(reward == 1):
            succesful_episodes.append(i)

        t += 1
        #learning_rate -= .005
        if done:
            break

        #time.sleep(0.1)
    if(epsilon > 0):
        epsilon -= .0001
    else:
        epsilon = 0

print(Q)
print(total)
print(succesful_episodes)

'''
Altering the size of the grid from 4x4 to 8x8 doesn't seem to change the
dificulty in programming because the 8x8 is already built into the frozen
lake environment generator. The Q-value array is much larger for the 8x8 but
the calculation for each Q-value did not change.  The challenging part of the
16x16 grid would be implementing it into the random map generator.

Increasing the grid size wouldn't necessarily change the method in which the
agent learns as it would become more rational as the episodes progressed.
However, with the increased size of the grid there would be more bears in the
grid and it would take more episodes for the agent to learn how to get to the
goal.
'''
