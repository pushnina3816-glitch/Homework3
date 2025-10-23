import pygame
import random


pygame.init()
pygame.mixer.init() 


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
FPS = 60


BALL_RADIUS = 20
spawn_points = [(50, 50), (150, 50), (250, 50), (350, 50)]
spawn_interval = 2000  
last_spawn_time = 0

CATCHER_WIDTH = 80
CATCHER_HEIGHT = 40


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Поймай шарик")
clock = pygame.time.Clock()

try:
    background_img = pygame.image.load('background.png')
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    background_img = None 


try:
    basket_img = pygame.image.load('basket.png')
    basket_img = pygame.transform.scale(basket_img, (CATCHER_WIDTH, CATCHER_HEIGHT))
    catcher_rect = basket_img.get_rect()
except:
    basket_img = None
    catcher_rect = pygame.Rect(0, 0, CATCHER_WIDTH, CATCHER_HEIGHT)


try:
    catch_sound = pygame.mixer.Sound('catch_sound.wav')
except:
    catch_sound = None 


balls = [] 
score = 0
missed = 0
GAME_OVER_LIMIT = 3


font = pygame.font.Font(None, 36) 
game_over_font = pygame.font.Font(None, 50) 


catcher_rect.centerx = SCREEN_WIDTH // 2
catcher_rect.bottom = SCREEN_HEIGHT - 10

running = True
game_over = False


while running:
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        

        if event.type == pygame.MOUSEMOTION and not game_over:
            catcher_rect.centerx = event.pos[0]
            

            if catcher_rect.left < 0:
                catcher_rect.left = 0
            if catcher_rect.right > SCREEN_WIDTH:
                catcher_rect.right = SCREEN_WIDTH

    if not game_over:
        current_time = pygame.time.get_ticks()

        if current_time - last_spawn_time > spawn_interval:
            x, y = random.choice(spawn_points)
            
            dx = random.randint(-2, 2) 
            dy = random.randint(2, 4)  
            balls.append([x, y, dx, dy])
            last_spawn_time = current_time

        for i in range(len(balls) - 1, -1, -1):
            ball = balls[i]
            

            ball[0] += ball[2] 
            ball[1] += ball[3] 

            if ball[0] < BALL_RADIUS or ball[0] > SCREEN_WIDTH - BALL_RADIUS:
                ball[2] = -ball[2] 


            ball_rect = pygame.Rect(ball[0] - BALL_RADIUS, ball[1] - BALL_RADIUS, 
                                    BALL_RADIUS * 2, BALL_RADIUS * 2)

            if catcher_rect.colliderect(ball_rect):
                score += 1
                if catch_sound:
                    catch_sound.play() 
                balls.pop(i) 
            
 
            elif ball[1] > SCREEN_HEIGHT + BALL_RADIUS: 
                missed += 1
                balls.pop(i) 
        

        if missed >= GAME_OVER_LIMIT:
            game_over = True


    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill((255, 255, 255)) 


    for x, y, dx, dy in balls:
        pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), BALL_RADIUS)

    if basket_img:
        screen.blit(basket_img, catcher_rect)
    else:
        pygame.draw.rect(screen, (0, 0, 255), catcher_rect) 


    score_text = font.render(f"Очки: {score}", True, (0, 0, 0))
    missed_text = font.render(f"Пропущено: {missed} / {GAME_OVER_LIMIT}", True, (200, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(missed_text, (10, 40))

    if game_over:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180) 
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        

        go_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        final_score_text = font.render(f"Итоговый счет: {score}", True, (255, 255, 255)) 
        

        go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        
        screen.blit(go_text, go_rect)
        screen.blit(final_score_text, final_score_rect)

    pygame.display.flip()


    clock.tick(FPS)


pygame.quit()