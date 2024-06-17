import pygame
import os

pygame.font.init()

FPS = 60
VVEL = 8
HVEL = 8
BULLET_VEL = 12
MAX_BULLETS = 4
WIN = pygame.display.set_mode((900, 500))
BG = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "pngwing.com.png")), (900, 500))
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
YELLOW_SPACESHIP_SCALED = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_SCALED = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
RESTART_EVENT = pygame.USEREVENT + 3
pygame.display.set_caption("Alien Spaceship!")

LINE = pygame.Rect(445, 0, 10, 500)

HEALTH = 20
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
TIMER_FONT = pygame.font.SysFont("comicsans", 40)
red_health = HEALTH
yellow_health = HEALTH
winner_text = ""
restart_time_left = 0

def handle_missiles(yellow_missiles, red_missiles, yellow, red):
    for missile in yellow_missiles:
        missile.x += BULLET_VEL
        if red.colliderect(missile):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_missiles.remove(missile)
        elif missile.x > 900:
            yellow_missiles.remove(missile)

    for missile in red_missiles:
        missile.x -= BULLET_VEL
        if yellow.colliderect(missile):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_missiles.remove(missile)
        elif missile.x < 0:
            red_missiles.remove(missile)

def draw_window(red, yellow, red_missiles, yellow_missiles, restart_time_left):
    WIN.fill((255, 255, 255))
    WIN.blit(BG, (0, 0))

    WIN.blit(HEALTH_FONT.render("Yellow: " + str(yellow_health), 1, (255, 255, 255)), (10, 10))
    WIN.blit(HEALTH_FONT.render("Red: " + str(red_health), 1, (255, 255, 255)), (700, 10))

    if winner_text != "" :
        WIN.blit(HEALTH_FONT.render(winner_text, 1, (255, 255, 255)), (350, 250))
        if restart_time_left > 0:
            WIN.blit(TIMER_FONT.render(f"Restarting in {restart_time_left}...", 1, (255, 255, 255)), (450, 300))

    WIN.blit(YELLOW_SPACESHIP_SCALED, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP_SCALED, (red.x, red.y))
    
    pygame.draw.rect(WIN, (255, 0, 0), LINE)

    for missile in yellow_missiles:
        pygame.draw.rect(WIN, (255, 255, 0), missile)

    for missile in red_missiles:
        pygame.draw.rect(WIN, (255, 0, 0), missile)

    pygame.display.update()

def handle_yellow_movement(keys, yellow):
    if keys[pygame.K_w] and yellow.y - VVEL > 0:
        yellow.y -= VVEL
    if keys[pygame.K_s] and yellow.y + VVEL + SPACESHIP_HEIGHT < 500:
        yellow.y += VVEL
    if keys[pygame.K_a] and yellow.x - HVEL > 0:
        yellow.x -= HVEL
    if keys[pygame.K_d] and yellow.x + HVEL + SPACESHIP_WIDTH < 450:
        yellow.x += HVEL

def handle_red_movement(keys, red):
    if keys[pygame.K_UP] and red.y - VVEL > 0:
        red.y -= VVEL
    if keys[pygame.K_DOWN] and red.y + VVEL + SPACESHIP_HEIGHT < 500:
        red.y += VVEL
    if keys[pygame.K_LEFT] and red.x - HVEL > 450:
        red.x -= HVEL
    if keys[pygame.K_RIGHT] and red.x + HVEL + SPACESHIP_WIDTH < 900:
        red.x += HVEL

def handle_restart():
    global red_health, yellow_health, winner_text, yellow_missiles, red_missiles, restart_time_left
    red_health = HEALTH
    yellow_health = HEALTH
    winner_text = ""
    yellow_missiles = []
    red_missiles = []
    restart_time_left = 0

yellow_missiles = []
red_missiles = []

def main():
    global red_health, yellow_health, winner_text, restart_time_left
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
            
            if event.type == YELLOW_HIT and yellow_health > 0:
                yellow_health -= 1
                print("Yellow hit")

            if event.type == RED_HIT and red_health > 0:
                red_health -= 1
                print("Red hit")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(yellow_missiles) < MAX_BULLETS:
                    missile = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_missiles.append(missile)

                if event.key == pygame.K_RSHIFT and len(red_missiles) < MAX_BULLETS:
                    missile = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_missiles.append(missile)

            if event.type == RESTART_EVENT:
                handle_restart()
                pygame.time.set_timer(RESTART_EVENT, 0)

        if red_health <= 0 and winner_text == "":
            print("Yellow wins!")
            winner_text = "Yellow wins!"
            restart_time_left = 3
            pygame.time.set_timer(RESTART_EVENT, 1000)

        if yellow_health <= 0 and winner_text == "":
            print("Red wins!")
            winner_text = "Red wins!"
            restart_time_left = 3
            pygame.time.set_timer(RESTART_EVENT, 1000)
        
        if winner_text != "" and restart_time_left > 0:
            restart_time_left -= 1 

        keys = pygame.key.get_pressed()
        handle_yellow_movement(keys, yellow)
        handle_red_movement(keys, red)
        handle_missiles(yellow_missiles, red_missiles, yellow, red)

        draw_window(red, yellow, red_missiles, yellow_missiles, restart_time_left)

    pygame.quit()

if __name__ == "__main__":
    main()
