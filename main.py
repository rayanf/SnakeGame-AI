import pygame  
import sys  
import random

class Sprite(pygame.sprite.Sprite):  
    def __init__(self, pos):  
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.Surface([10, 10])  
        self.rect = self.image.get_rect()  
        self.rect.center = pos  
        self.Direction = None
        self.headPos = pos
        self.tails = []
        self.length = 0
        
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



def generate_food(food_group):
    x = random.randint(0,600)
    y = random.randint(0,600)

    food = Sprite([x,y])
    food.image.fill((110, 215, 45))
 
    food_group.add(food)

    return [x,y]

def main():  
    pygame.init()  
    clock = pygame.time.Clock()  
    fps = 20
    bg = [100, 100, 100]  
    size =[600, 600]  
    screen = pygame.display.set_mode(size)  
    player = Sprite([30, 30])  

    player.move = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]  
    player.vx = 10
    player.vy = 10
    player.image.fill((255, 100, 255))  

    food = Sprite([100, 60])  
    food.image.fill((110, 215, 45))  

    food_group = pygame.sprite.Group()  
    food_group.add(food)  
  
    player_group = pygame.sprite.Group()  
    player_group.add(player)  

    while True:  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                return False

        pressed = pygame.key.get_pressed()

        player.get_direction(pressed)
        player.run()
          
        screen.fill(bg)  
      
        hit = pygame.sprite.spritecollide(player, food_group, True)  

        if hit: 
            generate_food(food_group) 
            


        player_group.draw(screen)  
        food_group.draw(screen)  
        pygame.display.update()  
        clock.tick(fps)  
    pygame.quit()  
    sys.exit  

if __name__ == '__main__':  
    main()