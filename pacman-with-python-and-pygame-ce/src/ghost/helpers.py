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


# Blinky is going to turn whenener colliing with walls, otherwise he will continue straight
def move_blinky(ghost):
    # The Pacman is left from the ghost and the ghost can go left
    can_follow_target_to_left = (
        ghost.target_position.x < ghost.rect.x and ghost.allowed_turns[Direction.LEFT]
    )
    # The Pacman is right from the ghost and the ghost can go right
    can_follow_target_to_right = (
        ghost.target_position.x > ghost.rect.x and ghost.allowed_turns[Direction.RIGHT]
    )
    # The Pacman is above the ghost and the ghost can go up
    can_follow_target_up = (
        ghost.target_position.y < ghost.rect.y and ghost.allowed_turns[Direction.UP]
    )
    # The Pacman is below the ghost and the ghost can go down
    can_follow_target_down = (
        ghost.target_position.y > ghost.rect.y and ghost.allowed_turns[Direction.DOWN]
    )

    # Direction to the right is he default ghost's direction
    if ghost.direction == Direction.RIGHT:
        if can_follow_target_to_right:
            ghost.rect.centerx += ghost.speed
        elif not ghost.allowed_turns[Direction.RIGHT]:
            if can_follow_target_down:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            if can_follow_target_up:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            elif can_follow_target_to_left:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            # The Pacman is above/below and left from ghost and the ghost cannot go above/below and left,
            # so we try to move it any possible direction.
            elif ghost.allowed_turns[Direction.DOWN]:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            elif ghost.allowed_turns[Direction.UP]:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            elif ghost.allowed_turns[Direction.LEFT]:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
        # The ghost can go right, so he will continue going right
        elif ghost.allowed_turns[Direction.RIGHT]:
            ghost.rect.centerx += ghost.speed
    elif ghost.direction == Direction.LEFT:
        if can_follow_target_to_left:
            ghost.rect.centerx -= ghost.speed
        elif not ghost.allowed_turns[Direction.LEFT]:
            if can_follow_target_down:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            elif can_follow_target_up:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            elif can_follow_target_to_right:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
            # The Pacman is above/below and right from the ghost and the ghost cannot go above/below and right,
            # so we try to move it any possible direction.
            elif ghost.allowed_turns[Direction.DOWN]:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            elif ghost.allowed_turns[Direction.UP]:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            elif ghost.allowed_turns[Direction.RIGHT]:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
        # The ghost can go left, so he will continue going left
        elif ghost.allowed_turns[Direction.LEFT]:
            ghost.rect.centerx -= ghost.speed
    elif ghost.direction == Direction.UP:
        if can_follow_target_up:
            ghost.rect.centery -= ghost.speed
        elif not ghost.allowed_turns[Direction.UP]:
            if can_follow_target_to_right:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
            elif can_follow_target_to_left:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            elif can_follow_target_down:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            # The Pacman is left/right and up from the ghost and the ghost cannot go left/right and up,
            # so we try to move it any possible direction
            elif ghost.allowed_turns[Direction.DOWN]:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            elif ghost.allowed_turns[Direction.RIGHT]:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
            elif ghost.allowed_turns[Direction.LEFT]:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
        # The ghost can go up, so he will continue going up
        elif ghost.allowed_turns[Direction.UP]:
            ghost.rect.centery -= ghost.speed
    elif ghost.direction == Direction.DOWN:
        if can_follow_target_down:
            ghost.rect.centery += ghost.speed
        elif not ghost.allowed_turns[Direction.DOWN]:
            if can_follow_target_to_right:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
            elif can_follow_target_to_left:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            elif can_follow_target_up:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            # The Pacman is left/right and down from the ghost and the ghost cannot go left/right and down,
            # so we try to move it any possible direction
            if ghost.allowed_turns[Direction.UP]:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            elif ghost.allowed_turns[Direction.RIGHT]:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
            elif ghost.allowed_turns[Direction.LEFT]:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
        # The ghost can go down, so he will continue going down
        elif ghost.allowed_turns[Direction.DOWN]:
            ghost.rect.centery += ghost.speed


# Inky is going to turn up or down at any point to pursue the Pacman,
# but left and right only on collision
def move_inky(ghost):
    # The Pacman is left from the ghost and the ghost can go left
    can_follow_target_to_left = (
        ghost.target_position.x < ghost.rect.x and ghost.allowed_turns[Direction.LEFT]
    )
    # The Pacman is right from the ghost and the ghost can go right
    can_follow_target_to_right = (
        ghost.target_position.x > ghost.rect.x and ghost.allowed_turns[Direction.RIGHT]
    )
    # The Pacman is above the ghost and the ghost can go up
    can_follow_target_up = (
        ghost.target_position.y < ghost.rect.y and ghost.allowed_turns[Direction.UP]
    )
    # The Pacman is below the ghost and the ghost can go down
    can_follow_target_down = (
        ghost.target_position.y > ghost.rect.y and ghost.allowed_turns[Direction.DOWN]
    )

    # Direction to the right is he default ghost's direction
    if ghost.direction == Direction.RIGHT:
        if can_follow_target_to_right:
            ghost.rect.centerx += ghost.speed
        elif not ghost.allowed_turns[Direction.RIGHT]:
            if can_follow_target_down:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            if can_follow_target_up:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            elif can_follow_target_to_left:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            # The Pacman is above/below and left from ghost and the ghost cannot go above/below and left,
            # so we try to move it any possible direction.
            elif ghost.allowed_turns[Direction.DOWN]:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            elif ghost.allowed_turns[Direction.UP]:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            elif ghost.allowed_turns[Direction.LEFT]:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
        # The ghost can go right, but the Pacman is not on the right side
        elif ghost.allowed_turns[Direction.RIGHT]:
            if can_follow_target_up:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            elif can_follow_target_up:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            # The Pacman is not up or down from the ghost
            # so it will go its default direction right
            else:
                ghost.rect.centerx += ghost.speed
    elif ghost.direction == Direction.LEFT:
        if can_follow_target_down:
            ghost.direction = Direction.DOWN
        elif can_follow_target_to_left:
            ghost.rect.centerx -= ghost.speed
        elif not ghost.allowed_turns[Direction.LEFT]:
            if can_follow_target_down:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            elif can_follow_target_up:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            elif can_follow_target_to_right:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
            # The Pacman is above/below and right from the ghost and the ghost cannot go above/below and right,
            # so we try to move it any possible direction.
            elif ghost.allowed_turns[Direction.DOWN]:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            elif ghost.allowed_turns[Direction.UP]:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            elif ghost.allowed_turns[Direction.RIGHT]:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
        # The ghost can go left, but the Pacman is not on the left side
        elif ghost.allowed_turns[Direction.LEFT]:
            if can_follow_target_down:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            elif can_follow_target_up:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            # The Pacman is not up or down from the ghost
            # so it will go its default direction left
            else:
                ghost.rect.centerx -= ghost.speed
    elif ghost.direction == Direction.UP:
        if can_follow_target_up:
            ghost.rect.centery -= ghost.speed
        elif not ghost.allowed_turns[Direction.UP]:
            if can_follow_target_to_right:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
            elif can_follow_target_to_left:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            elif can_follow_target_down:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            # The Pacman is left/right and up from the ghost and the ghost cannot go left/right and up,
            # so we try to move it any possible direction
            elif ghost.allowed_turns[Direction.LEFT]:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            elif ghost.allowed_turns[Direction.DOWN]:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            elif ghost.allowed_turns[Direction.RIGHT]:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
        # The ghost can go up, so he will continue going up
        elif ghost.allowed_turns[Direction.UP]:
            ghost.rect.centery -= ghost.speed
    elif ghost.direction == Direction.DOWN:
        if can_follow_target_down:
            ghost.rect.centery += ghost.speed
        elif not ghost.allowed_turns[Direction.DOWN]:
            if can_follow_target_to_right:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
            elif can_follow_target_to_left:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            elif can_follow_target_up:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            # The Pacman is left/right and down from the ghost and the ghost cannot go left/right and down,
            # so we try to move it any possible direction
            if ghost.allowed_turns[Direction.UP]:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            elif ghost.allowed_turns[Direction.LEFT]:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            elif ghost.allowed_turns[Direction.RIGHT]:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
        # The ghost can go down, so he will continue going down
        elif ghost.allowed_turns[Direction.DOWN]:
            ghost.rect.centery += ghost.speed


# Pinky is going to turn left or right at any point to pursue the Pacman,
# but up and down only on collision
def move_pinky(ghost):
    # The Pacman is left from the ghost and the ghost can go left
    can_follow_target_to_left = (
        ghost.target_position.x < ghost.rect.x and ghost.allowed_turns[Direction.LEFT]
    )
    # The Pacman is right from the ghost and the ghost can go right
    can_follow_target_to_right = (
        ghost.target_position.x > ghost.rect.x and ghost.allowed_turns[Direction.RIGHT]
    )
    # The Pacman is above the ghost and the ghost can go up
    can_follow_target_up = (
        ghost.target_position.y < ghost.rect.y and ghost.allowed_turns[Direction.UP]
    )
    # The Pacman is below the ghost and the ghost can go down
    can_follow_target_down = (
        ghost.target_position.y > ghost.rect.y and ghost.allowed_turns[Direction.DOWN]
    )

    # Direction to the right is he default ghost's direction
    if ghost.direction == Direction.RIGHT:
        if can_follow_target_to_right:
            ghost.rect.centerx += ghost.speed
        elif not ghost.allowed_turns[Direction.RIGHT]:
            if can_follow_target_down:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            if can_follow_target_up:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            elif can_follow_target_to_left:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            # The Pacman is above/below and left from ghost and the ghost cannot go above/below and left,
            # so we try to move it any possible direction.
            elif ghost.allowed_turns[Direction.DOWN]:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            elif ghost.allowed_turns[Direction.UP]:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            elif ghost.allowed_turns[Direction.LEFT]:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
        # The ghost can go right, so he will continue going right
        elif ghost.allowed_turns[Direction.RIGHT]:
            ghost.rect.centerx += ghost.speed
    elif ghost.direction == Direction.LEFT:
        if can_follow_target_to_left:
            ghost.rect.centerx -= ghost.speed
        elif not ghost.allowed_turns[Direction.LEFT]:
            if can_follow_target_down:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            elif can_follow_target_up:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            elif can_follow_target_to_right:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
            # The Pacman is above/below and right from the ghost and the ghost cannot go above/below and right,
            # so we try to move it any possible direction.
            elif ghost.allowed_turns[Direction.DOWN]:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            elif ghost.allowed_turns[Direction.UP]:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            elif ghost.allowed_turns[Direction.RIGHT]:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
        # The ghost can go left, so he will continue going left
        elif ghost.allowed_turns[Direction.LEFT]:
            ghost.rect.centerx -= ghost.speed
    elif ghost.direction == Direction.UP:
        if can_follow_target_up:
            ghost.rect.centery -= ghost.speed
        elif not ghost.allowed_turns[Direction.UP]:
            if can_follow_target_to_right:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
            elif can_follow_target_to_left:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            elif can_follow_target_down:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            # The Pacman is left/right and up from the ghost and the ghost cannot go left/right and up,
            # so we try to move it any possible direction
            elif ghost.allowed_turns[Direction.LEFT]:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            elif ghost.allowed_turns[Direction.DOWN]:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            elif ghost.allowed_turns[Direction.RIGHT]:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
        # The ghost can go up, but the Pacman is not on the upper side
        elif ghost.allowed_turns[Direction.UP]:
            if can_follow_target_to_right:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
            elif can_follow_target_to_left:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            # The Pacman is not left or right from the ghost
            # so it will go its default direction up
            else:
                ghost.rect.centery -= ghost.speed
    elif ghost.direction == Direction.DOWN:
        if can_follow_target_down:
            ghost.rect.centery += ghost.speed
        elif not ghost.allowed_turns[Direction.DOWN]:
            if can_follow_target_to_right:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
            elif can_follow_target_to_left:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            elif can_follow_target_up:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            # The Pacman is left/right and down from the ghost and the ghost cannot go left/right and down,
            # so we try to move it any possible direction
            if ghost.allowed_turns[Direction.UP]:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            elif ghost.allowed_turns[Direction.LEFT]:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            elif ghost.allowed_turns[Direction.RIGHT]:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
        # The ghost can go down, but the Pacman is not on the down side
        elif ghost.allowed_turns[Direction.DOWN]:
            if can_follow_target_to_right:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
            elif can_follow_target_to_left:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            # The Pacman is not left or right from the ghost
            # so it will go its default direction down
            else:
                ghost.rect.centery += ghost.speed


# A ghost is going to turn whenever advantageous for pursuit the Pacman
def move_towards_target(ghost):
    # The Pacman is left from the ghost and the ghost can go left
    can_follow_target_to_left = (
        ghost.target_position.x < ghost.rect.x and ghost.allowed_turns[Direction.LEFT]
    )
    # The Pacman is right from the ghost and the ghost can go right
    can_follow_target_to_right = (
        ghost.target_position.x > ghost.rect.x and ghost.allowed_turns[Direction.RIGHT]
    )
    # The Pacman is above the ghost and the ghost can go up
    can_follow_target_up = (
        ghost.target_position.y < ghost.rect.y and ghost.allowed_turns[Direction.UP]
    )
    # The Pacman is below the ghost and the ghost can go down
    can_follow_target_down = (
        ghost.target_position.y > ghost.rect.y and ghost.allowed_turns[Direction.DOWN]
    )

    # Direction to the right is he default ghost's direction
    if ghost.direction == Direction.RIGHT:
        if can_follow_target_to_right:
            ghost.rect.centerx += ghost.speed
        elif not ghost.allowed_turns[Direction.RIGHT]:
            if can_follow_target_down:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            if can_follow_target_up:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            elif can_follow_target_to_left:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            # The Pacman is above/below and left from ghost and the ghost cannot go above/below and left,
            # so we try to move it any possible direction.
            elif ghost.allowed_turns[Direction.DOWN]:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            elif ghost.allowed_turns[Direction.UP]:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            elif ghost.allowed_turns[Direction.LEFT]:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
        # The ghost can go right, but the Pacman is not on the right side
        elif ghost.allowed_turns[Direction.RIGHT]:
            if can_follow_target_up:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            elif can_follow_target_up:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            # The Pacman is not up or down from the ghost
            # so it will go its default direction right
            else:
                ghost.rect.centerx += ghost.speed
    elif ghost.direction == Direction.LEFT:
        if can_follow_target_down:
            ghost.direction = Direction.DOWN
        elif can_follow_target_to_left:
            ghost.rect.centerx -= ghost.speed
        elif not ghost.allowed_turns[Direction.LEFT]:
            if can_follow_target_down:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            elif can_follow_target_up:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            elif can_follow_target_to_right:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
            # The Pacman is above/below and right from the ghost and the ghost cannot go above/below and right,
            # so we try to move it any possible direction.
            elif ghost.allowed_turns[Direction.DOWN]:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            elif ghost.allowed_turns[Direction.UP]:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            elif ghost.allowed_turns[Direction.RIGHT]:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
        # The ghost can go left, but the Pacman is not on the left side
        elif ghost.allowed_turns[Direction.LEFT]:
            if can_follow_target_down:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            elif can_follow_target_up:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            # The Pacman is not up or down from the ghost
            # so it will go its default direction left
            else:
                ghost.rect.centerx -= ghost.speed
    elif ghost.direction == Direction.UP:
        if can_follow_target_to_left:
            ghost.direction = Direction.LEFT
            ghost.rect.centerx -= ghost.speed
        elif can_follow_target_up:
            ghost.rect.centery -= ghost.speed
        elif not ghost.allowed_turns[Direction.UP]:
            if can_follow_target_to_right:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
            elif can_follow_target_to_left:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            elif can_follow_target_down:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            # The Pacman is left/right and up from the ghost and the ghost cannot go left/right and up,
            # so we try to move it any possible direction
            elif ghost.allowed_turns[Direction.LEFT]:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            elif ghost.allowed_turns[Direction.DOWN]:
                ghost.direction = Direction.DOWN
                ghost.rect.centery += ghost.speed
            elif ghost.allowed_turns[Direction.RIGHT]:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
        # The ghost can go up, but the Pacman is not on the upper side
        elif ghost.allowed_turns[Direction.UP]:
            if can_follow_target_to_right:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
            elif can_follow_target_to_left:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            # The Pacman is not left or right from the ghost
            # so it will go its default direction up
            else:
                ghost.rect.centery -= ghost.speed
    elif ghost.direction == Direction.DOWN:
        if can_follow_target_down:
            ghost.rect.centery += ghost.speed
        elif not ghost.allowed_turns[Direction.DOWN]:
            if can_follow_target_to_right:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
            elif can_follow_target_to_left:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            elif can_follow_target_up:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            # The Pacman is left/right and down from the ghost and the ghost cannot go left/right and down,
            # so we try to move it any possible direction
            if ghost.allowed_turns[Direction.UP]:
                ghost.direction = Direction.UP
                ghost.rect.centery -= ghost.speed
            elif ghost.allowed_turns[Direction.LEFT]:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            elif ghost.allowed_turns[Direction.RIGHT]:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
        # The ghost can go down, but the Pacman is not on the down side
        elif ghost.allowed_turns[Direction.DOWN]:
            if can_follow_target_to_right:
                ghost.direction = Direction.RIGHT
                ghost.rect.centerx += ghost.speed
            elif can_follow_target_to_left:
                ghost.direction = Direction.LEFT
                ghost.rect.centerx -= ghost.speed
            # The Pacman is not left or right from the ghost
            # so it will go its default direction down
            else:
                ghost.rect.centery += ghost.speed
