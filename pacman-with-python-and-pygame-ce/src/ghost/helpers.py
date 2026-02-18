from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAsset
from settings import Direction, pygame

from .constants import GhostImageType, GhostType


def get_ghost_images(ghost_type):
    asset_manager = get_asset_manager()
    main_image = None

    match ghost_type:
        case GhostType.BLINKY:
            main_image = asset_manager.graphics[ImageAsset.BLINKY_GHOST]
        case GhostType.PINKY:
            main_image = asset_manager.graphics[ImageAsset.PINKY_GHOST]
        case GhostType.INKY:
            main_image = asset_manager.graphics[ImageAsset.INKY_GHOST]
        case GhostType.CLYDE:
            main_image = asset_manager.graphics[ImageAsset.CLYDE_GHOST]

    return {
        # We have to scale an original ghost images, because they are too big
        GhostImageType.MAIN: pygame.transform.scale(main_image, (45, 45)),
        GhostImageType.SPOOKED: pygame.transform.scale(
            asset_manager.graphics[ImageAsset.SPOOKED_GHOST], (45, 45)
        ),
        GhostImageType.DEAD: pygame.transform.scale(
            asset_manager.graphics[ImageAsset.DEAD_GHOST], (45, 45)
        ),
    }


# Clyde is going to turn whenever advantageous for pursuit the Pacman
def move_clyde(clyde_ghost):
    # The Pacman is left from the ghost and the ghost can go left
    can_follow_target_to_left = (
        clyde_ghost.target[0] < clyde_ghost.rect.x
        and clyde_ghost.allowed_turns[Direction.LEFT]
    )
    # The Pacman is right from the ghost and the ghost can go right
    can_follow_target_to_right = (
        clyde_ghost.target[0] > clyde_ghost.rect.x
        and clyde_ghost.allowed_turns[Direction.RIGHT]
    )
    # The Pacman is above the ghost and the ghost can go up
    can_follow_target_up = (
        clyde_ghost.target[1] < clyde_ghost.rect.y
        and clyde_ghost.allowed_turns[Direction.UP]
    )
    # The Pacman is below the ghost and the ghost can go down
    can_follow_target_down = (
        clyde_ghost.target[1] > clyde_ghost.rect.y
        and clyde_ghost.allowed_turns[Direction.DOWN]
    )

    # Direction to the right is he default ghost's direction
    if clyde_ghost.direction == Direction.RIGHT:
        if can_follow_target_to_right:
            clyde_ghost.rect.centerx += clyde_ghost.speed
        elif not clyde_ghost.allowed_turns[Direction.RIGHT]:
            if can_follow_target_down:
                clyde_ghost.direction = Direction.DOWN
                clyde_ghost.rect.centery += clyde_ghost.speed
            if can_follow_target_up:
                clyde_ghost.direction = Direction.UP
                clyde_ghost.rect.centery -= clyde_ghost.speed
            elif can_follow_target_to_left:
                clyde_ghost.direction = Direction.LEFT
                clyde_ghost.rect.centerx -= clyde_ghost.speed
            # The Pacman is above/below and left from ghost and the ghost cannot go above/below and left,
            # so we try to move it any possible direction.
            elif clyde_ghost.allowed_turns[Direction.DOWN]:
                clyde_ghost.direction = Direction.DOWN
                clyde_ghost.rect.centery += clyde_ghost.speed
            elif clyde_ghost.allowed_turns[Direction.UP]:
                clyde_ghost.direction = Direction.UP
                clyde_ghost.rect.centery -= clyde_ghost.speed
            elif clyde_ghost.allowed_turns[Direction.LEFT]:
                clyde_ghost.direction = Direction.LEFT
                clyde_ghost.rect.centerx -= clyde_ghost.speed
        # The ghost can go right, but the Pacman is not on the right side
        elif clyde_ghost.allowed_turns[Direction.RIGHT]:
            if can_follow_target_up:
                clyde_ghost.direction = Direction.DOWN
                clyde_ghost.rect.centery += clyde_ghost.speed
            elif can_follow_target_up:
                clyde_ghost.direction = Direction.UP
                clyde_ghost.rect.centery -= clyde_ghost.speed
            # The Pacman is not up or down from the ghost
            # so it will go its default direction right
            else:
                clyde_ghost.rect.centerx += clyde_ghost.speed
    elif clyde_ghost.direction == Direction.LEFT:
        if can_follow_target_down:
            clyde_ghost.direction = Direction.DOWN
        elif can_follow_target_to_left:
            clyde_ghost.rect.centerx -= clyde_ghost.speed
        elif not clyde_ghost.allowed_turns[Direction.LEFT]:
            if can_follow_target_up:
                clyde_ghost.direction = Direction.UP
                clyde_ghost.rect.centery -= clyde_ghost.speed
            elif can_follow_target_to_right:
                clyde_ghost.direction = Direction.RIGHT
                clyde_ghost.rect.centerx += clyde_ghost.speed
            elif can_follow_target_down:
                clyde_ghost.direction = Direction.DOWN
                clyde_ghost.rect.centery += clyde_ghost.speed
            # The Pacman is above/below and right from the ghost and the ghost cannot go above/below and right,
            # so we try to move it any possible direction.
            elif clyde_ghost.allowed_turns[Direction.DOWN]:
                clyde_ghost.direction = Direction.DOWN
                clyde_ghost.rect.centery += clyde_ghost.speed
            elif clyde_ghost.allowed_turns[Direction.UP]:
                clyde_ghost.direction = Direction.UP
                clyde_ghost.rect.centery -= clyde_ghost.speed
            elif clyde_ghost.allowed_turns[Direction.RIGHT]:
                clyde_ghost.direction = Direction.RIGHT
                clyde_ghost.rect.centerx += clyde_ghost.speed
        # The ghost can go left, but the Pacman is not on the left side
        elif clyde_ghost.allowed_turns[Direction.LEFT]:
            if can_follow_target_down:
                clyde_ghost.direction = Direction.DOWN
                clyde_ghost.rect.centery += clyde_ghost.speed
            elif can_follow_target_up:
                clyde_ghost.direction = Direction.UP
                clyde_ghost.rect.centery -= clyde_ghost.speed

            # The Pacman is not up or down from the ghost
            # so it will go its default direction left
            else:
                clyde_ghost.rect.centerx -= clyde_ghost.speed
    elif clyde_ghost.direction == Direction.UP:
        if can_follow_target_to_left:
            clyde_ghost.direction = Direction.LEFT
            clyde_ghost.rect.centerx -= clyde_ghost.speed
        elif can_follow_target_up:
            clyde_ghost.rect.centery -= clyde_ghost.speed
        elif not clyde_ghost.allowed_turns[Direction.UP]:
            if can_follow_target_to_right:
                clyde_ghost.direction = Direction.RIGHT
                clyde_ghost.rect.centerx += clyde_ghost.speed
            elif can_follow_target_to_left:
                clyde_ghost.direction = Direction.LEFT
                clyde_ghost.rect.centerx -= clyde_ghost.speed
            elif can_follow_target_down:
                clyde_ghost.direction = Direction.DOWN
                clyde_ghost.rect.centery += clyde_ghost.speed
            # The Pacman is left/right and up from the ghost and the ghost cannot go left/right and up,
            # so we try to move it any possible direction
            if clyde_ghost.allowed_turns[Direction.DOWN]:
                clyde_ghost.direction = Direction.DOWN
                clyde_ghost.rect.centery += clyde_ghost.speed
            elif clyde_ghost.allowed_turns[Direction.LEFT]:
                clyde_ghost.direction = Direction.LEFT
                clyde_ghost.rect.centerx -= clyde_ghost.speed
            elif clyde_ghost.allowed_turns[Direction.RIGHT]:
                clyde_ghost.direction = Direction.RIGHT
                clyde_ghost.rect.centerx += clyde_ghost.speed
        # The ghost can go up, but the Pacman is not on the upper side
        elif clyde_ghost.allowed_turns[Direction.UP]:
            if can_follow_target_to_left:
                clyde_ghost.direction = Direction.LEFT
                clyde_ghost.rect.centerx -= clyde_ghost.speed
            elif can_follow_target_to_right:
                clyde_ghost.direction = Direction.RIGHT
                clyde_ghost.rect.centerx += clyde_ghost.speed
            # The Pacman is not left or right from the ghost
            # so it will go its default direction up
            else:
                clyde_ghost.rect.centery -= clyde_ghost.speed
    elif clyde_ghost.direction == Direction.DOWN:
        if can_follow_target_down:
            clyde_ghost.rect.centery += clyde_ghost.speed
        elif not clyde_ghost.allowed_turns[Direction.DOWN]:
            if can_follow_target_to_right:
                clyde_ghost.direction = Direction.RIGHT
                clyde_ghost.rect.centerx += clyde_ghost.speed
            elif can_follow_target_to_left:
                clyde_ghost.direction = Direction.LEFT
                clyde_ghost.rect.centerx -= clyde_ghost.speed
            elif can_follow_target_up:
                clyde_ghost.direction = Direction.UP
                clyde_ghost.rect.centery -= clyde_ghost.speed
            # The Pacman is left/right and down from the ghost and the ghost cannot go left/right and down,
            # so we try to move it any possible direction
            if clyde_ghost.allowed_turns[Direction.UP]:
                clyde_ghost.direction = Direction.UP
                clyde_ghost.rect.centery -= clyde_ghost.speed
            elif clyde_ghost.allowed_turns[Direction.LEFT]:
                clyde_ghost.direction = Direction.LEFT
                clyde_ghost.rect.centerx -= clyde_ghost.speed
            elif clyde_ghost.allowed_turns[Direction.RIGHT]:
                clyde_ghost.direction = Direction.RIGHT
                clyde_ghost.rect.centerx += clyde_ghost.speed
        # The ghost can go down, but the Pacman is not on the down side
        elif clyde_ghost.allowed_turns[Direction.DOWN]:
            if can_follow_target_to_left:
                clyde_ghost.direction = Direction.LEFT
                clyde_ghost.rect.centerx -= clyde_ghost.speed
            elif can_follow_target_to_right:
                clyde_ghost.direction = Direction.RIGHT
                clyde_ghost.rect.centerx += clyde_ghost.speed
            # The Pacman is not left or right from the ghost
            # so it will go its default direction down
            else:
                clyde_ghost.rect.centery += clyde_ghost.speed
