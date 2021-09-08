import pygame  
import sys  
import random



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
        self.Direction = None
        self.headPos = pos
        self.length = 0
        self.tails = []
        self.health = 1
    
    def get_direction(self,pressed):
        for i in range(4):
            if pressed[self.move[i]]:
                key = self.move[i]
                if key == pygame.K_LEFT and self.Direction != pygame.K_RIGHT:
                    self.Direction = key
                elif key == pygame.K_UP and self.Direction != pygame.K_DOWN:
                    self.Direction = key
                elif key == pygame.K_DOWN and self.Direction != pygame.K_UP:
                    self.Direction = key
                elif key == pygame.K_RIGHT and self.Direction != pygame.K_LEFT:
                    self.Direction = key

    def run(self):
        if self.Direction != None:
            for i in range(2):  
                if self.Direction == self.move[i]:  
                    self.rect.x += self.vx * [-1, 1][i]  

                elif self.Direction == self.move[2:4][i]:  
                    self.rect.y += self.vy * [-1, 1][i]

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
                    if self.Direction == self.move[i]:  
                        tail.rect.center = (self.rect.center[0] - 20 * [-1, 1][i],self.rect.center[1])

                    elif self.Direction == self.move[2:4][i]:  
                        tail.rect.center = (self.rect.center[0],self.rect.center[1] - 20 * [-1, 1][i])


                temp_direction1 = tail.Direction
                tail.Direction = self.Direction
                firstCheck = 0
            else:
                temp_pos2 = tail.rect.center
                tail.rect.center = temp_pos1
                temp_pos1 = temp_pos2
                temp_direction2 = tail.Direction
                tail.Direction = temp_direction1
                temp_direction1 = temp_direction2

    def create_tail(self, tail_group):
        for i in range(2):
                if self.Direction == self.move[i]:  
                    pos = (self.rect.center[0] - 20 * [-1, 1][i],self.rect.center[1])

                elif self.Direction == self.move[2:4][i]:  
                    pos = (self.rect.center[0],self.rect.center[1] - 20 * [-1, 1][i])

        tail = Tail(pos)
        tail.Direction = self.Direction
        tail_group.add(tail)
        self.tails.append(tail)



class Food(pygame.sprite.Sprite):  
    def __init__(self, pos):  
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.Surface([20, 20])  
        self.rect = self.image.get_rect()  
        self.rect.center = pos  
        self.image.fill((110, 215, 45))  



def generate_food(food_group,player):
    while True:
        x = random.randint(0,29)*20 + 10
        y = random.randint(0,29)*20 + 10
        for tail in player.tails:
            if tail.rect.center == (x,y):
                pass
        else:
            break
    

    food = Food([x,y])
    food.image.fill((110, 215, 45))
 
    food_group.add(food)

    return [x,y]

def hit():
    pass

class Tail(pygame.sprite.Sprite):  
    def __init__(self, pos):  
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.Surface([20, 20])  
        self.rect = self.image.get_rect()  
        self.rect.center = pos  
        self.image.fill((255, 100, 255)) 
        self.Direction = None
        self.move = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]  
        self.vx = 20 
        self.vy = 20
    


def wall_trigger(player):
    if player.rect.center[0] not in range(0,600) or player.rect.center[1] not in range(0,600):
        player.health -= 1
        reset(player)
        return True
    else:
        return False

def Health_trigger(player):
    if player.health == 0:
        return True
    else: 
        return False

def body_trigger(player):
    reset(player)
    player.health -= 1
    return True
        
def Display_score(player,score,screen):
    score_font = pygame.font.SysFont("comicsansms", 25) 
    value = score_font.render("Score: " + str(score), True, (255, 255, 102))
    # health = score_font.render("Health: " + str(player.health), True, (255, 255, 102))

    screen.blit(value, [0, 0])
    # screen.blit(health, [250, 0])
 
def eat(food_group ,tail_group ,player):
    generate_food(food_group,player) 
    player.length += 1
    player.create_tail(tail_group)

def reset(player):
    player.rect.center = (30,30)
    player.Direction = None
    for tail in player.tails:
        tail.rect.center = (10,30)

def Snake_game():  
    pygame.init()  
    clock = pygame.time.Clock()  
    fps = 25
    bg = (50, 153, 213)
  
    size =[600, 600]  
    screen = pygame.display.set_mode(size)  

    player = Player([30, 30])  
    player_group = pygame.sprite.Group()  
    player_group.add(player)  

    food = Food([110, 70])  
    food_group = pygame.sprite.Group()  
    food_group.add(food)  
  
    tail_group = pygame.sprite.Group()  
    
    GameOver = False
    while not GameOver:  
        wall_trigger(player)
        GameOver = Health_trigger(player)

        screen.fill(bg)  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                return False

        pressed = pygame.key.get_pressed()
        player.get_direction(pressed)
        player.run()
        player.tail_run()

        if pygame.sprite.spritecollide(player, food_group, True) : eat(food_group,tail_group, player)            
        if pygame.sprite.spritecollide(player, tail_group, True) : body_trigger(player)

        Display_score(player,player.length,screen)
        player_group.draw(screen)  
        food_group.draw(screen) 
        tail_group.draw(screen) 
        pygame.display.update()  
        clock.tick(fps)  
    pygame.quit()  
    sys.exit  
    return player.length

if __name__ == '__main__':  
    while True:
        score = Snake_game()
