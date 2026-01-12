import pygame
import random
from .constants import HEALTH, MONEY
from enemy.constants import ENEMY_SPAWN_DATA


class World:
    def __init__(self, map_image, metadata) -> None:
        self.level = 1
        self.level_metadata = metadata
        self.health = HEALTH
        self.money = MONEY
        self.image = map_image
        self.tile_map = []
        self.waypoints = []
        self.enemy_type_list = []
        self.spawned_enemies = 0
        self.process_metadata()
        self.process_enemies()

    def process_metadata(self):
        # Look through JSON metadata to extract relevant info
        for layer in self.level_metadata["layers"]:
            if layer["name"] == "tilemap":
                self.tile_map = layer["data"]
            elif layer["name"] == "waypoints":
                for object in layer["objects"]:
                    # the "waypoints_data" contains a list coordinates in the form of dictionaries
                    waypoints_data = object["polyline"]
                    self.process_waypoints(waypoints_data)

    # Iterates ovet the list of dictionaries to extract individual sets of X and Y coordinates
    def process_waypoints(self, waypoints_data):
        for point in waypoints_data:
            waypoint = (point.get("x"), point.get("y"))
            self.waypoints.append(waypoint)

    def process_enemies(self):
        enemies = ENEMY_SPAWN_DATA[self.level - 1]

        for enemy_type in enemies:
            number_of_enemies_to_spawn = enemies[enemy_type]

            for enemy in range(number_of_enemies_to_spawn):
                self.enemy_type_list.append(enemy_type)

        # At the end, randomise the list to shuffle the enemies types
        random.shuffle(self.enemy_type_list)

    def draw(self, surface):
        # the map will be drawn from the top left corner over the whole window
        surface.blit(self.image, (0, 0))
