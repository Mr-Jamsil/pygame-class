import pygame
from pathlib import Path
from pygame import Rect
from pygame.sprite import Sprite, LayeredUpdates
from pygame.surface import Surface
from pygame.time import Clock

TITLE = "Flappy Bird"
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
FPS = 120

PROJ_DIR = Path(__file__).parent
SPRITE_DIR = PROJ_DIR / "assets" / "sprites"
ICON_DIR = PROJ_DIR / "assets" / "icons"


pygame.init()

pygame.display.set_caption("Flappy Bird")
pygame.display.set_caption(TITLE)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def get_sprite(name):
    return pygame.image.load(SPRITE_DIR / f"{name}.png")

pygame.image.load("이미지파일명.png")

sprites = LayeredUpdates()
clock = Clock()


class Bird(Sprite):
    GRAVITY = 0.4
    FLAP_STRENGTH = 6
    
    def __init__(self, *groups):
        self.images = [
            get_sprite("redbird-0"),
            get_sprite("redbird-1"),
            get_sprite("redbird-2")
        ]
        self.image = get_sprite("redbird-0")
        self.rect = self.image.get_rect(topleft=(50, 50))
        self.fall_speed = 0
        super().__init__(*groups)
        
    def update(self):
        self.images.insert(0, self.images.pop())
        self.image = self.images[0]
        
        GRAVITY = 0.4
        self.fall_speed += GRAVITY
        self.rect.y += self.fall_speed
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.fall_speed = -6
            
            
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
