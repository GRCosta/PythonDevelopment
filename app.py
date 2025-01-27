# Importing libraries
import pygame
import random
import math

# Initializing Pygame
pygame.init()

# Setup Game window
PLAYAREAWIDTH = 300
PLAYAREAHEIGHT = 500

GAMEWIDTH = 600
GAMEHEIGHT = 900

gameWindow = pygame.display.set_mode((GAMEWIDTH, GAMEHEIGHT))

pygame.display.set_caption("FALLING CIRCLES")

# Circle types - Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
colors = [RED, GREEN, BLUE, YELLOW]  # List of colors for different types of circles

# Frame rate controller
clock = pygame.time.Clock()

# Gravity Constant
gravity = 0.7

# Defining the Circle class

class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocityY = 0          # Vertical Velocity
        self.velocityX = 0          # Horizontal Velocity (Rolling)
        self.bounceFactor = 0.3     # 0 = No Bounce, 1 = Perfect Bounce
        self.type = color

    def move(self):
        # Apply Gravity 
        self.velocityY += gravity
        self.x += self.velocityX
        self.y += self.velocityY

        # Bounce 
        if self.y + self.radius >= PLAYAREAHEIGHT:
            self.y = PLAYAREAHEIGHT - self.radius
            self.velocityY = -self.velocityY * self.bounceFactor

        # Wall check
        if self.x - self.radius <= 0 or self.x + self.radius >= PLAYAREAWIDTH:
            self.velocityX = - self.velocityX
    
    def draw(self):
        pygame.draw.circle(gameWindow, self.color, (int(self.x), int(self.y)), self.radius)

    def isColliding(self, other):
        # Collision Check
        distance = math.sqrt((self.x - other.x) **2 + (self.y - other.y) **2)
        return distance < self.radius + other.radius

    def merge(self, other):
        # If colliding, change circles to the next one
        if self.color == other.color:
            new_radius = self.radius + other.radius
            new_type = colors[(colors.index(self.color)+1)%len(colors)]
            return Circle(self.x, self.y, new_radius, new_type)

        return None

def create_new_circle():
    x = random.randint(50, PLAYAREAWIDTH-50)
    y = 0                                           # Change to actual start point
    radius = random.randint(10, 20)
    color = random.choice(colors)
    return Circle (x, y, radius, color)

def check_for_merge(circles):
    new_circles = []
    i = 0
    while i < len(circles):
        circle1 = circles[i]
        merged = False
        for j in range(i+1, len(circles)):
            circle2 = circles[j]
            if circle1.isColliding(circle2):
                merged_circle = circle1.merge(circle2)
                if merged_circle:
                    new_circles.append(merged_circle)
                    circles.pop(j)
                    merged = True
                    break
        if not merged:
            new_circles.append(circle1)
        i += 1
    return new_circles

# Main Game Loop
circles = []        # List to hold all the circles

while True:
    gameWindow.fill(WHITE)

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                circles.append(create_new_circle())

    # Update the positions
    for circle in circles:
        circle.move()

    # Check the Merge between circles
    circles = check_for_merge(circles)

    # Draw all the circles
    for circle in circles:
        circle.draw()

    # Update the game screen
    pygame.display.update()

    # Controlling the frame rate
    clock.tick(60)
