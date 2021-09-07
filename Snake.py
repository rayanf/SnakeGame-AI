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

            for i in range(2):  
                if self.Direction == self.move[2:4][i]:  
                    self.rect.y += self.vy * [-1, 1][i]



class Food(pygame.sprite.Sprite):  
    def __init__(self, pos):  
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.Surface([20, 20])  
        self.rect = self.image.get_rect()  
        self.rect.center = pos  
        self.image.fill((110, 215, 45))  

def generate_food(food_group):
    x = random.randint(0,600)
    y = random.randint(0,600)

    food = Food([x,y])
    food.image.fill((110, 215, 45))
 
    food_group.add(food)

    return [x,y]

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

    def run(self):
        if self.Direction != None:
            for i in range(2):  
                if self.Direction == self.move[i]:  
                    self.rect.x += self.vx * [-1, 1][i]  

            for i in range(2):  
                if self.Direction == self.move[2:4][i]:  
                    self.rect.y += self.vy * [-1, 1][i] 



def wall_trigger(player):
    if player.rect.center[0] not in range(0,600) or player.rect.center[1] not in range(0,600):
        return True
    else:
        return False

def Health_trigger(player):
    if player.health == 0:
        return True
    else: 
        return False

# def body_trigger(player):
#     for tail in 



def Display_score(player,score,screen):
    score_font = pygame.font.SysFont("comicsansms", 35) 
    value = score_font.render("Your Score: " + str(score), True, (255, 255, 102))
    health = score_font.render("Your Health: " + str(player.health), True, (255, 255, 102))

    screen.blit(value, [0, 0])
    screen.blit(health, [250, 0])
 
def Snake_game():  
    pygame.init()  
    clock = pygame.time.Clock()  
    fps = 20
    bg = (50, 153, 213)
  
    size =[600, 600]  
    screen = pygame.display.set_mode(size)  

    player = Player([30, 30])  
    player_group = pygame.sprite.Group()  
    player_group.add(player)  

    food = Food([100, 60])  
    food_group = pygame.sprite.Group()  
    food_group.add(food)  
  
    tail_group = pygame.sprite.Group()  
    
    GameOver = False
    while not GameOver:  
        if wall_trigger(player):
            player.health -= 1
            

        GameOver = Health_trigger(player)

        screen.fill(bg)  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                return False

        pressed = pygame.key.get_pressed()
        player.get_direction(pressed)
        player.run()

        temp_direction1 = None
        temp_direction2 = None
        firstCheck = 1
        for tail in player.tails:
            if firstCheck == 1:
                tail.run()
                temp_direction1 = tail.Direction
                tail.Direction = player.Direction
                firstCheck = 0
            else:
                tail.run() 
                temp_direction2 = tail.Direction
                tail.Direction = temp_direction1
                temp_direction1 = temp_direction2

        hit = pygame.sprite.spritecollide(player, food_group, True)  
        if hit: 
            generate_food(food_group) 
            player.length += 1
            tail = Tail(player.rect.center)
            tail.Direction = player.Direction
            tail_group.add(tail)
            player.tails.append(tail)

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
    score = Snake_game()
    print(score)