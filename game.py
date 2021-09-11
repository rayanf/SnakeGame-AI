import pygame  
import sys  
import random
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

    def lock_move_check(self,lock_list,old_direction):
        relativD = ['left','right']
        
        for i in range(2):
            if lock_list[i] == 1:
                if self.snake.direction == relativ_to_absolute(relativD[i],old_direction):
                    print('lock move')
                    return 1
        return 0


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


    def one_step(self,direction,lock_list):
        reward = 0
        self.framIter += 1
        old_direction = self.snake.direction
        self.snake.direction = direction
        self.snake.run()
        if self.crash():                    #check crash to waall or tails
            reward = -10
            done = True
        else: done = False    

        if self.lock_move_check(lock_list,old_direction):
            reward = -10
            done = True
            print('lock')

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


def relativ_to_absolute(relativeDirect,curent_ABSdirection):
        relativD = {'forward':0,'left':1,'right':-1}
        pygame_format_ABSdirection = [pygame.K_UP,pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT]
        curent_ABSdirection_Index = pygame_format_ABSdirection.index(curent_ABSdirection)
        ABS_direction = pygame_format_ABSdirection[(curent_ABSdirection_Index - relativD[relativeDirect])%4]
        return ABS_direction

def absolute_to_relative(curentDirect,Directions):
    direction_Index = {pygame.K_UP : 0 ,pygame.K_RIGHT : 1 ,pygame.K_DOWN : 2 ,pygame.K_LEFT : 3 }
    return (Directions[(direction_Index[curentDirect]%4)], Directions[(direction_Index[curentDirect]-1)%4], Directions[(direction_Index[curentDirect]+1)%4])



    
def is_fuck(game):
    u_d ,r_d ,l_d ,d_d = game.snake.get_danger()
    if  u_d == 1 and r_d == 1 and l_d == 1 and d_d == 1:
        return 1


def is_safe(game,act='forward'):
    if game.snake.direction == pygame.K_UP:
        # print('ok')
        if (game.snake.rect.center[1] - 0) / 20 >= game.snake.length:
            for tail in game.snake.tails:
                if tail.rect.center[1] < game.snake.rect.center[1]:
                    return False
            else: return True


    elif game.snake.direction == pygame.K_RIGHT:
        # print('ok1')

        if (600 - game.snake.rect.center[0]) / 20 >= game.snake.length:
            for tail in game.snake.tails:
                if tail.rect.center[0] > game.snake.rect.center[0]:
                    return False
            else: return True

    elif game.snake.direction == pygame.K_LEFT:
        # print('ok2')

        if (game.snake.rect.center[0] - 0) / 20 >= game.snake.length:
            for tail in game.snake.tails:
                if tail.rect.center[0] < game.snake.rect.center[0]:
                    return False
            else: return True

    elif game.snake.direction == pygame.K_DOWN:
        # print('ok3')

        if (600 - game.snake.rect.center[1]) / 20 >= game.snake.length:
            for tail in game.snake.tails:
                if tail.rect.center[1] > game.snake.rect.center[1]:
                    return False
            else: return True


def check_lock(game):
    actions = ['forward' ,'left' ,'right']
    danger_list = [0,0,0]

    for act in range(3): 

        temp_game = snake_game()
        temp_game.snake.rect.center = game.snake.rect.center
        temp_game.snakeGroup = game.snakeGroup
        temp_game.foods = game.foods
        temp_game.snake.rect.center = game.snake.rect.center
        temp_game.snake.length = game.snake.length
        temp_game.snake.direction = game.snake.direction
        temp_game.snake.tails = game.snake.tails
        temp_game.snake.tailsObject = game.snake.tailsObject
        abs_action = relativ_to_absolute(actions[act], temp_game.snake.direction)
        reward, done, temp_game.snake.length = temp_game.one_step(abs_action,[0,0,0])
        if done:
            danger_list[act] = 1
            del temp_game

        else: 
            danger_list[act] = is_lock(temp_game,1)        
            del temp_game
    return danger_list

def is_lock(game,i):
    print(i)
    if i > 20:
        return 0
    actions = ['forward' ,'left' ,'right']
    danger_list = [0,0,0]

    for act in range(3):
        # print('hah')

        if is_fuck(game):
            danger_list[act] = 1
            del temp_game
            return 1

        temp_game = snake_game()
        temp_game.snake.rect.center = game.snake.rect.center
        temp_game.snakeGroup = pygame.sprite.Group()
        temp_game.foods = game.foods
        temp_game.snake.rect.center = game.snake.rect.center
        temp_game.snake.length = game.snake.length
        temp_game.snake.direction = game.snake.direction
        temp_game.snake.tails = game.snake.tails
        temp_game.snake.tailsObject = game.snake.tailsObject
        abs_action = relativ_to_absolute(actions[act], temp_game.snake.direction)
        reward, done, temp_game.snake.length = temp_game.one_step(abs_action,[0,0,0])
        if done:
            danger_list[act] = 1
            del temp_game
            continue

        if is_safe(temp_game):
            danger_list[act] = 0
            del temp_game
            return 0

        danger_list[act] = is_lock(temp_game,i+1)
        del temp_game

    return 1
     

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