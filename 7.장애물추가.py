# Flappy Bird 게임
# 1. pygame 창 생성
# 2. 새(플레이어) 추가
# 3. 새(플레이어) 애니메이션 추가
# 4. 움직이지 않는 배경 추가
# 5. 움직이는 배경 추가
# 6. 바닥에 떨어지면 게임 종료
# 7. 장애물 추가

from pathlib import Path
import random

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
        self.mask = pygame.mask.from_surface(self.image)
        super().__init__(*groups)
    
    def update(self):
        self.fall_speed += self.GRAVITY
        self.rect.y += self.fall_speed
        
        self.images.insert(0, self.images.pop())
        self.image = self.images[0]
        
        if self.rect.x < 70:
            self.rect.x += 4

        # 새가 화면 아래로 완전히 사라지면 게임 오버
        global game_over
        if self.rect.top >= SCREEN_HEIGHT:
            game_over = True
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.fall_speed = 0 - self.FLAP_STRENGTH

    def check_collision(self, sprites):
        for sprite in sprites:
            if isinstance(sprite, Obstacle):
                if sprite.mask.overlap(self.mask, (self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y)):
                    return True
            # if self.rect.bottom < 0:
            #     return True
        return False

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

class Obstacle(pygame.sprite.Sprite):
    GAP = 100
    SPEED = 2
    
    def __init__(self, *groups):
        super().__init__(*groups)
        self._layer = 3
        self.passed = False
        
        self._create_pipes()
        self._set_position()
        
    def _create_pipes(self):
        pipe = get_sprite("pipe-green")
        pipe_rect = pipe.get_rect()
        
        self.pipe_bottom = pipe
        self.pipe_top = pygame.transform.flip(pipe, False, True)
        
        surface_height = pipe_rect.height * 2 + self.GAP
        self.image = pygame.Surface((pipe_rect.width, surface_height), pygame.SRCALPHA)
        self.image.blit(self.pipe_bottom, (0, pipe_rect.height + self.GAP))
        self.image.blit(self.pipe_top, (0, 0))
        
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
    def _set_position(self):
        floor_height = get_sprite("floor").get_rect().height
        min_y = 100
        max_y = SCREEN_HEIGHT - floor_height - 100
        self.rect.midleft = (SCREEN_WIDTH, random.uniform(min_y, max_y))
        
    def update(self):
        self.rect.x -= self.SPEED
        if self.rect.right <= 0:
            self.kill()
            
    def is_passed(self):
        if self.rect.x < 50 and not self.passed:
            self.passed = True
            return True
        return False

sprites = pygame.sprite.LayeredUpdates()
clock = pygame.time.Clock()  # FPS 설정을 위해

bird = Bird(sprites)
bg1 = Background(0, sprites)
bg2 = Background(1, sprites)

# pygame이 자동으로 고유한 이벤트 ID를 생성해줍
# 다른 사용자 정의 이벤트와 구분하기 위함
PIPE_SPAWN_EVENT = pygame.event.custom_type()
PIPE_SPAWN_INTERVAL = 1500  # 파이프 생성 간격 (밀리초, 2초마다)
pygame.time.set_timer(PIPE_SPAWN_EVENT, PIPE_SPAWN_INTERVAL)
# 이 함수는 주기적으로 이벤트를 발생시키는 타이머를 설정합니다.
# PIPE_SPAWN_EVENT라는 사용자 정의 이벤트를 PIPE_SPAWN_INTERVAL마다 발생시킵니다.

running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == PIPE_SPAWN_EVENT:
            obs = Obstacle(sprites)

        bird.handle_event(event)

    if not game_over:
        screen.fill(0)  # (0,0,0) RGB = black
        sprites.draw(screen)
        sprites.update()
            
        if bird.check_collision(sprites):
            game_over = True
            # pygame.time.set_timer(PIPE_SPAWN_EVENT, 0)
    else:
        # 게임 오버 메시지 표시
        msg = GameOverMessage(sprites)
        sprites.draw(screen)

        # 게임 오버 메시지가 표시된 후 Esc 키를 누르면 창 종료
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
