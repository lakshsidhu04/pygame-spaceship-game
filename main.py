import pygame
import os

FPS = 60
VVEL = 8
HVEL = 8
BULLET_VEL = 12
WIN = pygame.display.set_mode((900, 500))
BG = pygame.image.load(os.path.join("Assets", "space.png"))
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
YELLOW_SPACESHIP_SCALED = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_SCALED = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

pygame.display.set_caption("Alien Spaceship!")

LINE = pygame.Rect(445, 0, 10, 500)
RED_BULLET = pygame.Rect(0, 0, 5, 5)
YELLOW_BULLET = pygame.Rect(0, 0, 5, 5)

def draw_window(red, yellow):
    WIN.fill((255, 255, 255))
    WIN.blit(BG, (0, 0))
    pygame.draw.rect(WIN, (255, 0, 0), LINE)
    WIN.blit(YELLOW_SPACESHIP_SCALED, (yellow.x , yellow.y))
    WIN.blit(RED_SPACESHIP_SCALED, (red.x, red.y))
    pygame.display.update()

def handle_yellow_movement(keys, yellow):
    if keys[pygame.K_w]:
        yellow.y -= VVEL
    if keys[pygame.K_s]:
        yellow.y += VVEL
    if keys[pygame.K_a]:
        yellow.x -= HVEL
    if keys[pygame.K_d]:
        yellow.x += HVEL

    if yellow.x - HVEL < 0:
        yellow.x = HVEL
    
    if yellow.x + HVEL > 450 - SPACESHIP_WIDTH:
        yellow.x = 450 - SPACESHIP_WIDTH - HVEL

    if yellow.y - VVEL < 0:
        yellow.y = VVEL

    if yellow.y + VVEL > 500 - SPACESHIP_HEIGHT:
        yellow.y = 500 - SPACESHIP_HEIGHT - VVEL

def handle_red_movement(keys, red):
    if keys[pygame.K_UP]:
        red.y -= VVEL
    if keys[pygame.K_DOWN]:
        red.y += VVEL
    if keys[pygame.K_LEFT]:
        red.x -= HVEL
    if keys[pygame.K_RIGHT]:
        red.x += HVEL

    if red.x < 450:
        red.x = 450
    if red.x > 900 - SPACESHIP_WIDTH:
        red.x = 900 - SPACESHIP_WIDTH
    
    if red.y < 0:
        red.y = 0
    if red.y > 500 - SPACESHIP_HEIGHT:
        red.y = 500 - SPACESHIP_HEIGHT

def handle_yellow_fire(keys, yellow):
    if keys[pygame.K_SPACE]:
        bullet = pygame.Rect(yellow.x, yellow.y, 5, 5)
        return bullet

def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    clock = pygame.time.Clock()
    run = True 
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quit")
                run = False
        keys = pygame.key.get_pressed()
        handle_yellow_movement(keys, yellow)
        handle_red_movement(keys, red)
        
        yellow_bullet = handle_yellow_fire(keys, yellow)
        if yellow_bullet:
            
    
        draw_window(red, yellow)

    pygame.quit()

if __name__ == "__main__":
    main()