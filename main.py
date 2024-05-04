import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((626, 417))
pygame.display.set_caption("Japanese Blood")
icon = pygame.image.load('game/images/icon.png').convert_alpha()
bg = pygame.image.load('game/images/background.png').convert_alpha()
player = pygame.image.load('game/images/111.png').convert_alpha()
ninja = pygame.image.load('game/images/enemy1.png').convert_alpha()


play_button_img = pygame.image.load("game/images/play.png")
play_button_rect = play_button_img.get_rect()
play_button_rect.center = (313, 200)

background_img = pygame.image.load("game/images/bg_start.jpg")
background_rect = background_img.get_rect()


quit_button_img = pygame.image.load("game/images/exit.png")
quit_button_rect = quit_button_img.get_rect()
quit_button_rect.center = (313, 300)

welcome_font = pygame.font.Font(None, 36)
welcome_text = welcome_font.render("Welcome to the Game!", True, (0, 0, 0))

win_font = pygame.font.Font(None, 36)
win_text = welcome_font.render("You win! You're incredible", True, (0, 0, 0))

bullets_left = 5
bullet = pygame.image.load('game/images/bullet.png').convert_alpha()
bullets = []
kills = 0

hp = pygame.image.load('game/images/hp2.png').convert_alpha()
heart_rect = hp.get_rect()

hp_list = [(0, 0), (50, 0), (100, 0)] 

ninja_list = []


walk_right = [
    pygame.image.load('game/images/player_right/1.1.png').convert_alpha(),
    pygame.image.load('game/images/player_right/1.2.png').convert_alpha(),
    pygame.image.load('game/images/player_right/1.3.png').convert_alpha(),
    pygame.image.load('game/images/player_right/1.4.png').convert_alpha(),
    pygame.image.load('game/images/player_right/1.5.png').convert_alpha(),
    pygame.image.load('game/images/player_right/1.6.png').convert_alpha(),
]

walk_left = [
    pygame.image.load('game/images/player_left/2.1.png').convert_alpha(),
    pygame.image.load('game/images/player_left/2.2.png').convert_alpha(),
    pygame.image.load('game/images/player_left/2.3.png').convert_alpha(),
    pygame.image.load('game/images/player_left/2.4.png').convert_alpha(),
    pygame.image.load('game/images/player_left/2.5.png').convert_alpha(),
    pygame.image.load('game/images/player_left/2.6.png').convert_alpha(),
]


pygame.display.set_icon(icon)

player_anim_count = 0

bg_x = 0

bg_sound = pygame.mixer.Sound('game/sounds/bg_sound.mp3')
bg_sound.play()

player_speed = 5
player_x = 150
player_y = 300

is_jump = False
jump_count = 8

ninja_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ninja_timer, 2500)

label = pygame.font.Font('game/mon.ttf', 40)
lose_label = label.render("Вы проиграли", False, (193, 196, 199) )
restart_label = label.render("Играть заново", False, (115, 132, 148) )
restart_label_rect = restart_label.get_rect(topleft=(180, 200))


gameplay = True
show_welcome_screen = True
win_screen = False

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            
            if play_button_rect.collidepoint(event.pos):
                show_welcome_screen = False
            
            if quit_button_rect.collidepoint(event.pos):
                running = False

    if show_welcome_screen:
        screen.blit(background_img, background_rect)
        screen.blit(play_button_img, play_button_rect)
        screen.blit(quit_button_img, quit_button_rect)
        screen.blit(welcome_text, (200, 100))
        pygame.display.flip()

    else:
        while not show_welcome_screen:

            screen.blit(bg, (bg_x, 0))
            screen.blit(bg, (bg_x + 626, 0))
            for heart_pos in hp_list:
                heart_rect.topleft = heart_pos
                screen.blit(hp, heart_rect)

            if gameplay:
                    
                

                player_rect = walk_right[0].get_rect(topleft=(player_x, player_y))   
                
                if ninja_list:
                    for (i, el) in enumerate(ninja_list):
                        screen.blit(ninja, el)
                        el.x -= 10

                        if el.x < -10:
                            ninja_list.pop(i)

                        for (i, el) in enumerate(hp_list):
                            if hp_list:
                                for (index, ninja_el) in  enumerate(ninja_list):
                                    if player_rect.colliderect(ninja_el):
                                        ninja_list.pop(index)
                                        hp_list.pop(i)
                                        if not hp_list:
                                            gameplay = False
                        
                    

                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    screen.blit(walk_left[player_anim_count], (player_x, player_y))
                else:
                    screen.blit(walk_right[player_anim_count], (player_x, player_y))

                if keys[pygame.K_LEFT] and player_x > 50:
                    player_x -= player_speed
                elif keys[pygame.K_RIGHT] and player_x < 500:
                    player_x += player_speed

                if not is_jump:
                    if keys[pygame.K_SPACE]:
                        is_jump = True
                else:
                    if jump_count >= -8:
                        if jump_count > 0:
                            player_y -= (jump_count ** 2) / 2
                        else:
                            player_y += (jump_count ** 2) / 2
                        jump_count -= 1
                    else:
                        is_jump = False
                        jump_count = 8

                if player_anim_count == 5:
                    player_anim_count = 0
                else:
                    player_anim_count += 1

                bg_x -= 2
                if bg_x == -626:
                    bg_x = 0


            
                if bullets:
                    for (i, el) in enumerate(bullets):
                        screen.blit(bullet, (el.x, el.y))
                        el.x += 4

                        if el.x > 640:
                            bullets.pop()

                        if ninja_list:
                            for (index, ninja_el) in  enumerate(ninja_list):
                                if el.colliderect(ninja_el):
                                    ninja_list.pop(index)
                                    bullets.pop(i)
                                    kills += 1
                                    if kills == 4:
                                        win_screen = True
                                        while win_screen == True:
                                              for event in pygame.event.get():
                                                if event.type == pygame.QUIT:
                                                    running = False
                                                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                                    
                                                    if play_button_rect.collidepoint(event.pos):
                                                        show_welcome_screen = False
                                                    
                                                    if quit_button_rect.collidepoint(event.pos):
                                                        running = False
                                                if win_screen:
                                                    screen.blit(background_img, background_rect)
                                                    screen.blit(play_button_img, play_button_rect)
                                                    screen.blit(quit_button_img, quit_button_rect)
                                                    screen.blit(win_text, (200, 100))
                                                    pygame.display.flip()

            

            
                                    

            else:
            
                if not hp_list:
                    screen.fill((224, 255, 255))
                    screen.blit(lose_label, (180, 100))
                    screen.blit(restart_label, restart_label_rect)

                mouse = pygame.mouse.get_pos()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    gameplay = True
                    player_x = 150
                    ninja_list.clear()
                    bullets.clear()
                    hp_list = [(0, 0), (50, 0), (100, 0)] 
                    bullets_left = 5

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if event.type == ninja_timer:
                    ninja_list.append(ninja.get_rect(topleft=(700, 330)))
                if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_d and bullets_left > 0:
                    bullets.append(bullet.get_rect(topleft=(player_x + 50, player_y + 40)))
                    bullets_left -= 1


            
            clock.tick(30)
        