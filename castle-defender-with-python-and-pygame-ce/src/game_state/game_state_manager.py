import os

from enemy.constants import EnemyType
from settings import pygame
from timer import Timer

from .constants import (
    BEST_SCORE_FILE_NAME,
    INCREASE_MAX_HEALTH_AMOUNT,
    INCREASE_MAX_HEALTH_COST,
    LEVEL_DIFFICULTY_MULTIPLIER,
    LEVEL_START_DELAY,
    LEVEL_WON_DELAY,
    LEVELS_COUNT,
    REPAIR_HEALTH_AMOUNT,
    REPAIR_HEALTH_COST,
    STARTING_CASTLE_HEALTH,
    STARTING_ENEMY_DIFFICULTY,
    TOWER_COST,
)
from .game_state import GameState


class GameStateManager:
    def __init__(self):
        self._game_state = GameState.WAITING_TO_START
        self._current_level = 1
        self._level_difficulty = 0
        self._enemy_difficulty = STARTING_ENEMY_DIFFICULTY
        self._alive_enemies = 0
        self._subscribers = []
        self._start_level_timer = Timer(
            duration=LEVEL_START_DELAY, repeat=False, autostart=True
        )
        self._level_won_timer = Timer(duration=LEVEL_WON_DELAY)
        self.score = 0
        self.set_best_score()
        self.money = 0
        self._health = STARTING_CASTLE_HEALTH
        self.max_health = STARTING_CASTLE_HEALTH

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, value):
        self._game_state = value

    @property
    def current_level(self):
        return self._current_level

    @property
    def level_difficulty(self):
        return self._level_difficulty

    @level_difficulty.setter
    def level_difficulty(self, value):
        self._level_difficulty = value

    @property
    def alive_enemies(self):
        return self._alive_enemies

    @alive_enemies.setter
    def alive_enemies(self, value):
        self._alive_enemies = value

        if self.is_current_level_won():
            if self._current_level == LEVELS_COUNT:
                self._game_state = GameState.GAME_WON
            else:
                self._game_state = GameState.LEVEL_WON
                self._level_won_timer.activate()

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value

        if self._health <= 0:
            self._health = 0
            self._game_state = GameState.GAME_OVER

    def set_best_score(self):
        if os.path.exists(BEST_SCORE_FILE_NAME):
            # Open the file for reading
            with open(BEST_SCORE_FILE_NAME, "r") as file:
                self.best_score = int(file.read())
        else:
            self.best_score = 0

    def update_after_enemy_died(self, enemy_type):
        self.alive_enemies -= 1

        match enemy_type:
            case EnemyType.KNIGHT:
                self.score += 100
                self.money += 100
            case EnemyType.GOBLIN:
                self.score += 125
                self.money += 125
            case EnemyType.RED_GOBLIN:
                self.score += 150
                self.money += 150
            case EnemyType.PURPLE_GOBLIN:
                self.score += 200
                self.money += 200

    def repair_health(self):
        if self.health < self.max_health and self.money >= REPAIR_HEALTH_COST:
            self.health += REPAIR_HEALTH_AMOUNT
            self.money -= REPAIR_HEALTH_COST

            if self.health > self.max_health:
                self.health = self.max_health

    def increase_max_health(self):
        if self.money >= INCREASE_MAX_HEALTH_COST:
            self.max_health += INCREASE_MAX_HEALTH_AMOUNT
            self.money -= INCREASE_MAX_HEALTH_COST

    def add_tower(self):
        if self.money >= TOWER_COST:
            self.money -= TOWER_COST
            self.notify_all_add_tower()

    def move_to_next_level(self):
        self._current_level += 1
        self._alive_enemies = 0
        self._level_difficulty = 0
        self._enemy_difficulty *= LEVEL_DIFFICULTY_MULTIPLIER
        self.notify_all_new_level()
        self._game_state = GameState.WAITING_TO_START
        self._start_level_timer.activate()

        if self.best_score < self.score:
            self.best_score = self.score

            # Open the file for writting
            with open(BEST_SCORE_FILE_NAME, "w") as file:
                file.write(str(self.best_score))

    def is_current_level_won(self):
        return self._alive_enemies == 0

    def reached_level_difficulty(self):
        return self._level_difficulty >= self._enemy_difficulty

    def restart(self):
        self._current_level = 1
        self._alive_enemies = 0
        self._level_difficulty = 0
        self._enemy_difficulty = STARTING_ENEMY_DIFFICULTY
        self.score = 0
        self.money = 0
        self._health = STARTING_CASTLE_HEALTH
        self.max_health = STARTING_CASTLE_HEALTH
        self.notify_all_restart()
        self._game_state = GameState.WAITING_TO_START
        self._start_level_timer.activate()

    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)

    def notify_all_add_tower(self):
        for subscriber in self._subscribers:
            subscriber.create_tower()

    def notify_all_restart(self):
        for subscriber in self._subscribers:
            subscriber.restart()

    def notify_all_new_level(self):
        for subscriber in self._subscribers:
            subscriber.new_level()

    def update(self):
        self._start_level_timer.update()
        self._level_won_timer.update()

        is_mouse_cursor_visible = self._game_state in [
            GameState.GAME_WON,
            GameState.GAME_OVER,
        ]
        pygame.mouse.set_visible(is_mouse_cursor_visible)

        if (
            self._game_state == GameState.WAITING_TO_START
            and not self._start_level_timer.active
        ):
            self._game_state = GameState.RUNNING
        elif (
            self._game_state == GameState.LEVEL_WON and not self._level_won_timer.active
        ):
            self.move_to_next_level()


GAME_STATE_MANAGER = GameStateManager()


def get_game_state_manager():
    return GAME_STATE_MANAGER
