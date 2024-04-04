import pygame
import sys

pygame.init() #imports pygame modules and initializes them

#sets up my screen 
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Soccer Game lol")

#defines the colors needed for the game
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#setting the speed, size and position of my players (2 squares lol)
PLAYER_SIZE = 50
player1_pos = [WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT // 4 - PLAYER_SIZE // 2]
player2_pos = [WIDTH // 2 - PLAYER_SIZE // 2, 3 * HEIGHT // 4 - PLAYER_SIZE // 2]
player_speed = 8

#ball(one square)
BALL_SIZE = 20
ball_pos = [WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2]
ball_speed = [0, 0]  # Ball initially not moving

#goal(bigger white rectangles)
GOAL_WIDTH = WIDTH // 4
GOAL_HEIGHT = 50
top_goal = pygame.Rect((WIDTH - GOAL_WIDTH) // 2, 0, GOAL_WIDTH, GOAL_HEIGHT)
bottom_goal = pygame.Rect((WIDTH - GOAL_WIDTH) // 2, HEIGHT - GOAL_HEIGHT, GOAL_WIDTH, GOAL_HEIGHT)

#scores
score_top = 0
score_bottom = 0

#fonts
font = pygame.font.Font(None, 36)



def main():
    #variables that I'm going to use in this function 
    global player1_pos, player2_pos, ball_pos, ball_speed, score_top, score_bottom
    
    clock = pygame.time.Clock()
    
    #sets up the timer
    timer_font = pygame.font.Font(None, 36)
    start_time = pygame.time.get_ticks()
    timer_value = 5
    timer_text = timer_font.render(f"Time left: {timer_value}", True, WHITE)

    while True:
        screen.fill(GREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #square 1 movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player1_pos[1] -= player_speed
        if keys[pygame.K_s]:
            player1_pos[1] += player_speed
        if keys[pygame.K_a]:
            player1_pos[0] -= player_speed
        if keys[pygame.K_d]:
            player1_pos[0] += player_speed

        # square 2 movement
        if keys[pygame.K_UP]:
            player2_pos[1] -= player_speed
        if keys[pygame.K_DOWN]:
            player2_pos[1] += player_speed
        if keys[pygame.K_LEFT]:
            player2_pos[0] -= player_speed
        if keys[pygame.K_RIGHT]:
            player2_pos[0] += player_speed

        #this section makes sure the players don't go off the screen
        player1_pos[0] = max(0, min(WIDTH - PLAYER_SIZE, player1_pos[0]))
        player1_pos[1] = max(0, min(HEIGHT - PLAYER_SIZE, player1_pos[1]))
        player2_pos[0] = max(0, min(WIDTH - PLAYER_SIZE, player2_pos[0]))
        player2_pos[1] = max(0, min(HEIGHT - PLAYER_SIZE, player2_pos[1]))

        # Ball movement when player 1 hits it
        if pygame.Rect(player1_pos[0], player1_pos[1], PLAYER_SIZE, PLAYER_SIZE).colliderect(
                pygame.Rect(ball_pos[0], ball_pos[1], BALL_SIZE, BALL_SIZE)):
            # If player 1 touches the ball, kick it away from player 1
            ball_speed = [player_speed * ((ball_pos[0] + BALL_SIZE // 2) - (player1_pos[0] + PLAYER_SIZE // 2)) / (PLAYER_SIZE // 2),
                          player_speed * ((ball_pos[1] + BALL_SIZE // 2) - (player1_pos[1] + PLAYER_SIZE // 2)) / (PLAYER_SIZE // 2)]
        
        # Ball movement when player 2 hits it
        if pygame.Rect(player2_pos[0], player2_pos[1], PLAYER_SIZE, PLAYER_SIZE).colliderect(
                pygame.Rect(ball_pos[0], ball_pos[1], BALL_SIZE, BALL_SIZE)):
            #

            # If player 2 touches the ball, kick it away from player 2
            ball_speed = [player_speed * ((ball_pos[0] + BALL_SIZE // 2) - (player2_pos[0] + PLAYER_SIZE // 2)) / (PLAYER_SIZE // 2),
                          player_speed * ((ball_pos[1] + BALL_SIZE // 2) - (player2_pos[1] + PLAYER_SIZE // 2)) / (PLAYER_SIZE // 2)]
        
        # Ball movement
        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]

        # makes sure the ball doesn't go off the screen
        if ball_pos[0] <= 0 or ball_pos[0] >= WIDTH - BALL_SIZE:
            ball_speed[0] *= -1
        if ball_pos[1] <= 0 or ball_pos[1] >= HEIGHT - BALL_SIZE:
            ball_speed[1] *= -1

        # because I coulnd't out how to make the ball go into the net, I just made it so that if the ball touches the goal(white rectangle), its a goal :)
        if top_goal.colliderect(pygame.Rect(ball_pos[0], ball_pos[1], BALL_SIZE, BALL_SIZE)):
            if ball_pos[1] <= GOAL_HEIGHT: 
                ball_pos = [WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2]  
                ball_speed = [0, 0]  
                score_bottom += 1
                print("Goal for Blue!")
        elif bottom_goal.colliderect(pygame.Rect(ball_pos[0], ball_pos[1], BALL_SIZE, BALL_SIZE)):
            if ball_pos[1] >= HEIGHT - GOAL_HEIGHT: 
                ball_pos = [WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2] 
                ball_speed = [0, 0] 
                score_top += 1
                print("Goal for Red!")
        
        # This is where I draw everything on the screen
        pygame.draw.line(screen, WHITE, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2) # half way line
        pygame.draw.rect(screen, WHITE, top_goal)  #  top goal
        pygame.draw.rect(screen, WHITE, bottom_goal)  #  bottom goal
        pygame.draw.rect(screen, BLACK, (ball_pos[0], ball_pos[1], BALL_SIZE, BALL_SIZE))  #  ball
        pygame.draw.rect(screen, BLUE, (player1_pos[0], player1_pos[1], PLAYER_SIZE, PLAYER_SIZE))  #  player 1
        pygame.draw.rect(screen, RED, (player2_pos[0], player2_pos[1], PLAYER_SIZE, PLAYER_SIZE))  #  player 2

        #  scores
        score_text_top = font.render(f"Blue Team: {score_top}", True, WHITE)
        score_text_bottom = font.render(f"Red Team: {score_bottom}", True, WHITE)
        screen.blit(score_text_top, (20, 20))
        screen.blit(score_text_bottom, (20, HEIGHT - 40))
        
        # Timer 
        if timer_value > 0:
            if pygame.time.get_ticks() % 1000 == 0:  # updates per second
                timer_value -= 1
                timer_text = timer_font.render(f"Time left: {timer_value}", True, WHITE)
        else:
            winner_text = None
            if score_top > score_bottom:
                winner_text = "Blue team wins!"
            elif score_top < score_bottom:
                winner_text = "Red team wins!"
            else:
                winner_text = "It's a draw!"
                
            winner_font = pygame.font.Font(None, 48)
            winner_surface = winner_font.render(winner_text, True, WHITE)
            winner_rect = winner_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(winner_surface, winner_rect)
        
        #  timer
        screen.blit(timer_text, (WIDTH - 200, 20))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
