import pygame
from pygame.locals import *
pygame.init()
screen_width = 1000
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout - Ayaan Hashmi')
font = pygame.font.SysFont('Segoe UI', 30, True)
background = (0, 0, 0)
border_color = (255, 255, 255)
yellow_block = (255, 255, 0)
orange_block = (255, 165, 0)
red_block = (255, 0, 0)
paddle_color = (255, 255, 255)
paddle_outline = (255, 255, 255)
text_color = (255, 255, 255)
cols = 8
rows = 6
clock = pygame.time.Clock()
fps = 80
live_ball = False
game_over = 0
def draw_text(text, font, text_col, x, y):
    text_surface = font.render(text, True, text_col)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x + 200, y)
    screen.blit(text_surface, text_rect)

class Wall:
    def __init__(self):
        self.width = int(screen_width / cols)
        self.height = 50
        self.create_wall()
    
    def create_wall(self):
        self.blocks = []
        for row in range(rows):
            block_row = []
            for col in range(cols):
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                strength = 3 - row // 2
                block_row.append([rect, strength])
            self.blocks.append(block_row)
    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                color_index = min(block[1], len([yellow_block, orange_block, red_block])) - 1
                block_col = [yellow_block, orange_block, red_block][color_index]
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, background, block[0], 2)
class Paddle:
    def __init__(self):
        self.reset()
    def move(self):
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1
    def draw(self):
        pygame.draw.rect(screen, paddle_color, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)
    def reset(self):
        self.height = 20
        self.width = screen_width // cols
        self.x = (screen_width // 2) - (self.width // 2)
        self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 0
class GameBall:
    def __init__(self, x, y):
        self.reset(x, y)
    def move(self):
        collision_thresh = 5
        wall_destroyed = 1
        row_count = 0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                if self.rect.colliderect(item[0]):
                    if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                    if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
                        self.speed_y *= -1
                    if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_x > 0:
                        self.speed_x *= -1
                    if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x < 0:
                        self.speed_x *= -1
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] -= 1
                    else:
                        wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)
                if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_destroyed = 0
                item_count += 1
            row_count += 1
        if wall_destroyed == 1:
            self.game_over = 1
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > screen_height:
            self.game_over = -1
        if self.rect.colliderect(player_paddle):
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
            else:
                self.speed_x *= -1
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over
    def draw(self):
        pygame.draw.circle(screen, paddle_color, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
                           self.ball_rad)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
                           self.ball_rad, 3)
    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = 0
wall = Wall()
wall.create_wall()
player_paddle = Paddle()
ball = GameBall(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
run = True
while run:
    clock.tick(fps)
    screen.fill(background)
    border_thickness = 5
    pygame.draw.rect(screen, border_color, (0, 0, screen_width, border_thickness))  # Top border
    pygame.draw.rect(screen, border_color, (0, 0, border_thickness, screen_height))  # Left border
    pygame.draw.rect(screen, border_color,(0, screen_height - border_thickness, screen_width, border_thickness))  # Bottom border
    pygame.draw.rect(screen, border_color,(screen_width - border_thickness, 0, border_thickness, screen_height))  # Right border

    wall.draw_wall()
    player_paddle.draw()
    ball.draw()
    if live_ball:
        player_paddle.move()
        game_over = ball.move()
        if game_over != 0:
            live_ball = False
    if not live_ball:
        if game_over == 0:
            draw_text('CLICK ANYWHERE TO START', font, text_color, 100, screen_height // 2 + 100)
        elif game_over == 1:
            draw_text('YOU WON!', font, text_color, 240, screen_height // 2 + 50)
            draw_text('CLICK ANYWHERE TO START', font, text_color, 100, screen_height // 2 + 100)
        elif game_over == -1:
            draw_text('YOU WON!', font, text_color, 240, screen_height // 2 + 50)
            draw_text('CLICK ANYWHERE TO START', font, text_color, 100, screen_height // 2 + 100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not live_ball:
            live_ball = True
            ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
            player_paddle.reset()
            wall.create_wall()
    pygame.display.update()
pygame.quit()