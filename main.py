import pygame
import time
import random

pygame.init()
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
dis_width = 1000
dis_height = 800
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Змейка Бог Пожиратель Крипов')
clock = pygame.time.Clock()
snake_block = 50
snake_speed = 8
font_style = pygame.font.SysFont("bahnschrift", 28)
score_font = pygame.font.SysFont("comicsansms", 40)
 
sprite_size = int(snake_block * 1.25)  
travka_img = pygame.image.load('travka.png').convert()
travka_img = pygame.transform.scale(travka_img, (dis_width, dis_height))

wall_img = pygame.image.load('stenka_boga.png').convert()
wall_tile = pygame.transform.scale(wall_img, (snake_block, snake_block))

apple_img = pygame.image.load('apple.png').convert_alpha()
apple_img = pygame.transform.scale(apple_img, (int(snake_block * 1.1), int(snake_block * 1.1)))

head_img_raw = pygame.image.load('golova.png').convert_alpha()
head_img = pygame.transform.scale(head_img_raw, (sprite_size, sprite_size))

first_img_raw = pygame.image.load('first.png').convert_alpha()
first_img = pygame.transform.scale(first_img_raw, (sprite_size, sprite_size))

body_img_raw = pygame.image.load('double.png').convert_alpha()
body_img = pygame.transform.scale(body_img_raw, (sprite_size, sprite_size))

laser_img = pygame.image.load('laser.png').convert_alpha()

def draw_environment():
    dis.blit(travka_img, (0, 0))
    
    for x in range(0, dis_width, snake_block):
        dis.blit(wall_tile, (x, 0))
        dis.blit(wall_tile, (x, dis_height - snake_block))
    for y in range(snake_block, dis_height - snake_block, snake_block):
        dis.blit(wall_tile, (0, y))
        dis.blit(wall_tile, (dis_width - snake_block, y))

def Your_score(score):
    value = score_font.render("Ваш счёт: " + str(score), True, yellow)
    dis.blit(value, [snake_block + 15, 10])

def get_rotation(dx, dy):
    if dx > 0: return 270
    if dx < 0: return 90
    if dy > 0: return 180
    return 0

def our_snake(snake_block, snake_list, x1_change, y1_change):
    n = len(snake_list)
    if n == 0:
        return

    for i in range(n - 2):
        curr_x, curr_y = snake_list[i][0], snake_list[i][1]
        next_x, next_y = snake_list[i+1][0], snake_list[i+1][1]
        
        dx = next_x - curr_x
        dy = next_y - curr_y
        if dx == 0 and dy == 0:
            dx, dy = x1_change, y1_change
            
        rot_angle = get_rotation(dx, dy)
        rotated_body = pygame.transform.rotate(body_img, rot_angle)
        body_rect = rotated_body.get_rect(center=(curr_x + snake_block // 2, curr_y + snake_block // 2))
        dis.blit(rotated_body, body_rect.topleft)

    if n >= 2:
        i = n - 2
        curr_x, curr_y = snake_list[i][0], snake_list[i][1]
        next_x, next_y = snake_list[i+1][0], snake_list[i+1][1]
        
        dx = next_x - curr_x
        dy = next_y - curr_y
        if dx == 0 and dy == 0:
            dx, dy = x1_change, y1_change
            
        rot_angle = get_rotation(dx, dy)
        rotated_first = pygame.transform.rotate(first_img, rot_angle)
        first_rect = rotated_first.get_rect(center=(curr_x + snake_block // 2, curr_y + snake_block // 2))
        dis.blit(rotated_first, first_rect.topleft)

    head_x, head_y = snake_list[-1][0], snake_list[-1][1]
    head_rot = get_rotation(x1_change, y1_change)
    rotated_head = pygame.transform.rotate(head_img, head_rot)
    head_rect = rotated_head.get_rect(center=(head_x + snake_block // 2, head_y + snake_block // 2))
    dis.blit(rotated_head, head_rect.topleft)

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def spawn_food():
    foodx = round(random.randrange(snake_block, dis_width - 2 * snake_block) / float(snake_block)) * snake_block
    foody = round(random.randrange(snake_block, dis_height - 2 * snake_block) / float(snake_block)) * snake_block
    return [foodx, foody]

def gameLoop():
    game_over = False
    game_close = False
    x1 = round((dis_width / 2) / float(snake_block)) * snake_block
    y1 = round((dis_height / 2) / float(snake_block)) * snake_block
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1
    current_score = 0
    foods_count = 2  
    max_foods = 15  
    foods = [spawn_food() for _ in range(foods_count)]
    laser_active = 0
    laser_dir = None
    last_laser_time = 0  
    laser_cooldown = 5.0 
    beam_width = snake_block 
    while not game_over:
        while game_close == True:
            draw_environment()
            message("Вы проиграли! Нажмите Q для выхода или C для повторной игры", red)
            Your_score(current_score)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    current_time = time.time()
                    if current_time - last_laser_time >= laser_cooldown:
                        last_laser_time = current_time
                        laser_active = 5  # Лазер виден 5 кадров
                        dx, dy = x1_change, y1_change
                        if dx == 0 and dy == 0:
                            dy = -snake_block  # По умолчанию вверх
                        laser_dir = (dx, dy)

                elif event.key == pygame.K_LEFT and x1_change != snake_block:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -snake_block:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != snake_block:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -snake_block:
                    y1_change = snake_block
                    x1_change = 0
        if x1 < snake_block or x1 >= dis_width - snake_block or y1 < snake_block or y1 >= dis_height - snake_block:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        
        draw_environment()
        
        for food in foods:
            apple_rect = apple_img.get_rect(center=(food[0] + snake_block // 2, food[1] + snake_block // 2))
            dis.blit(apple_img, apple_rect.topleft)
            
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
                
        our_snake(snake_block, snake_List, x1_change, y1_change)
        
        if laser_active > 0 and laser_dir:
            dx, dy = laser_dir
            hit_foods = []
            if dx > 0:  # Вправо
                start_x, end_x, y_pos = x1 + snake_block, dis_width - snake_block, y1
                for food in foods:
                    if abs(food[1] - y1) <= beam_width and food[0] >= x1:
                        hit_foods.append(food)
                laser_w = int(max(1, end_x - start_x))
                scaled_laser = pygame.transform.scale(laser_img, (laser_w, beam_width))
                dis.blit(scaled_laser, (start_x, y_pos))
            elif dx < 0:  # Влево
                start_x, end_x, y_pos = snake_block, x1, y1
                for food in foods:
                    if abs(food[1] - y1) <= beam_width and food[0] <= x1:
                        hit_foods.append(food)
                laser_w = int(max(1, end_x - start_x))
                scaled_laser = pygame.transform.scale(laser_img, (laser_w, beam_width))
                dis.blit(scaled_laser, (start_x, y_pos))
            elif dy > 0:  # Вниз
                x_pos, start_y, end_y = x1, y1 + snake_block, dis_height - snake_block
                for food in foods:
                    if abs(food[0] - x1) <= beam_width and food[1] >= y1:
                        hit_foods.append(food)
                laser_h = int(max(1, end_y - start_y))
                rotated_laser = pygame.transform.rotate(laser_img, 90)
                scaled_laser = pygame.transform.scale(rotated_laser, (beam_width, laser_h))
                dis.blit(scaled_laser, (x_pos, start_y))
            elif dy < 0:  # Вверх
                x_pos, start_y, end_y = x1, snake_block, y1
                for food in foods:
                    if abs(food[0] - x1) <= beam_width and food[1] <= y1:
                        hit_foods.append(food)
                laser_h = int(max(1, end_y - start_y))
                rotated_laser = pygame.transform.rotate(laser_img, 90)
                scaled_laser = pygame.transform.scale(rotated_laser, (beam_width, laser_h))
                dis.blit(scaled_laser, (x_pos, start_y))
            
            for food in hit_foods:
                if food in foods:
                    foods.remove(food)
                    foods.append(spawn_food())
                    current_score += 2  # x2 очки за уничтожение лазером!
                    Length_of_snake += 1
                    if current_score % 2 == 0 and len(foods) < max_foods:
                        foods.append(spawn_food())
            
            laser_active -= 1
        
        cd_left = max(0.0, laser_cooldown - (time.time() - last_laser_time))
        if cd_left > 0:
            laser_txt = font_style.render(f"Лазер: {cd_left:.1f}с", True, yellow)
        else:
            laser_txt = font_style.render("Лазер [Z]: ГОТОВ", True, green)
        dis.blit(laser_txt, [dis_width - snake_block - 240, 10])

        Your_score(current_score)
        pygame.display.update()
        for food in foods:
            if abs(x1 - food[0]) < snake_block and abs(y1 - food[1]) < snake_block:
                foods.remove(food)
                foods.append(spawn_food())
                current_score += 1  # Обычное съедание дает +1 очко
                Length_of_snake += 1
                if current_score % 2 == 0 and len(foods) < max_foods:
                    foods.append(spawn_food())
                break
        clock.tick(snake_speed)
    pygame.quit()
    quit()
gameLoop()