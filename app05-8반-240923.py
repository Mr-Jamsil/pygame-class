# Flappy Bird 게임
# 1. pygame 창 생성
# 2. 새(플레이어) 추가
# 3. 새(플레이어) 애니메이션 추가
# 4. 움직이지 않는 배경 추가

from pathlib import Path
from typing import Any

import pygame
from pygame.sprite import Sprite

TITLE = "Flappy Bird"
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
FPS = 60      

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
    GRAVITY = 0.4
    FLAP_STRENGTH = 6
    INITIAL_POSITION = (-50, 50)
    
    def __init__(self, *groups):
        self._layer = 5
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
        
        if self.rect.x < 70:
            self.rect.x += 4
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.fall_speed = 0 - self.FLAP_STRENGTH

class Background(Sprite):
    def __init__(self, index, *groups):
        self._layer = 0
        self.image = get_sprite("background")
        self.rect = self.image.get_rect(topleft=(SCREEN_WIDTH*index, 0))
        super().__init__(*groups)

    def update(self):
        self.rect.x -= 1
        if self.rect.right <= 0:
            self.rect.x = SCREEN_WIDTH


sprites = pygame.sprite.LayeredUpdates()
clock = pygame.time.Clock()  # FPS 설정을 위해

bird = Bird(sprites)
bg1 = Background(0, sprites)
bg2 = Background(1, sprites)

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
