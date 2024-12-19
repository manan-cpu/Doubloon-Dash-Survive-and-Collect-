import pygame
import random
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retry or Exit Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (255, 0, 0)

FPS = 60
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("comicsans", 40)

PLAYER_SIZE = 50
player_velocity = 5

ENEMY_SIZE = 50
enemy_speed = 3
enemies = [{"x": random.randint(0, WIDTH - ENEMY_SIZE), "y": 0} for _ in range(5)]

DOUBLOON_SIZE = 30
doubloon_x = random.randint(0, WIDTH - DOUBLOON_SIZE)
doubloon_y = random.randint(0, HEIGHT // 2)

score = 0
level = 1


def main():
    global player_x, player_y, score, level, enemy_speed, doubloon_x, doubloon_y

    player_x = WIDTH // 2
    player_y = HEIGHT - 70
    score = 0
    level = 1
    enemy_speed = 3

    running = True
    while running:
        WINDOW.fill((0, 128, 128))
        clock.tick(FPS)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Player Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player_x - player_velocity > 0:
            player_x -= player_velocity
        if keys[pygame.K_d] and player_x + player_velocity < WIDTH - PLAYER_SIZE:
            player_x += player_velocity
        if keys[pygame.K_w] and player_y - player_velocity > 0:
            player_y -= player_velocity
        if keys[pygame.K_s] and player_y + player_velocity < HEIGHT - PLAYER_SIZE:
            player_y += player_velocity

        # Draw Player
        pygame.draw.rect(WINDOW, WHITE, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))

        # Draw Doubloon
        pygame.draw.circle(WINDOW, GOLD, (doubloon_x, doubloon_y), DOUBLOON_SIZE)

        # Doubloon Collection Logic
        if (player_x < doubloon_x < player_x + PLAYER_SIZE) and (
            player_y < doubloon_y < player_y + PLAYER_SIZE
        ):
            score += 1
            doubloon_x = random.randint(0, WIDTH - DOUBLOON_SIZE)
            doubloon_y = random.randint(0, HEIGHT // 2)

        # Draw Enemies
        for enemy in enemies:
            pygame.draw.rect(WINDOW, RED, (enemy["x"], enemy["y"], ENEMY_SIZE, ENEMY_SIZE))
            enemy["y"] += enemy_speed
            if enemy["y"] > HEIGHT:
                enemy["y"] = 0
                enemy["x"] = random.randint(0, WIDTH - ENEMY_SIZE)

            # Collision Detection
            if (
                player_x < enemy["x"] + ENEMY_SIZE
                and player_x + PLAYER_SIZE > enemy["x"]
                and player_y < enemy["y"] + ENEMY_SIZE
                and player_y + PLAYER_SIZE > enemy["y"]
            ):
                display_message("Game Over!", score)
                return

        # Level Up Logic
        if score > 0 and score % 5 == 0:
            level = score // 5 + 1
            enemy_speed = 3 + level  # Increase enemy speed gradually

        # Display Score and Level
        score_text = FONT.render(f"Score: {score}  |  Level: {level}", True, BLACK)
        WINDOW.blit(score_text, (10, 10))

        pygame.display.update()


# Game Over Display with Retry or Exit
def display_message(message, final_score):
    WINDOW.fill(BLACK)
    game_over_text = FONT.render(message, True, RED)
    score_text = FONT.render(f"Your Score: {final_score}", True, GOLD)
    retry_text = FONT.render("Press R to Retry or Q to Quit", True, WHITE)
    WINDOW.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
    WINDOW.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    WINDOW.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 60))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Retry
                    main()  # Restart the game
                    return
                if event.key == pygame.K_q:  # Quit
                    sys.exit()


if __name__ == "__main__":
    main()
