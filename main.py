# import pygame  
# pygame.init()  
# white = (255, 255, 255)  

# height = 600  
# width = 600  

# display_surface = pygame.display.set_mode((height, width))  
  
# pygame.display.set_caption('Image')  
  
# image = pygame.image.load(r'E:/Photo/photo_2019-07-10_15-51-55.jpg')  
  
# is_blue = True  
# x = 30  
# y = 30  

# while True:  
#     display_surface.fill(white)  
#     display_surface.blit(image, (0, 0))


#     for event in pygame.event.get():  
#         if event.type == pygame.QUIT:  
#             pygame.quit()  
#             quit() 
#         if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  
#             is_blue = not is_blue 


    
#     pressed = pygame.key.get_pressed()  
#     if pressed[pygame.K_UP]: y -= 1
#     if pressed[pygame.K_DOWN]: y += 1  
#     if pressed[pygame.K_LEFT]: x -= 1  
#     if pressed[pygame.K_RIGHT]:  x += 1      

    
#     if is_blue:  
#         color = (0, 128, 255)  
#     else:   
#         color = (255, 100, 0)  

#     pygame.draw.rect(display_surface, color , pygame.Rect(x, y, 60, 60))


#     # if event.type in (pygame.KEYDOWN, pygame.KEYUP):  
#     #     key_name = pygame.key.name(event.key)  
#     #     key_name = key_name.upper()  

#     #     if event.type == pygame.KEYDOWN:  
#     #         print(u'"{}" key pressed'.format(key_name))  

#     #     elif event.type == pygame.KEYUP:  
#     #         print(u'"{}" key released'.format(key_name))  
        
#     pygame.display.update()   




import pygame  
import sys  
#Sprite class   
class Sprite(pygame.sprite.Sprite):  
    def __init__(self, pos):  
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.Surface([20, 20])  
        self.image.fill((255, 100, 255))  
        self.rect = self.image.get_rect()  
        self.rect.center = pos  
        self.Direction = None

def main():  
    pygame.init()  
    clock = pygame.time.Clock()  
    fps = 50
    bg = [100, 100, 100]  
    size =[600, 600]  
    screen = pygame.display.set_mode(size)  
    player = Sprite([30, 30])  

    player.move = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]  
    player.vx = 5 
    player.vy = 5 
  
    wall = Sprite([100, 60])  
  
    wall_group = pygame.sprite.Group()  
    wall_group.add(wall)  
  
    player_group = pygame.sprite.Group()  
    player_group.add(player)  

    while True:  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                return False
    
        key = pygame.key.get_pressed() 

        for i in range(2):  
            if key[player.move[i]]:  
                player.rect.x += player.vx * [-1, 1][i]  
  
        for i in range(2):  
            if key[player.move[2:4][i]]:  
                player.rect.y += player.vy * [-1, 1][i]  

        screen.fill(bg)  
      
        hit = pygame.sprite.spritecollide(player, wall_group, True)  

        if hit:  
            player.image.fill((250, 250, 250))  

        player_group.draw(screen)  
        wall_group.draw(screen)  
        pygame.display.update()  
        clock.tick(fps)  
    pygame.quit()  
    sys.exit  

if __name__ == '__main__':  
    main()