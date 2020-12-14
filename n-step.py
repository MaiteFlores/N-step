##Maite Flores
##Nov 2020

import turtle
import math
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from tkinter import *



blocked = 0.0 #color
player = 0.3 #color
goal = 0.9 #color

epsilon = 0.7
learning_rate = 0.7
discount = 0.9

dif_actions = [0,1,2,3]
# 1 = UP
# 3 = DOWN
# 0 = LEFT 
# 2 = RIGHT

class Maze(object):
    def __init__(self, maze, runner = (0,0)):
        self._maze = np.array(maze)
        x,y = self._maze.shape
        self.goal = (x-1,y-1)
        #self.empty =[(r,c) for r in range(x) for c in range(y) if self._maze[r,c] == 1.0]
        #self.border = [[(r,c) for r in range(x) for c in range(y) if self._maze[r,c] == 0.0]]
        #self.visited_square = []
        self.restart(runner)


     #restarts the maze 
    def restart(self, runner):
        self.maze = np.copy(self._maze)
        self.visited_square = set()
        reset_x,reset_y = self._maze.shape
        self.runner = runner
        runner_xcor, runner_ycor = runner
        self._maze[runner_xcor,runner_ycor] = player
        self.state = (runner_xcor, runner_ycor, 'start')
        self.min_reward = -.3 * (reset_x*reset_y)
        self.final_reward = 0

        
    #does the move 
    def change_state(self, move):
        # xcor, ycor = self._maze.shape
        new_xcor,new_ycor, new_mode = runner_xcor, runner_ycor, mode = self.state
        if self.maze[runner_xcor, runner_ycor] > 0.0:
            self.visited_square.add((runner_xcor, runner_ycor))

        is_valid = self.check_move()

        if not is_valid:
            new_mode = 'barrier'
        elif move in is_valid:
            new_mode = 'running'
            if move == 0: #left
                new_ycor-=1
            elif move == 1: #up
                new_xcor -=1
            if move == 2: #right
                new_ycor +=1
            elif move == 3: #down
                new_xcor+=1
        else:
            new_mode = 'stop'

        self.state = (new_xcor,new_ycor, new_mode)
                
         
    #does the action 
    def moves(self, decision):
        self.change_state(decision)
        score = self.reward()
        self.final_reward += score
        check_is_over = self.is_over()
        return score, check_is_over

    #gets reward
    def reward(self):
        runner_xcor, runner_ycor, mode = self.state
        new_xcor,new_ycor = self._maze.shape
        if runner_xcor == new_xcor-1 and runner_ycor == new_ycor-1:
            return 10.00
        if mode == 'barrier':
            return self.min_reward -0.50
        if mode == 'running':
            return -0.1
        if mode == 'stop':
            return -0.25
        if (runner_xcor, runner_ycor) in self.visited_square:
            return -0.20

    #checks state of playing 
    def is_over(self):
        if self.final_reward < self.min_reward:
            return 'Lost'
        runner_xcor,runner_ycor, mode = self.state
        x_axis,y_axis = self._maze.shape
        if (runner_xcor,runner_ycor) ==  self.goal:
            return 'Winner'
        return 'Playing'
        

    def check_move(self,cell = NONE):

        if cell is NONE:
            cur_xcor, cur_ycor, mode = self.state
        else:
            cur_xcor, cur_ycor = cell

        valid_actions = [0,1,2,3]
        #Up, down, left, right
        x_axis, y_axis = self._maze.shape

        if cur_xcor == 0:
            valid_actions.remove(1)
        elif cur_xcor == x_axis-1:
            valid_actions.remove(3)
        if cur_ycor == 0:
            valid_actions.remove(0)
        elif cur_ycor == y_axis - 1:
            valid_actions.remove(2)

        if cur_xcor > 0 and self._maze[cur_xcor-1, cur_ycor] == 0.0:
            valid_actions.remove(1)
        if cur_xcor < x_axis-1 and self._maze[cur_xcor+1, cur_ycor] == 0.0:
            valid_actions.remove(3)
        if cur_ycor > 0 and self._maze[cur_xcor, cur_ycor-1] == 0.0:
            valid_actions.remove(0)
        if cur_ycor < y_axis-1 and self._maze[cur_xcor,cur_ycor+1] == 0.0:
            valid_actions.remove(2)

        return valid_actions
        
        

maze =[
    [ 1.,  1.,  1.,  0.,  1.,  1.,  1.,  1.,  1.,  1.],
    [ 1.,  0.,  0.,  1.,  1.,  0.,  1.,  1.,  1.,  1.],
    [ 1.,  1.,  1.,  1.,  1.,  0.,  0.,  1.,  0.,  1.],
    [ 1.,  0.,  1.,  0.,  1.,  1.,  1.,  1.,  0.,  1.],
    [ 0.,  1.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  1.],
    [ 1.,  1.,  0.,  1.,  1.,  1.,  1.,  1.,  1.,  1.],
    [ 1.,  1.,  1.,  1.,  0.,  1.,  1.,  1.,  1.,  1.],
    [ 1.,  0.,  1.,  1.,  1.,  1.,  0.,  0.,  0.,  0.],
    [ 1.,  0.,  0.,  0.,  0.,  0.,  1.,  1.,  1.,  0.],
    [ 1.,  1.,  1.,  1.,  1.,  1.,  1.,  0.,  1.,  1.]
]


def create_maze(maze):
    plt.grid('on')
    x,y = maze._maze.shape
    #fig= plt.subplots()
    axis = plt.gca()
    #im = axis.imshow(maze)
    axis.set_xticks(np.arange(x))
    axis.set_yticks(np.arange(y))
    axis.set_xticklabels([])
    axis.set_yticklabels([])
    pic = np.copy(maze._maze)        
    #print(x,y)
    for row,col in maze.visited_square:
        pic[row,col] = 0.6
    runner_xcor, runner_ycor, runner_mode = maze.state
    pic[runner_xcor, runner_ycor] = 0.3   #runner
    pic[x-1, y-1] = 0.7 # finish line
            
    axis.set_title("N-Step Maze")
    
    img = plt.imshow(pic,interpolation='none',cmap = 'gray')
    #fig.tight_layout()
    #plt.show()
    plt.ion()
    plt.pause(0.15)
    plt.show()
    return img

##########################################################################################




##########################################################################################
table_rows = 20
table_cols = 20
##
##q_vals = np.zeros((table_rows, table_cols, 4))


#def create_qtable_and_rewards(maze):
q_vals = np.zeros((table_rows, table_cols,4))

##def remember(self, episode):
##    memory = list()
##    max_mem = 100
##    # episode = [envstate, action, reward, envstate_next, game_over]
##    # memory[i] = episode
##    # envstate == flattened 1d maze cells info, including rat cell (see method: observe)
##    memory.append(episode)
##    if len(memory) > max_memory:
##        del memory[0]

#
def updateQ(old_x, old_y, new_x, new_y, action, reward):
    old_q_val = q_vals[old_x, old_y, action]
    temp = reward + (discount * np.max(q_vals[new_x, new_y])) - old_q_val
    new_q_val = old_q_val + (learning_rate * temp)
    q_vals[old_x, old_y, action] = new_q_val



def train_(maze):
    #maze = Maze(maze)
    win_count=0
    epoch=100
    count = 0
    #max_memory = 500

    #experience = Experience(maze, max_memory=max_memory)
    for e in range(epoch):
            count+=1
        # for episode in range(game_amount):
            
            #if you want random start
            #runner_cell = random.choice(maze.empty)
            #maze.restart(runner_cell)
            runner_cell = (0, 0)
            maze.restart(runner_cell)
            game_over = False
 
            # get initial envstate (1d flattened canvas)
            #envstate = maze.check_state()

        # n_episodes = 0
            while not game_over:
                valid_actions = maze.check_move()
                if not valid_actions: break
                #prev_envstate = envstate
                action = get_next_action(maze, q_vals)
            
                old_x, old_y, mode = maze.state
                # Apply action, get reward and new envstate
                reward, game_status = maze.moves(action)
                if game_status == 'Winner':
                    win_count=win_count+1
                    game_over = True
                elif game_status == 'Lost':
                    game_over = True
                else:
                    game_over = False

                new_x, new_y, mode = maze.state
                # update Q
                updateQ(old_x, old_y, new_x, new_y, action, reward)

            print(count,'/', epoch)


def get_next_action(maze, q_vals):
    valid_actions = maze.check_move()
    # Get next action
    if np.random.rand() > epsilon:
        action = random.choice(valid_actions)
    else:
        cur_x, cur_y, mode = maze.state
        action = np.argmax(q_vals[cur_x, cur_y])
    return action
        

def get_shortest_path(maze):
    runner_cell = (0, 0)
    maze.restart(runner_cell)
    game_over = False

    total_reward = 0; 
    #envstate = maze.check_state()
    #_moves =0

# n_episodes = 0
    while not game_over:
        valid_actions = maze.check_move()
        if not valid_actions: break
        #prev_envstate = envstate
        cur_x, cur_y, mode = maze.state
        action = np.argmax(q_vals[cur_x, cur_y])
    
        # Apply action, get reward and new envstate
        reward, game_status = maze.moves(action)
        print("Reward per move: ", reward)
        total_reward = total_reward + reward
        if game_status == 'Winner':
            print("Win!")
            game_over = True
        elif game_status == 'Lost':
            print("Loser!")
            game_over = True
        else:
            game_over = False

        #_moves=_moves+1
        create_maze(maze)
    
    #create_maze(maze)
    #print("Steps: ", _moves)
    print("Final score: ",total_reward)

gen = Maze(maze)
gen1 = Maze(maze)
gen2 = Maze(maze)
gen3 = Maze(maze)

#train_(gen)
train_(gen1)
train_(gen2)
train_(gen3)

get_shortest_path(gen)



