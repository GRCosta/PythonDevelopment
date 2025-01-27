import pygame
import random
import math
from pygame.colordict import THECOLORS

# Initialize pygame
pygame.init()

# Game constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 900
PLAY_AREA_WIDTH = 600
PLAY_AREA_HEIGHT = 750
PLAY_AREA_TOP = WINDOW_HEIGHT - PLAY_AREA_HEIGHT
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Define the circle colors using colordict
selected_colors = [
    'blue4', 'brown1', 'brown3', 'burlywood1', 
    'yellow1', 'violetred4', 'tan1', 
    'red1', 'yellow2', 'yellowgreen', 'limegreen'
]
color_list = [THECOLORS[color] for color in selected_colors]

# Circle types with increasing radius and corresponding colors
CIRCLE_LIST = [(1 + i * 0.5, color_list[i]) for i in range(len(color_list))]
PLAYER_CIRCLE_LIST = CIRCLE_LIST[:5]  # Restrict the player to use only the first 5 circles

# Initialize screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Merge Game")

# Fonts
font = pygame.font.Font(None, 36)

class Circle:
    def __init__(self, x, y, radius, color, falling=False):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.falling = falling

    @staticmethod
    def spawn():
        radius, color = random.choice(PLAYER_CIRCLE_LIST)
        x = (WINDOW_WIDTH - PLAY_AREA_WIDTH) // 2 + PLAY_AREA_WIDTH // 2
        y = PLAY_AREA_TOP - int(radius * 10)
        return Circle(x, y, radius * 10, color)

    def move(self, direction):
        if not self.falling:
            self.x += direction * 5
            left_bound = (WINDOW_WIDTH - PLAY_AREA_WIDTH) // 2 + self.radius
            right_bound = (WINDOW_WIDTH + PLAY_AREA_WIDTH) // 2 - self.radius
            self.x = max(left_bound, min(right_bound, self.x))

    def fall(self):
        if self.falling:
            self.y += 5

    def check_collision(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.hypot(dx, dy)
        return distance < (self.radius + other.radius)

    def merge(self, other):
        global score
        if self.radius == other.radius:
            index = [c[0] for c in CIRCLE_LIST].index(self.radius / 10)
            if index + 1 < len(CIRCLE_LIST):
                new_radius, new_color = CIRCLE_LIST[index + 1]
                score += 10
                return Circle(
                    (self.x + other.x) // 2,
                    (self.y + other.y) // 2,
                    new_radius * 10,
                    new_color
                )
        return None

    def handle_collision(self, circles):
        if self.y + self.radius >= PLAY_AREA_TOP + PLAY_AREA_HEIGHT:
            self.y = PLAY_AREA_TOP + PLAY_AREA_HEIGHT - self.radius
            self.falling = False
            return False

        collided = False
        for other in circles:
            if self.check_collision(other):
                new_circle = self.merge(other)
                if new_circle:
                    circles.remove(other)
                    circles.remove(self)
                    circles.append(new_circle)
                    return False
                else:
                    collided = True
                    self.y = other.y - other.radius - self.radius

        if not collided:
            self.falling = True
        else:
            self.falling = False
        return self.falling

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

# Game variables
circles = []
current_circle = None
score = 0
high_score = 0
running = True
clock = pygame.time.Clock()
move_direction = 0

# Main game loop
while running:
    screen.fill(WHITE)
    pygame.draw.rect(screen, GRAY, ((WINDOW_WIDTH - PLAY_AREA_WIDTH) // 2, PLAY_AREA_TOP, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT))
    score_text = font.render(f"Score: {score}", True, BLACK)
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(score_text, (20, 20))
    screen.blit(high_score_text, (WINDOW_WIDTH - 200, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and current_circle and not current_circle.falling:
                current_circle.falling = True
            elif event.key == pygame.K_LEFT:
                move_direction = -1
            elif event.key == pygame.K_RIGHT:
                move_direction = 1
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                move_direction = 0

    if current_circle:
        current_circle.move(move_direction)
        if current_circle.falling:
            if not current_circle.handle_collision(circles):
                circles.append(current_circle)
                current_circle = None

    if not current_circle:
        current_circle = Circle.spawn()

    for circle in circles:
        circle.draw()

    if current_circle:
        current_circle.fall()
        current_circle.draw()

    if any(circle.y - circle.radius <= PLAY_AREA_TOP for circle in circles):
        high_score = max(high_score, score)
        score = 0
        circles.clear()
        current_circle = None

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
