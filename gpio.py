from typing import MutableSequence, MutableMapping, Callable, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from . import InputPin, OutputPin, Button

IN0 = 2, 0
IN1 = 2, 1
IN2 = 2, 6
IN3 = 2, 7
OUT0 = 2, 8
OUT1 = 2, 9
OUT2 = 5, 9
OUT3 = 5, 10

class Gpio:

    def __init__(self):
        from . import InputPin, OutputPin
        self.in0 = InputPin(IN0)
        self.in1 = InputPin(IN1)
        self.in2 = InputPin(IN2)
        self.in3 = InputPin(IN3)
        self.inputs = [self.in0, self.in1, self.in2, self.in3, self.in4]

        self.out0 = OutputPin(OUT0)
        self.out1 = OutputPin(OUT1)
        self.out2 = OutputPin(OUT2)
        self.out3 = OutputPin(OUT3)
        self.inputs = [self.in0, self.in1, self.in2, self.in3, self.in4]

        self.inputs_to_scan:MutableSequence[InputPin] = []

    def _register_scan(self, pin:'InputPin') -> None:
        if pin not in self.inputs_to_scan:
            self.inputs_to_scan.append(pin)

    def do_scan(self) -> None:
        for pin in self.inputs_to_scan:
            pin.get()

    def button(self, pin:Union['InputPin', int]) -> 'Button':
        from . import Button
        if isinstance(pin, int):
            pin = self.inputs[pin]
        return Button(pin, self)
