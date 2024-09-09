import pygame
from pathlib import Path
from pygame.sprite import Group, Sprite

TITLE = "Flappy Bird"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 120

PROJ_DIR = Path(__file__).parent
ICON_DIR = PROJ_DIR / "assets" / "icons"

pygame.init()
pygame.display.set_caption(TITLE)

icon = pygame.image.load(ICON_DIR / "red_bird.png")
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def get_sprite(name):
    directory = Path(__file__).parent / 'assets' / 'sprites'
    return pygame.image.load(directory / f"{name}.png")


class Bird(Sprite):
    GRAVITY = 0.2
    FLAP_STRENGTH = 9
    INITIAL_POSITION = (50, 50)
    
    def __init__(self, *groups):
        self.images = [
            get_sprite("redbird-0"),
            get_sprite("redbird-1"),
            get_sprite("redbird-2"),
        ]
        self.image = get_sprite("redbird-0")
        self.rect = self.image.get_rect(topleft=self.INITIAL_POSITION)
        self.fall_speed = 0
        super().__init__(*groups)
    
    def update(self):
        self.fall_speed += self.GRAVITY
        self.rect.y += self.fall_speed
        
        self.images.insert(0, self.images.pop())
        self.image = self.images[0]
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.fall_speed = 0 - self.FLAP_STRENGTH


sprites = pygame.sprite.LayeredUpdates()
clock = pygame.time.Clock()  # FPS 설정을 위해

bird = Bird(sprites)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        bird.handle_event(event)

    screen.fill(0)  # (0,0,0) RGB = black
    screen.fill("pink")
    
    sprites.draw(screen)
    sprites.update()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
