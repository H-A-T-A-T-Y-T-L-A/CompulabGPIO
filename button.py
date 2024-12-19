import time
from typing import MutableSequence, Iterable, Tuple, Callable, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from . import InputPin, Gpio

class Button:

    def __init__(self, pin:'InputPin', gpio:'Gpio') -> None:
        self.pin = pin
        gpio.register_scan(pin)
        pin.on_change = self.change
        self._on_down:Callable[[], None] = lambda: None
        self._on_up:Callable[[], None] = lambda: None
        self._on_click:Callable[[], None] = lambda: None
        self._on_long_click:MutableSequence[Tuple[Callable[[], None], float]] = []
        self._click_start_time:Optional[float] = 0

    @property
    def _min_long_click(self) -> float:
        return min(t for _, t in self._on_long_click)

    @property
    def _long_click_intervals(self) -> Iterable[Tuple[Callable[[], None], float, float]]:
        max_time = float('inf')
        for func, min_time in sorted(
            self._on_long_click,
            key = lambda x: x[1],
            reverse = True
        ):
            yield func, min_time, max_time
            max_time = min_time

    def on_down(self, func:Callable[[], None]) -> None:
        self._on_down = func

    def on_up(self, func:Callable[[], None]) -> None:
        self._on_up = func

    def on_click(self, func:Callable[[], None]) -> None:
        self._on_click = func

    def on_long_click(self, func:Callable[[], None], hold_seconds:float) -> None:
        self._on_long_click.append((func, hold_seconds))

    def change(self) -> None:
        current_time = time.time()
        hold_time = (current_time - self._click_start_time) if self._click_start_time is not None else 0
        # if the button has just been pressed
        if self.pin.state:
            self._on_down()
            self._click_start_time = time.time()
        # if the button has been released
        if not self.pin.state:
            self._on_up()
        # if the button has been pressed and released faster than any long click setting
        if not self.pin.state and hold_time < self._min_long_click:
            self._on_click()
        # trigger the appropriate click, depending on the time the button has been held
        for func, min_time, max_time in self._long_click_intervals:
            if min_time <= hold_time < max_time:
                func()
                break
