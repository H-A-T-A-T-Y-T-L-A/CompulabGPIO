from typing import Tuple
import subprocess

class Pin:

    def __init__(self, pin:Tuple[int, int]) -> None:
        self.pin_group, self.pin_number = pin

    def set(self, value:bool) -> None:
        read_result = subprocess.run(
            ['gpioget', f'{self.pin_group}', f'{self.pin_number}={int(value)}'],
            stdout = subprocess.DEVNULL,
            stderr = subprocess.PIPE,
            text = True,
        )

        read_error = read_result.stderr

        if read_error:
            raise ValueError(f'GPIO {self.pin_group} {self.pin_number} write error:\n{read_error}')