import pygame
from sys import exit
import random

def main():

    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    clock = pygame.time.Clock()
    active = False
    score = 0
    
    # Background adn text assets
    sky_surf = pygame.image.load("sprites/sky.png").convert_alpha()
    ground_surf = pygame.image.load("sprites/ground.png").convert_alpha()
        
    text_font = pygame.font.Font("font/Pixeltype.ttf", 70)
    text_surf = text_font.render("Bird Dodger", False, "Black")
    text_rect = text_surf.get_rect(center = (400, 100))
    
    # Sound assets
    music = pygame.mixer.Sound("audio/arcade_kid.mp3")
    music.set_volume(0.5)
    music.play(loops = -1)

    jump_sound = pygame.mixer.Sound("audio/jump_08.wav")
    jump_sound.set_volume(0.2)
    
    # Hero assets
    hero_idle_1 = pygame.image.load("sprites/hero_idle1.png").convert_alpha()
    hero_idle_2 = pygame.image.load("sprites/hero_idle2.png").convert_alpha()

    hero_walk_1 = pygame.image.load("sprites/hero_walk1.png").convert_alpha()
    hero_walk_2 = pygame.image.load("sprites/hero_walk2.png").convert_alpha()
    hero_walk_3 = pygame.image.load("sprites/hero_walk3.png").convert_alpha()
    hero_walk_4 = pygame.image.load("sprites/hero_walk4.png").convert_alpha()
    hero_walk_5 = pygame.image.load("sprites/hero_walk5.png").convert_alpha()
    hero_walk_6 = pygame.image.load("sprites/hero_walk6.png").convert_alpha()

    hero_duck_1 = pygame.image.load("sprites/hero_duck.png").convert_alpha()

    hero_idle = [hero_idle_1, hero_idle_2]
    hero_walk = [hero_walk_1, hero_walk_2, hero_walk_3, hero_walk_4, hero_walk_5, hero_walk_6]
    hero_duck = [hero_duck_1]
    
    hero_assets = [hero_idle, hero_walk, hero_duck]
    
    flip = False
    animation = 0
    hero_frames_index = 0
    hero_gravity = 0
    hero_surf = hero_assets[animation][hero_frames_index]
    hero_rect = hero_surf.get_rect(midbottom = (400, 300))
    
    # Bird assets
    bird_fly_1 = pygame.image.load("sprites/bird_1.png").convert_alpha()
    # bird_fly_2 = pygame.image.load("sprites/bird_2.png").convert_alpha()
    bird_fly_3 = pygame.image.load("sprites/bird_3.png").convert_alpha()

    bird_frames = [bird_fly_1, bird_fly_3]
    bird_frames_index = 0
    bird_surf = bird_frames[bird_frames_index]

    bird_y = random.randint(150, 250)
    bird_x = 900
    bird_speed = 5
    bird_rect = bird_surf.get_rect(midbottom = (bird_x, bird_y))

    bird_animation_timer = pygame.USEREVENT +1
    pygame.time.set_timer(bird_animation_timer, 200)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                exit()
            
            if active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and hero_rect.bottom == 300:
                        jump_sound.play()
                        hero_gravity = -20
                
                if event.type == bird_animation_timer:
                    if bird_frames_index == 0:
                        bird_frames_index = 1
                    else:
                        bird_frames_index = 0
                    bird_surf = bird_frames[bird_frames_index]
 
        if active:
            # Player movement
            hero_gravity += 1   # Gravity
            hero_rect.y += hero_gravity
            if hero_rect.bottom > 300:
                hero_rect.bottom = 300
            
            if hero_rect.bottom < 300: # Jumping animation
                hero_surf = hero_walk[4] # Same image used in walking animation
                if flip:
                    hero_surf = pygame.transform.flip(hero_walk[4], True, False)

            keys = pygame.key.get_pressed() 
            
            if keys[pygame.K_RIGHT]:    # Movement, right
                if hero_rect.bottom == 300:
                    animation, hero_surf, hero_frames_index, flip = hero_move_animation(hero_assets[1], hero_frames_index, "right")
                hero_rect.right += 5
            
            elif keys[pygame.K_LEFT]:    # Movement, left
                if hero_rect.bottom == 300:
                    animation, hero_surf, hero_frames_index, flip = hero_move_animation(hero_assets[1], hero_frames_index, "left")
                hero_rect.left -= 5
            
            elif keys[pygame.K_DOWN] and hero_rect.bottom == 300:    # Ducking
                animation, hero_surf, flip = hero_duck_animation(hero_assets[2], flip)
                hero_rect.bottom = 325
            
            elif hero_rect.bottom == 300:    # Idle animation
                animation, hero_surf, hero_frames_index = hero_idle_animation(hero_assets[0], hero_frames_index, flip)

            if hero_rect.x == 900:    # Travel thorugh border, right
                hero_rect.x = -100
            
            elif hero_rect.x == -100:    # Travel through border, left
                hero_rect.x = 900

            # Collision
            if hero_rect.colliderect(bird_rect):
                hero_rect.midbottom = (400, 300)
                read_score(score)
                active = False
            
            # Bird movement
            bird_rect.left -= bird_speed
            if bird_rect.right < 0:
                score += 1
                bird_speed = random.randint(5, 20)
                bird_y = random.randint(150, 299)
                bird_rect.midbottom = (bird_x, bird_y)
                if score >= 10:
                    bird_speed = (score * 1.1)

            # Update score
            score_font = pygame.font.Font("font/Pixeltype.ttf", 40)
            score_surf = score_font.render(f"score: {score}", False, "Black")
            score_rect = score_surf.get_rect(center = (70, 20))
        
            # Draw on screen
            screen.blit(sky_surf, (0, 0))
            screen.blit(ground_surf, (0, 300))
            screen.blit(bird_surf, bird_rect)
            screen.blit(hero_surf, hero_rect)
            screen.blit(score_surf, score_rect)
            
        else:
            score = 0
            bird_speed = 5
            bird_x = 900

            # Update highscore
            with open("high_score.txt") as file:
                high_score = file.readline()
            high_score_font = pygame.font.Font("font/Pixeltype.ttf", 50)
            high_score_surf = high_score_font.render(f"Best Score: {high_score}", False, "Black")    
            high_score_rect = high_score_surf.get_rect(center = (650, 200))
            
            screen.blit(sky_surf, (0, 0))
            screen.blit(high_score_surf, high_score_rect)
            screen.blit(ground_surf, (0, 300))
            screen.blit(text_surf, text_rect)
            screen.blit(hero_surf, hero_rect)
            animation, hero_surf, hero_frames_index = hero_idle_animation(hero_assets[0], hero_frames_index, flip)

            keys = pygame.key.get_pressed() 
            if keys[pygame.K_RETURN]:
                bird_rect.midbottom = (bird_x, bird_y)
                hero_rect.midbottom = (400, 300)
                active = True
        
        pygame.display.update()
        clock.tick(60)

def hero_idle_animation(frames, index, flip):
    animation = 0
    index += 0.03
    
    if index > len(frames):
        index = 0
    if flip:
        surf = pygame.transform.flip(frames[int(index)], True, False)
    else:
        surf = frames[int(index)]

    return animation, surf, index

def hero_move_animation(frames, index, state, flip=False):
    animation = 1
    index += 0.23
    
    if index > len(frames):
        index = 0
    if state == "left":
        surf = pygame.transform.flip(frames[int(index)], True, False)
        flip = True
    elif state =="right":
        surf = frames[int(index)]
    
    return animation, surf, index, flip

def hero_duck_animation(frames, flip):
    animation = 2

    if flip:
        surf = pygame.transform.flip(frames[0], True, False)
    else:
        surf = frames[0]

    return animation, surf, flip

def read_score(score):
    with open("high_score.txt") as file:
        high_score = file.readline()
        if score > int(high_score):
            with open("high_score.txt", "w") as file:
                file.write(str(score))

main()