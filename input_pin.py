from typing import Tuple
import subprocess

class InputPin:

    def __init__(self, pin:Tuple[int, int]) -> None:
        self.pin_group, self.pin_number = pin

    def get(self) -> bool:
        read_result = subprocess.run(
            ['gpioget', f'{self.pin_group}', f'{self.pin_number}'],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text = True,
        )

        read_output = read_result.stdout
        read_error = read_result.stderr

        if read_error:
            raise ValueError(f'GPIO {self.pin_group} {self.pin_number} read error:\n{read_error}')

        return read_output == '1'