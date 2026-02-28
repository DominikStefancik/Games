from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAssetGroup
from castle.bullet import Bullet
from castle.castle import Castle
from enemy.constants import EnemyType
from enemy.enemy import Enemy
from enemy.enemy_group import EnemyGroup
from settings import pygame, WINDOW_HEIGHT, WINDOW_WIDTH


class SpritesManager:
    def __init__(self):
        # The main surface on which we will be drawing sprites
        self.display_surface = pygame.display.get_surface()
        self.static_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = EnemyGroup()
        self.clock = pygame.time.Clock()

        self.asset_manager = get_asset_manager()
        self.castle = Castle(
            group=self.static_sprites,
            images=self.asset_manager.graphics[ImageAssetGroup.CASTLE],
            position=(WINDOW_WIDTH - 430, WINDOW_HEIGHT - 470),
            create_bullet_function=self.create_bullet,
        )
        Enemy(
            group=self.enemy_sprites,
            animation_frames=self.asset_manager.graphics[ImageAssetGroup.KNIGHT],
            type=EnemyType.KNIGHT,
            position=(350, WINDOW_HEIGHT - 200),
        )

    def create_bullet(self, position, angle):
        Bullet(
            group=self.bullet_sprites,
            image=self.asset_manager.graphics[ImageAssetGroup.BULLET],
            position=position,
            angle=angle,
        )

    def update(self):
        delta_time = self.clock.tick() / 1000

        self.static_sprites.update(delta_time)
        self.enemy_sprites.update(delta_time, self.castle, self.bullet_sprites)
        self.bullet_sprites.update(delta_time)

    def draw(self):
        self.static_sprites.draw(self.display_surface)
        self.enemy_sprites.draw()
        self.bullet_sprites.draw(self.display_surface)
