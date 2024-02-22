import pygame
import random
import math
import time

pygame.init()

#Load assets
player_sprite = pygame.image.load("player.png")
player_sprite = pygame.transform.smoothscale(player_sprite, (80,80))
zombie_sprite = pygame.image.load("zombie_sprite.png")
zombie_sprite = pygame.transform.smoothscale(zombie_sprite, (80,80))
brute_sprite = pygame.image.load("Brute.png")
brute_sprite = pygame.transform.smoothscale(brute_sprite, (100,100))
pygame.mixer.music.load("background-music.mp3")
pygame.mixer.music.play(-1)
death_sound = pygame.mixer.Sound("death-sound.mp3")
gun_sound = pygame.mixer.Sound("gun-sound.mp3")
hurt_sound = pygame.mixer.Sound("hurt-sound.mp3")
shotgun_sound = pygame.mixer.Sound("shotgun-sound.mp3")

#Initialize game variables
screen = pygame.display.set_mode((1280, 720))
running = True
player = {
    "pos": pygame.math.Vector2((640,360)),
    "rad": 27,
    "color": "blue",
    "speed": 0.8,
    "vel": pygame.math.Vector2((0,0)),
    "sprite": player_sprite
}
bullets = []
zombies = []
brutes = []
lives = 5
gun = "shotgun"
kill_counter = 0
default_font = pygame.font.Font(pygame.font.get_default_font(), 70)
game_over_text = default_font.render("GAME OVER", True, "black")
ammo_font = pygame.font.Font(pygame.font.get_default_font(), 30)
button_rect = pygame.Rect(screen.get_width() / 2 - 200, screen.get_height() / 2 + 180, 400, 120)
clock = pygame.time.Clock()
start_time = time.time()
dt = 0

#Set zombie spawn timer
SPAWNZOMBIE = 2100
pygame.time.set_timer(SPAWNZOMBIE, 1000)
 
SPAWNBRUTE = 2100
pygame.time.set_timer(SPAWNBRUTE, 1000)

#Define utility functions

#deletes unnecesary bullet
def clean_up_bullets(array):
    i = 0
    while i < len(array):
        ball = array[i]
        pos = ball["pos"]
        if pos.x > 1280 or pos.x < 0 or pos.y > 720 or pos.y < 0:
            array.pop(i)
        else:
            i += 1

#calculates physics movements
def update_pos(ball):
    if ball["vel"].length() != 0:
        ball["vel"].scale_to_length(ball["speed"] * dt)
        ball["pos"] += ball["vel"]

#keeps the player on the screen
def limit_pos(ball):
    if ball["pos"].x > 1280:
        ball["pos"].x = 1280
    if ball["pos"].x < 0:
        ball["pos"].x = 0
    if ball["pos"].y > 720:
        ball["pos"].y = 720
    if ball["pos"].y < 0:
        ball["pos"].y = 0

#draws a circle to the screen
def draw_ball(ball):
    pygame.draw.circle(screen, ball["color"], ball["pos"], ball["rad"])

#draws a sprite to the screen
def draw_sprite(ball):
    sprite = ball["sprite"]
    pos = ball["pos"]
    x = pos.x - (sprite.get_width() / 2)
    y = pos.y - (sprite.get_width() / 2)
    screen.blit(sprite, (x,y))

#checks collision between two balls
def check_collision(ball1, ball2):
    diff = ball1["pos"] - ball2["pos"]
    return diff.length() < ball1["rad"] + ball2["rad"]

ammo = 10
ammo_text = ammo_font.render("Ammo " + str(ammo) + " left", True, "black")

#Main game Loop
while running:
    #Check events
    for event in pygame.event.get():
        #Quit game event
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if event.key == pygame.K_r:
                    ammo = 10
                    ammo_text = ammo_font.render("Ammo " + str(ammo) + " left", True, "black")
        #Click mouse event
        if event.type == pygame.MOUSEBUTTONUP:
            if lives > 0 and ammo > 0:
                ammo = ammo -1
                ammo_text = ammo_font.render("Ammo " + str(ammo) + " left", True, "black")
                #Spawn a new bullet
                if gun == "pistol":
                    new_bullet = {
                        "pos": player["pos"].copy(),
                        "rad": 8,
                        "color": "red",
                        "speed": 2,
                        "vel": pygame.mouse.get_pos() - player["pos"]
                    }
                    bullets.append(new_bullet)
                    gun_sound.play()
                elif gun == "shotgun":
                    vel = pygame.mouse.get_pos() - player["pos"]
                    new_bullet = {
                        "pos": player["pos"].copy(),
                        "rad": 8,
                        "color": "red",
                        "speed": 2,
                        "vel": vel
                    }
                    new_bullet2 = {
                        "pos": player["pos"].copy(),
                        "rad": 8,
                        "color": "red",
                        "speed": 2,
                        "vel": vel.rotate(10)
                    }
                    bullets.append(new_bullet)
                    bullets.append(new_bullet2)
                    shotgun_sound.play()
               
                elif gun == "lasergun":
                    vel = pygame.mouse.get_pos() - player["pos"]
                    new_bullet3 = {
                        "pos": player["pos"].copy(),
                        "rad": 8,
                        "color": "red",
                        "speed": 0.5,
                        "vel" :vel
                    }
                    bullets.append(new_bullet3)
             
            else:
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.music.play(-1)
                    lives = 5
                    kill_counter = 0
                    bullets = []
                    zombies = []
                    player["pos"] = pygame.math.Vector2((640,360))
                    start_time = time.time()
                    pygame.time.set_timer(SPAWNZOMBIE, 1000)
        #Spawn zombie event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                gun = "pistol"
            elif event.key == pygame.K_2:
                gun = "shotgun"
            elif event.key == pygame.K_3:
                gun = "lasergun"   
        if event.type == SPAWNZOMBIE and lives > 0:
           
            angle = random.uniform(0,360)
            middle = pygame.math.Vector2((640,360))
            offset = pygame.math.Vector2((750,0))

            curr_time = time.time()
            millis = (curr_time - start_time) * 1000
            speed = pow(millis, 0.3) / 100.0
           
            new_zombie = {
                "pos": middle + offset.rotate(angle),
                "rad": 30,
                "color": "darkgreen",
                "speed": speed,
                "vel": pygame.math.Vector2((0,0)),
                "sprite": zombie_sprite
            }
            zombies.append(new_zombie)
            spawn_interval = math.exp(millis / 80000)*1000
            pygame.time.set_timer(SPAWNZOMBIE, 1000)
               #Spawn brute event

        if event.type == SPAWNBRUTE and lives > 0:
            angle = random.uniform(0,360)
            middle = pygame.math.Vector2((640,360))
            offset = pygame.math.Vector2((750,0))

            curr_time = time.time()
            millis = (curr_time - start_time) * 1000
            speed = pow(millis, .2) / 100.0

            new_brute = {
                "pos": middle + offset.rotate(angle),
                "rad": 60,
                "color": "darkgreen",
                "speed": speed,
                "vel": pygame.math.Vector2((0,0)),
                "sprite": brute_sprite
            }

            brutes.append(new_brute)
            spawn_interval = math.exp(millis / 80000)*1000
            pygame.time.set_timer(SPAWNBRUTE, 1000)

    #when the player is alive
    if lives > 0:
        screen.fill("slategrey")

        screen.blit(ammo_text, (30,40))

        #spawn bullet
        if pygame.mouse.get_pressed() and gun == "lasergun":
            vel = pygame.mouse.get_pos() - player["pos"]
            new_bullet3 = {
                        "pos": player["pos"].copy(),
                        "rad": 8,
                        "color": "red",
                        "speed": 0.5,
                        "vel" :vel
                    }
            bullets.append(new_bullet3)
           

        #checking WASD movement
        keys = pygame.key.get_pressed()
        player["vel"] = pygame.math.Vector2((0,0))
        if keys[pygame.K_w]:
            player["vel"].y -= 1
        if keys[pygame.K_s]:
            player["vel"].y += 1
        if keys[pygame.K_a]:
            player["vel"].x -= 1
        if keys[pygame.K_d]:
            player["vel"].x += 1

        #removing unncessary bullets
        clean_up_bullets(bullets)

        #drawing red rectangles to represent lives
        for i in range(lives):
            rect = pygame.Rect(40*i + 10, 10, 30, 30)
            pygame.draw.rect(screen, "red", rect)

        #update each zombie position and check if it's hitting the player
        for zombie in zombies:
            zombie["vel"] = player["pos"] - zombie["pos"]
            update_pos(zombie)
            #draw_ball(zombie)
            direction_to_face = player["pos"] - zombie["pos"]
            r,theta = direction_to_face.as_polar()
            zombie["sprite"] = pygame.transform.rotate(zombie_sprite, -theta)
            draw_sprite(zombie)
            if check_collision(zombie, player):
                lives -= 1
                zombies.remove(zombie)
                if lives == 0:
                    death_sound.play()
                else:
                    hurt_sound.play()
        
        for brute in brutes:
            brute["vel"] = player["pos"] - brute["pos"]
            update_pos(brute)
            #draw_ball(brute)
            direction_to_face = player["pos"] - brute["pos"]
            r,theta = direction_to_face.as_polar()
            brute["sprite"] = pygame.transform.rotate(brute_sprite, -theta)
            draw_sprite(brute)
            if check_collision(brute, player):
                lives -= 2
                brutes.remove(brute)
                if lives == 0:
                    death_sound.play()
                else:
                    hurt_sound.play()

        #update each bullet position and check if it's hitting a zombie
        for bullet in bullets:
            draw_ball(bullet)
            update_pos(bullet)
            for zombie in zombies:
                if check_collision(bullet, zombie):
                    zombies.remove(zombie)
                    bullets.remove(bullet)
                    kill_counter += 1
                    break
            for brute in brutes:
                if check_collision(bullet, brute):
                    brutes.remove(brute)
                    bullets.remove(bullet)
                    kill_counter += 1
                    break

        #update the player position and make them face the mouse
        update_pos(player)
        limit_pos(player)
        direction_to_face = pygame.mouse.get_pos() - player["pos"]
        r,theta = direction_to_face.as_polar()
        player["sprite"] = pygame.transform.rotate(player_sprite, -theta)
        draw_sprite(player)

        pygame.display.flip()

        dt = clock.tick(60)
    else:
        #If the player is dead, we draw the death screen instead
        pygame.mixer.music.stop()
        screen.fill("red")

        x = (screen.get_width() / 2) - (game_over_text.get_width() / 2)
        y = (screen.get_height() / 2) - (game_over_text.get_height() / 2)
        screen.blit(game_over_text, (x,y))

        kill_counter_text = default_font.render("YOU KILLED " + str(kill_counter) + " ZOMBIES!", True, "black")

        x = (screen.get_width() / 2) - (kill_counter_text.get_width() / 2)
        y = (screen.get_height() / 2 + 100) - (kill_counter_text.get_height() / 2)
        screen.blit(kill_counter_text, (x,y))

       
        pygame.draw.rect(screen, "slategrey", button_rect)

        restart_text = default_font.render("RESTART", True, "Black")
        x = (screen.get_width() / 2) - (restart_text.get_width() / 2)
        y = screen.get_height() / 2 + 210
        screen.blit(restart_text, (x,y))

        pygame.display.flip()
 
pygame.quit()