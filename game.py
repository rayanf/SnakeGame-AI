import pygame  
import sys  
import random
import networkx as nx
from edges import edges
class snake_game:
    def __init__(self):
        self.w = 600
        self.h = 600
        self.snake_size = 20
        self.fps = 40

        self.screen = pygame.display.set_mode([self.w,self.h])  
        self.clock = pygame.time.Clock()  
        self.framIter = 0

        self.snake = Player([290,290])
        self.snakeGroup = pygame.sprite.Group()
        self.snakeGroup.add(self.snake) 
        self.foods = pygame.sprite.Group()
        
        self.graph = nx.Graph()
        self.graph.add_edges_from(edges)
        
    def reset(self):
        self.snake.rect.center = (290,290)
        self.snake.direction = pygame.K_UP
        self.snake.length = 0
        self.snake.tails = []
        self.snake.tailsObject = pygame.sprite.Group()
        self.foods = pygame.sprite.Group()
        self.screen = pygame.display.set_mode([self.w,self.h])  
        self.framIter = 0          
        self.update_screen()
        self.generate_food()


    def crash(self):
        if self.snake.rect.center[0] not in range(0,self.w) or self.snake.rect.center[1] not in range(0,self.w):
            return True
        elif pygame.sprite.spritecollide(self.snake, self.snake.tailsObject, True):
            return True 
        else: return False

    def eat(self):
        if  pygame.sprite.spritecollide(self.snake, self.foods, True):
            self.generate_food() 
            self.snake.length += 1
            self.snake.create_tail(self.snake.tailsObject)
            return True
        
        else: return False


    def generate_food(self):
        while True:
            x = random.randint(0,29)*20 + 10
            y = random.randint(0,29)*20 + 10
            for tail in self.snake.tails:
                if tail.rect.center == (x,y):
                    pass
            else:
                break

        food = Food([x,y])
        food.image.fill((110, 215, 45))
        self.foods.add(food)
        self.currentfood = food
        return [x,y]

    def lock_move(self,old_direction,lock_list):
        relativD = ['forward','left','right']
        
        for i in range(3):
            if lock_list[i] == 0:
                if self.snake.direction == relativ_to_absolute(relativD[i],old_direction):
                    return True
        return False
        
    def one_step(self,direction,lock_list):
        reward = 0
        self.framIter += 1
        old_direction = self.snake.direction
        self.snake.direction = direction
        self.snake.run()
        if self.crash():                    #check crash to waall or tails
            reward = -10
            done = True
        elif self.lock_move(old_direction,lock_list): 
            reward = -10
            done = True
            print('thats wrong')
        else:
            done = False    

        
        if self.eat(): reward = +10          #check eat foods

        return reward, done, self.snake.length

    def update_screen(self):
        score_font = pygame.font.SysFont("comicsansms", 25) 

        value = score_font.render("Score: " + str(self.snake.length), True, (255, 255, 102))

        self.screen.fill((50, 153, 213))
        self.screen.blit(value, [0, 0])
        self.snakeGroup.draw(self.screen)  
        self.foods.draw(self.screen) 
        self.snake.tailsObject.draw(self.screen) 
        pygame.display.update()  

        pygame.display.flip()

             
    def get_next_move_pos(self,direction):
        abs_direction = relativ_to_absolute(direction,self.snake.direction)
        current_point = self.snake.rect.center

        for i in range(2):  
            if abs_direction == self.snake.move[i]:  
                current_point =  (current_point[0] + self.snake.vx * [-1, 1][i]  ,current_point[1])

            elif abs_direction == self.snake.move[2:4][i]:  
                current_point = (current_point[0] ,current_point[1] + self.snake.vy * [-1, 1][i])

        return current_point

    def check_into_ground(self,point):
        if point[0] < 600 and point[0] > 0 and point[1] > 0 and point[1] < 600:
            return True
        else: return False



    def check_path(self):
        graph = self.graph.copy()
        graph = self.remove_tails_graph(graph)

        forward_point = self.get_next_move_pos('forward')
        try:
            if self.check_into_ground(forward_point):
                forward_path = nx.has_path(graph, self.get_graph_node(forward_point), self.get_graph_node(self.currentfood.rect.center))
            else: forward_path = False
        except : forward_path = False
        try:
            left_point = self.get_next_move_pos('left')
            if self.check_into_ground(left_point):
                left_path = nx.has_path(graph, self.get_graph_node(left_point), self.get_graph_node(self.currentfood.rect.center))
            else: left_path = False
        except : left_path = False

        try:
            right_point = self.get_next_move_pos('right')
            if self.check_into_ground(right_point):
                right_path = nx.has_path(graph, self.get_graph_node(right_point), self.get_graph_node(self.currentfood.rect.center))
            else: right_path = False
        except: right_path = False
        # self.graph.add_edges_from(edges)
        del graph
        return (forward_path, left_path, right_path )

    def get_graph_node(self,point):
        node = int(str(point[0]) + str(point[1]))
        return node

    def remove_tails_graph(self,graph):
        nodes = []
        for tail in self.snake.tails:
            nodes.append(self.get_graph_node(tail.rect.center))
        if self.check_into_ground(self.snake.rect.center):
            nodes.append(self.get_graph_node(self.snake.rect.center))
        
        graph.remove_nodes_from(nodes)
        return graph



def relativ_to_absolute(relativeDirect,curent_ABSdirection):
        relativD = {'forward':0,'left':1,'right':-1}
        pygame_format_ABSdirection = [pygame.K_UP,pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT]
        curent_ABSdirection_Index = pygame_format_ABSdirection.index(curent_ABSdirection)
        ABS_direction = pygame_format_ABSdirection[(curent_ABSdirection_Index - relativD[relativeDirect])%4]
        return ABS_direction

def absolute_to_relative(curentDirect,Directions):
    direction_Index = {pygame.K_UP : 0 ,pygame.K_RIGHT : 1 ,pygame.K_DOWN : 2 ,pygame.K_LEFT : 3 }
    return (Directions[(direction_Index[curentDirect]%4)], Directions[(direction_Index[curentDirect]-1)%4], Directions[(direction_Index[curentDirect]+1)%4])


     

class Player(pygame.sprite.Sprite):  
    def __init__(self, pos):  
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.Surface([20, 20])  
        self.rect = self.image.get_rect()  
        self.image.fill((155, 0, 155))  
        self.move = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]  
        self.vx = 20
        self.vy = 20
        self.rect.center = pos  
        self.direction = pygame.K_UP
        self.length = 0
        self.tails = []
        self.tailsObject = pygame.sprite.Group()


    def run(self):
        if self.direction != None:
            for i in range(2):  
                if self.direction == self.move[i]:  
                    self.rect.x += self.vx * [-1, 1][i]  

                elif self.direction == self.move[2:4][i]:  
                    self.rect.y += self.vy * [-1, 1][i]


            self.tail_run()

    def tail_run(self):
        temp_direction1 = None
        temp_direction2 = None
        temp_pos1 = None
        temp_pos2 = None
        firstCheck = 1
        for tail in self.tails:
            if firstCheck == 1:
                temp_pos1 = tail.rect.center
                
                for i in range(2):
                    if self.direction == self.move[i]:  
                        tail.rect.center = (self.rect.center[0] - 20 * [-1, 1][i],self.rect.center[1])

                    elif self.direction == self.move[2:4][i]:  
                        tail.rect.center = (self.rect.center[0],self.rect.center[1] - 20 * [-1, 1][i])


                temp_direction1 = tail.direction
                tail.direction = self.direction
                firstCheck = 0
            else:
                temp_pos2 = tail.rect.center
                tail.rect.center = temp_pos1
                temp_pos1 = temp_pos2
                temp_direction2 = tail.direction
                tail.direction = temp_direction1
                temp_direction1 = temp_direction2

    def create_tail(self, tail_group):
        for i in range(2):
                if self.direction == self.move[i]:  
                    pos = (self.rect.center[0] - 20 * [-1, 1][i],self.rect.center[1])

                elif self.direction == self.move[2:4][i]:  
                    pos = (self.rect.center[0],self.rect.center[1] - 20 * [-1, 1][i])

        tail = Tail(pos)
        tail.direction = self.direction
        tail_group.add(tail)
        self.tails.append(tail)

    def get_danger(self):
        up_danger = [abs(0 - self.rect.center[1])]
        right_danger = [abs(600 - self.rect.center[0])]
        down_danger = [abs(600 - self.rect.center[1])]
        left_danger = [abs(0 - self.rect.center[0])]

        for tail in self.tails:
            if tail.rect.center[1] == self.rect.center[1]:
                if tail.rect.center[0] > self.rect.center[0]:
                    right_danger.append(tail.rect.center[0] - self.rect.center[0])
                else:
                    left_danger.append(self.rect.center[0] - tail.rect.center[0])

            if tail.rect.center[0] == self.rect.center[0]:
                if tail.rect.center[1] > self.rect.center[1]:
                    down_danger.append(tail.rect.center[1] - self.rect.center[1])
                else:
                    up_danger.append(self.rect.center[1] - tail.rect.center[1])

        return min(up_danger), min(right_danger), min(left_danger), min(down_danger)



class Tail(pygame.sprite.Sprite):  
    def __init__(self, pos):  
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.Surface([20, 20])  
        self.rect = self.image.get_rect()  
        self.rect.center = pos  
        self.image.fill((255, 100, 255)) 
        self.direction = None
        self.move = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]  
        self.vx = 20 
        self.vy = 20




class Food(pygame.sprite.Sprite):  
    def __init__(self, pos):  
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.Surface([20, 20])  
        self.rect = self.image.get_rect()  
        self.rect.center = pos  
        self.image.fill((110, 215, 45))  






if __name__ == '__main__':  
    pass