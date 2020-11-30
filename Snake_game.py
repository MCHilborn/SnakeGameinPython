# -*- coding: utf-8 -*-
"""

@author: Micha
"""
from random import randint

class Game:
    #inputs
    IN_UP = "W"
    IN_DOWN = "S"
    IN_LEFT = "A"
    IN_RIGHT = "D"
    
    #directions
    UP = (0, -1) #forgive me Descartes, (0,0) is top left
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
        
    #tile values
    EMPTY = 0
    HEAD = 1
    BODY = 2
    FOOD = 3
    
    DISPLAY_CHARS = { #dictionary
        EMPTY: " ",
        HEAD: "X",
        BODY: "O",
        FOOD: "*"
        }
    
    def __init__(self, height, width): #declare the size of the board
        self.height = height
        self.width = width  
        self.snake = Snake([(5, 3),(5, 4),(5, 5)],(0, 1),False) #starting snake heading down
        self.food = Food((randint(0, 19),randint(0, 9))) #width is 20, height is 10
         
    def board_matrix(self): #return a 2D matrix, a list of lists. This is an empty board
        #make an empty board (2D array)
        board = [[0 for n in range(self.height)] for n in range(self.width)] #thanks geeksforgeeks
        #note: doing this the "C" way results in a pointer, so any reference to an inner list is a pointer
        #to the element in all of the lists
        #instead, use this way!
        #note: I have to figure out why my height and my width are switched for some reason
        head = self.snake.head()
        #add the snake to the board
        for v in self.snake.body:
            board[v[0]][v[1]] = self.BODY #through each tuple in the body assign the value of BODY
        board[head[0]][head[1]] = self.HEAD #refers to coordinates of the head
        #now to render the food
        #food_location is a tuple x,y
        board[self.food.location[0]][self.food.location[1]] = self.FOOD #ERROR: list index out of range sometimes
        #problem solved: remember, 0 indexing.
        return board               
         
    def render(self):
        top_bottom_border = "+" + "-" * self.width + "+"
        matrix = self.board_matrix()
        print(top_bottom_border) #add a border for aesthetic to top and bottom
        #board will be printed line-by-line
        for y in range(0,self.height):
            line = "|"
            for x in range(0,self.width): 
                cell_value = matrix[x][y] #render the corresponding value in the matrix
                line += self.DISPLAY_CHARS[cell_value]
            line += "|"
            print(line)
        print(top_bottom_border)
        print(self.snake.body[:])
        
    def get_input(self):
        new_direction = input().upper() #case matters!
        if(new_direction == self.IN_UP and self.snake.direction != self.DOWN):
            self.snake.set_direction(self.UP)
        elif(new_direction == self.IN_DOWN and self.snake.direction != self.UP):
            self.snake.set_direction(self.DOWN)
        elif(new_direction == self.IN_LEFT and self.snake.direction != self.RIGHT):
            self.snake.set_direction(self.LEFT)
        elif(new_direction == self.IN_RIGHT and self.snake.direction != self.LEFT):
            self.snake.set_direction(self.RIGHT)
        else:
            print("need new input")
            self.get_input() #recursion
 
    def play(self):
        while(1):
            self.get_input() #runs set_directions
            self.snake.take_step(self.snake.direction)
            if self.snake.collision == True:
                break
            if self.snake.head() == self.food.location: #hmmm does this update?
                self.snake.body.insert(0,self.food.location) #insert is better than append
                #otherwise the body doesn't stretch until the previous food location is left
                self.food.regenerate_food()
                if self.food.location in self.snake.body:
                    self.food.regenerate_food()
            self.render()
        print("game over")           
      
class Snake:
    
    def __init__(self,init_body,init_direction,collision_status): #initialize snake with body size and direction
        self.body = init_body #body is a set of tuples that grows as it eats
        self.direction = init_direction
        self.collision = collision_status
    
    def take_step(self, direction): #take a step
        #direction is a tuple
        #tuples are immutable(?!)
        #make a new list
        #have the old list point to the new one
        new_list = []
        for n in range(0,len(self.body)-1):
            new_list.append(self.body[n+1])
        next_position = ((self.body[-1][0]+direction[0])%game.width,(self.body[-1][1]+direction[1])%game.height)
        new_list.append(next_position)
        
        #collisions:
        #self collision
        if next_position in self.body:
            self.collision = True
        #wall collisions
        #going left through the wall
        if self.body[-1][0] == 0 and next_position[0] == game.width-1:
            self.collision = True
        #going right through the wall
        if self.body[-1][0] == game.width-1 and next_position[0] == 0:
            self.collision = True
        #going through top wall
        if self.body[-1][1] == 0 and next_position[1] == game.height-1:
            self.collision = True
        #going through bottom wall
        if self.body[-1][1] == game.height-1 and next_position[1] == 0:
            self.collision = True
        self.body = new_list
    
    def set_direction(self,direction): #takes a tuple as a direction
        self.direction = direction
    
    def head(self):
        return self.body[-1] #before the start of the body
    
class Food:
    
    def __init__(self,init_pos):
        self.location = init_pos #pos is a tuple representing the x and y coordinates
    def regenerate_food(self):
        self.location = (randint(0, 19),randint(0, 9))
        
        
game = Game(10, 20) #instance of Game object
game.render()
game.play()