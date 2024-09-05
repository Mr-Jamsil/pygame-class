import pygame
from pathlib import Path
from pygame.sprite import Group, Sprite

pygame.init()

pygame.display.set_caption("Flappy Bird")

screen_size = (288, 512)
screen = pygame.display.set_mode(screen_size)

def get_sprite(name):
    directory = Path(__file__).parent / 'assets' / 'sprites'
    return pygame.image.load(directory / f"{name}.png")


class Bird(Sprite):
    def __init__(self, *groups):
        self.image = get_sprite("redbird-0")
        self.rect = self.image.get_rect(topleft=(50, 50))
        self.fall_speed = 0
        super().__init__(*groups)
    
    def update(self):
        GRAVITY = 0.4
        self.fall_speed += GRAVITY
        self.rect.y += self.fall_speed
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.fall_speed = -6


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
    clock.tick(60)

pygame.quit()
