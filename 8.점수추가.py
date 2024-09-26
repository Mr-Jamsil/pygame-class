# Flappy Bird 게임
# 1. pygame 창 생성
# 2. 새(플레이어) 추가
# 3. 새(플레이어) 애니메이션 추가
# 4. 움직이지 않는 배경 추가
# 5. 움직이는 배경 추가
# 6. 바닥에 떨어지면 게임 종료
# 7. 장애물 추가
# 8. 점수 추가

from pathlib import Path

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
        self.mask = pygame.mask.from_surface(self.image) # NOTE
        super().__init__(*groups)
    
    def update(self):
        self.fall_speed += self.GRAVITY
        self.rect.y += self.fall_speed
        
        self.images.insert(0, self.images.pop())
        self.image = self.images[0]
        
        if self.rect.x < 70:
            self.rect.x += 4

        # NOTE 새가 화면 아래로 완전히 사라지면 게임 오버
        global game_over
        if self.rect.top >= SCREEN_HEIGHT:
            game_over = True
        
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


class GameOverMessage(Sprite):
    def __init__(self, *groups):
        self._layer = 4
        self.image = get_sprite("gameover")
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        super().__init__(*groups)

sprites = pygame.sprite.LayeredUpdates()
clock = pygame.time.Clock()  # FPS 설정을 위해

bird = Bird(sprites)
bg1 = Background(0, sprites)
bg2 = Background(1, sprites)

running = True
game_over = False # <---- NOTE
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        bird.handle_event(event)

    if not game_over:
        screen.fill(0)  # (0,0,0) RGB = black
        sprites.draw(screen)
        sprites.update()
    else:
        # 게임 오버 메시지 표시
        msg = GameOverMessage(sprites)
        sprites.draw(screen)

        # 게임 오버 메시지가 표시된 후 Esc 키를 누르면 종료
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            # 게임 창 종료
            running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
