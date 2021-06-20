from typing import List, Final, Dict, ContextManager
import turtle
import contextlib
from random import randint


FASTEST_ANIMATION: Final[int] = 0
FULL_SCREEN_WIDTH: Final[float] = 1.0
FULL_SCREEN_HEIGHT: Final[float] = 1.0


@contextlib.contextmanager
def use_turtle(
        title: str,
        speed: int = FASTEST_ANIMATION,
        width: float = FULL_SCREEN_WIDTH,
        height: float = FULL_SCREEN_HEIGHT
) -> ContextManager[turtle.Turtle]:
    turtle_obj = turtle.Turtle()
    turtle_obj.speed(speed=speed)

    screen = turtle.Screen()
    screen.setup(width=width, height=height, startx=0, starty=0)
    # Set the starting position of the pen to the bottom left position.
    screen.setworldcoordinates(
        llx=-1,
        lly=-1,
        urx=screen.window_width(),
        ury=screen.window_height()
    )

    screen.title(titlestring=title)
    screen.delay(delay=0)
    screen.colormode(cmode=255)

    yield turtle_obj

    turtle.done()


def draw_hilbert_curve(level: int):
    alphabet: Final[List[str]] = ["A", "B"]
    angle: Final[int] = 90
    distance: Final[int] = 20
    axiom: Final[str] = "A"
    production_rules: Dict[str, List[str]] = {
        "A": ["+", "B", "F", "-", "A", "F", "A", "-", "F", "B", "+"],
        "B": ["-", "A", "F", "+", "B", "F", "B", "+", "F", "A", "-"]
    }

    def change_color_to_random(turtle_obj: turtle.Turtle):
        turtle_obj.color(*[randint(a=0, b=255) for i in range(3)])

    def draw_rule(turtle_obj: turtle.Turtle, rule: str, level: int):
        if level == 0:
            return

        commands: List[str] = production_rules.get(rule)

        for command in commands:
            change_color_to_random(turtle_obj=turtle_obj)

            if command in alphabet:
                draw_rule(turtle_obj=turtle_obj, rule=command, level=level - 1)
            elif command == "F":
                turtle_obj.forward(distance=distance)
            elif command == "+":
                turtle_obj.left(angle=angle)
            elif command == "-":
                turtle_obj.right(angle=angle)

    with use_turtle(title="Hilbert Curve") as turtle_obj:
        turtle_obj.pensize(width=5)
        draw_rule(turtle_obj=turtle_obj, rule=axiom, level=level)


def main():
    draw_hilbert_curve(level=5)


if __name__ == "__main__":
    main()
