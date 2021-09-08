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
        self.snake.direction = None
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


    def one_step(self,direction):
        reward = 0
        self.framIter += 1
        self.snake.direction = direction
        self.snake.run()
        if self.crash():                    #check crash to waall or tails
            reward = -10
            done = True
        else: done = False    

        if self.eat(): reward = +10          #check eat foods

        self.update_screen()
        self.clock.tick(self.fps)  

        return reward, done, self.snake.length

    def update_screen(self):
        # score_font = pygame.font.SysFont("comicsansms", 25) 

        # value = score_font.render("Score: " + str(self.snake.length), True, (255, 255, 102))

        self.screen.fill((50, 153, 213))
        # self.screen.blit(value, [0, 0])
        self.snakeGroup.draw(self.screen)  
        self.foods.draw(self.screen) 
        self.snake.tailsObject.draw(self.screen) 
        pygame.display.update()  

        pygame.display.flip()



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
        self.direction = None
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
                    left_danger.append(tail.rect.center[0] - self.rect.center[0])
                else:
                    right_danger.append(self.rect.center[0] - tail.rect.center[0])

            if tail.rect.center[0] == self.rect.center[0]:
                            if tail.rect.center[1] > self.rect.center[1]:
                                up_danger.append(tail.rect.center[1] - self.rect.center[1])
                            else:
                                down_danger.append(self.rect.center[1] - tail.rect.center[1])

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
    pygame.init()
    game = snake_game()
    game.reset()
    
    while True:
        game.one_step(pygame.K_UP)
        game.one_step(pygame.K_DOWN)