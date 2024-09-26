import pygame
from pathlib import Path
from pygame import Rect
from pygame.sprite import Sprite, LayeredUpdates
from pygame.surface import Surface
from pygame.time import Clock
from enum import IntEnum, auto
TITLE = "Flappy Bird"
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512

TOP_DIR = Path(__file__).parent
PROJ_DIR = Path(__file__).parent
SPRITES_DIR = PROJ_DIR / "assets" / "sprites"

pygame.init()

pygame.display.set_caption(TITLE)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
running = True


# 스프라이트(Sprites) = 2D 그래픽 오브젝트
sprites = LayeredUpdates()
clock = Clock()



class Layer(IntEnum):
    BACKGROUND = auto()
    OBSTACLE = auto()
    FLOOR = auto()
    PLAYER = auto()
    UI = auto()


def load_sprites():
    sprites = {}
    for file in SPRITES_DIR.iterdir():
        sprites[file.stem] = pygame.image.load(file)
    return sprites


def get_sprite(name) -> Surface:
    return pygame.image.load(SPRITES_DIR / f"{name}.png")

class Bird(Sprite):
    GRAVITY = 0.4  # 중력 (프레임마다 증가하는 떨어지는 속도)
    FLAP_STRENGTH = 6  # 날갯짓 강도
    ANIMATION_SPEED = 0.1  # 기본 애니메이션 속도
    FLAP_ANIMATION_SPEED = 0.2  # 날갯짓 애니메이션 속도 (더 빠름)
    FLAP_DURATION = 15  # space를 뗀 후 몇 프레임 동안 애니메이션이 계속될지 설정

    def __init__(self, *groups):
        self._layer = Layer.PLAYER  # 새는 위쪽 레이어에 그리기 위해 레이어를 1로 설정

        self.images = [
            get_sprite("redbird-0"),  # 날개 접힌 상태
            get_sprite("redbird-1"),  # 날개 중간 상태
            get_sprite("redbird-2"),  # 날개 펴진 상태
            get_sprite("redbird-1"),  # 날개 중간 상태
        ]

        # 기본 이미지는 첫번째 이미지로 설정
        self.image = self.images[0]

        # 이미지의 위치는 (-50, 50)으로 설정
        self.rect: Rect = self.image.get_rect(topleft=(-50, 50))

        self.mask = pygame.mask.from_surface(self.image)

        self.fall_speed = 0

        # 애니메이션 인덱스 및 속도 제어를 위한 변수
        self.animation_index = 0
        self.animation_timer = 0

        # space 키가 눌렸는지 여부
        self.flapping = False

        # space를 뗀 후에도 몇 프레임 동안 펄럭이는 것을 유지하는 타이머
        self.flap_timer = 0

        super().__init__(*groups)

    def update(self):
        # 날갯짓 상태에 따른 애니메이션 처리
        if self.flapping or self.flap_timer > 0:
            self.animation_timer += self.FLAP_ANIMATION_SPEED
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.animation_index = (self.animation_index + 1) % len(self.images)
                self.image = self.images[self.animation_index]

            # 만약 space 키가 떼어진 상태라면 타이머를 줄임
            if not self.flapping:
                self.flap_timer -= 1
        else:
            # space 키가 눌리지 않았을 때는 0번째 이미지 (가만히 떨어지는 상태)
            self.image = self.images[0]

        # 중력 및 위치 업데이트
        self.fall_speed += self.GRAVITY
        self.rect.y += self.fall_speed

        # 새가 시작 위치로 이동하는 코드
        if self.rect.x < 50:
            self.rect.x += 3

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.flapping = True
            self.fall_speed = 0
            self.fall_speed -= self.FLAP_STRENGTH

        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            self.flapping = False
            self.flap_timer = self.FLAP_DURATION  # space 키를 뗀 후에도 애니메이션을 유지할 타이머 설정
            
            
            
class Background(Sprite):
    def __init__(self, speed, *groups):
        self._layer = Layer.BACKGROUND  # 배경은 아래쪽 레이어에 그리기 위해 레이어를 0으로 설정
        super().__init__(*groups)
        self.image = get_sprite("background")
        self.speed = speed  # 배경의 스크롤 속도 설정
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.rect2 = self.image.get_rect(topleft=(SCREEN_WIDTH, 0))  # 두 번째 배경 위치 설정

    def update(self):
        # 배경을 왼쪽으로 이동
        self.rect.x -= self.speed
        self.rect2.x -= self.speed

        # 첫 번째 배경이 화면을 벗어나면 오른쪽 끝으로 이동
        if self.rect.right <= 0:
            self.rect.x = SCREEN_WIDTH

        # 두 번째 배경이 화면을 벗어나면 오른쪽 끝으로 이동
        if self.rect2.right <= 0:
            self.rect2.x = SCREEN_WIDTH

    def draw(self, screen):
        # 두 배경을 모두 그립니다
        screen.blit(self.image, self.rect)
        screen.blit(self.image, self.rect2)
                    
                    

class Floor(pygame.sprite.Sprite):
    def __init__(self, index, *groups):
        self._layer = Layer.FLOOR
        self.image = get_sprite("floor")
        self.rect = self.image.get_rect(bottomleft=(SCREEN_WIDTH * index, SCREEN_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)
        super().__init__(*groups)

    def update(self):
        self.rect.x -= 2

        if self.rect.right <= 0:
            self.rect.x = SCREEN_WIDTH

bird = Bird(sprites)
background = Background(2, sprites)
# Floor(0, sprites)
# Floor(1, sprites)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        bird.handle_event(event)

    screen.fill(0)
    background.draw(screen)
    sprites.draw(screen)
    sprites.update()

    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()
