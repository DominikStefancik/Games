from .constants import TimerDuration
from .timer import Timer


class TimersManager:
    def __init__(self):
        self.startup_timer = Timer(
            duration=TimerDuration.STARTUP_UP.value, repeat=False, autostart=True
        )
        self.power_up_timer = Timer(TimerDuration.POWER_UP.value)
        self.ghost_resurrection_timer = Timer(TimerDuration.GHOST_RESURRECTION.value)

    def update(self):
        self.startup_timer.update()
        self.power_up_timer.update()
        self.ghost_resurrection_timer.update()


TIMERS_MANAGER = TimersManager()


def get_timers_manager():
    return TIMERS_MANAGER
