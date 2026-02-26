from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAssetGroup
from castle.bullet import Bullet
from castle.castle import Castle
from enemy.constants import EnemyType
from enemy.enemy import Enemy
from settings import pygame, WINDOW_HEIGHT, WINDOW_WIDTH


class SpritesManager:
    def __init__(self):
        # The main surface on which we will be drawing sprites
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()

        self.asset_manager = get_asset_manager()
        Castle(
            group=self.all_sprites,
            images=self.asset_manager.graphics[ImageAssetGroup.CASTLE],
            position=(WINDOW_WIDTH - 430, WINDOW_HEIGHT - 470),
            create_bullet_function=self.create_bullet,
        )
        Enemy(
            groups=(self.all_sprites, self.enemy_sprites),
            animation_frames=self.asset_manager.graphics[ImageAssetGroup.KNIGHT],
            type=EnemyType.KNIGHT,
            position=(200, WINDOW_HEIGHT - 200),
        )

    def create_bullet(self, position, angle):
        Bullet(
            groups=(self.all_sprites, self.bullet_sprites),
            image=self.asset_manager.graphics[ImageAssetGroup.BULLET],
            position=position,
            angle=angle,
        )

    def update(self):
        delta_time = self.clock.tick() / 1000

        self.all_sprites.update(delta_time)

    def draw(self):
        self.all_sprites.draw(self.display_surface)
