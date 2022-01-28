import random, sys, os
import pygame

def set_colissions(w, h):
    col = []
    for w_up in range(w + 2):
        col.append([w_up, 0])
    for w_down in range(w + 2):
        col.append([w_down, h + 1])
    for h_left in range(h + 2):
        col.append([0, h_left])
    for h_right in range(h + 2):
        col.append([w + 1, h_right])
    return col

def set_food_pos(w, h):
    x = random.randint(1,w)
    y = random.randint(1,h)
    pos = [x,y]
    return pos


class Snake:
    def __init__(self,w,h,controller):
        self.W = w
        self.H = h
        self.controller = controller
        self.pos = [None,None]
        self.score = 0
        self.reset()
        self.memory = []
        self.pos_memory_update()
        self.direction = 'UP'
        self.DEATH = False

    def pos_memory_update(self):
        self.memory.insert(0,[self.pos[0],self.pos[1]])
        self.memory = self.memory[:self.score+5]

    def set_position(self):
        control = self.controller.get_output()
        if control == 0:
            # if self.direction != 'DOWN':
            self.direction = 'UP'
        if control == 1:
            # if self.direction != 'UP':
            self.direction = 'DOWN'
        if control == 2:
            # if self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if control == 3:
            # if self.direction != 'LEFT':
            self.direction = 'RIGHT'
        if control == -1:
            self.direction = 'UP'

        if self.direction == 'UP':
            self.pos[1] -= 1
        if self.direction == 'DOWN':
            self.pos[1] += 1
        if self.direction == 'LEFT':
            self.pos[0] -= 1
        if self.direction == 'RIGHT':
            self.pos[0] += 1

    def reset(self):
        self.score = 0
        self.pos = [self.W//2,self.H//2]
        self.controller.reset()

    def food_eaten(self):
        self.score += 1

    def body(self):
        b = []
        for block in range(self.score + 1):
            b.append(self.memory[block])
        return b



class Environment:
    def __init__(self,size,window_pos,controller):
        self.width = size[0]
        self.height = size[1]
        self.controller = controller
        self.collisions = set_colissions(self.width,self.height)
        self.food_pos = set_food_pos(self.width,self.height)
        self.snake = Snake(self.width,self.height,self.controller)
        self.eaten = False

        # Init to render
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (window_pos[0], window_pos[1])
        pygame.init()
        self.create_window_control = False

    def reset(self):
        f = set_food_pos(self.width, self.height)
        self.food_pos = [f[0],f[1]]
        self.snake.reset()

    def snake_body(self):
        body = self.snake.body()
        return body

    def check_death(self):
        b = self.snake_body()
        pos = [self.snake.pos[0],self.snake.pos[1]]
        if pos in self.collisions or pos in b:
            self.snake.DEATH = True
            self.reset()

    def get_sensors(self):
        head_coord = [self.snake.pos[0],self.snake.pos[1]]
        food_coords = [self.food_pos[0],self.food_pos[1]]
        body_coords = self.snake_body()
        colisions_coords = self.collisions
        direction = self.snake.direction

        s = Senses(head_coord,food_coords,body_coords,colisions_coords,direction)
        senses = s.get_senses()
        return senses

    def run(self):
        self.snake.DEATH = False
        self.eaten = False
        self.snake.set_position()
        self.check_death()
        self.snake.pos_memory_update()

        if self.food_pos == self.snake.pos:
            self.snake.food_eaten()

            self.food_pos = set_food_pos(self.width, self.height)
            while self.food_pos in self.snake_body():
                self.food_pos = set_food_pos(self.width,self.height)

            self.eaten = True

    def render(self,block_size,framerate):
        if self.create_window_control == False:
            self.window = pygame.display.set_mode(((self.width+2) * block_size, (self.height+2) * block_size),pygame.NOFRAME)
        self.create_window_control = True

        self.window.fill((0,0,0))
        clock = pygame.time.Clock()

        # Draw snake
        b = self.snake_body()
        for block in b:
            pygame.draw.rect(self.window, (0, 255, 0),
                             (block[0] * block_size, block[1] * block_size, block_size, block_size))

        # Draw colissions
        for col in self.collisions:
            pygame.draw.rect(self.window,(0,0,255),(col[0]*block_size,col[1]*block_size,block_size,block_size))

        # Draw food
        pygame.draw.rect(self.window,(255,0,0),(self.food_pos[0]*block_size,self.food_pos[1]*block_size,block_size,block_size))

        pygame.display.update()
        clock.tick(framerate)


class Senses:
    def __init__(self,head_coord,food_coords,body_coords,colisions_coords,direction):
        self.head_coord = head_coord
        self.food_coords = food_coords
        self.body_coords = body_coords
        self.colisions_coords = colisions_coords
        self.direction = direction

        self.F_X, self.F_Y, self.C_X, self.C_Y, self.B_X, self.B_Y = [0, 0, 0, 0, 0, 0]

    def get_senses(self):
        # Food:
        self.F_X, self.F_Y = [0,0]
        self.F_X = self.head_coord[0] - self.food_coords[0]
        self.F_Y = self.head_coord[1] - self.food_coords[1]

        # Colisions:
        self.C_X, self.C_Y = [0,0]
        sonda = [self.head_coord[0]+1,self.head_coord[1]]
        if sonda in self.colisions_coords:
            self.C_X = -1
        sonda = [self.head_coord[0] - 1, self.head_coord[1]]
        if sonda in self.colisions_coords:
            self.C_X = 1

        sonda = [self.head_coord[0], self.head_coord[1]+1]
        if sonda in self.colisions_coords:
            self.C_Y = -1
        sonda = [self.head_coord[0], self.head_coord[1]-1]
        if sonda in self.colisions_coords:
            self.C_Y = 1

        # Body:
        self.B_X, self.B_Y = [0, 0]
        sonda = [self.head_coord[0] + 1, self.head_coord[1]]
        if sonda in self.body_coords:
            self.B_X = -1
        sonda = [self.head_coord[0] - 1, self.head_coord[1]]
        if sonda in self.body_coords:
            self.B_X = 1

        sonda = [self.head_coord[0], self.head_coord[1] + 1]
        if sonda in self.body_coords:
            self.B_Y = -1
        sonda = [self.head_coord[0], self.head_coord[1] - 1]
        if sonda in self.body_coords:
            self.B_Y = 1


        return self.F_X, self.F_Y, self.C_X, self.C_Y, self.B_X, self.B_Y




