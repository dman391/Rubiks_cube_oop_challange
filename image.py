import copy
import math
import queue


from vpython import box, canvas, color, rate, vector
from Solver_class import Solver


class CubeViewer:
    def __init__(self):
        self.scene = canvas(
            title="Rubik's Cube Solver",
            width=1000,
            height=700,
            background=vector(0.08, 0.09, 0.12),
        )
        self.scene.forward = vector(-1, -0.7, -1)
        self.scene.range = 5

        self.cube = Solver()
        self.objects = []

        # Face normal, direction to the right, direction upwards.
        self.faces = {
            "F": (vector(0, 0, 1), vector(1, 0, 0), vector(0, 1, 0)),
            "B": (vector(0, 0, -1), vector(-1, 0, 0), vector(0, 1, 0)),
            "U": (vector(0, 1, 0), vector(1, 0, 0), vector(0, 0, -1)),
            "D": (vector(0, -1, 0), vector(1, 0, 0), vector(0, 0, 1)),
            "R": (vector(1, 0, 0), vector(0, 0, -1), vector(0, 1, 0)),
            "L": (vector(-1, 0, 0), vector(0, 0, 1), vector(0, 1, 0)),
        }

        self.colours = {
            "W": color.white,
            "Y": color.yellow,
            "G": vector(0, 0.7, 0.15),
            "B": vector(0.1, 0.3, 1),
            "O": vector(1, 0.45, 0),
            "R": color.red,
        }

        self.build_cube()

    def build_cube(self):
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                for z in (-1, 0, 1):
                    if (x, y, z) == (0, 0, 0):
                        continue

                    body = box(
                        pos=vector(x, y, z),
                        size=vector(0.96, 0.96, 0.96),
                        color=vector(0.025, 0.025, 0.025),
                    )
                    self.objects.append(body)

        # Nine coloured stickers on each outer face.
        for face, (normal, right, upwards) in self.faces.items():
            for row in range(3):
                for column in range(3):
                    position = (
                        normal * 1.49
                        + right * (column - 1)
                        + upwards * (1 - row)
                    )

                    # Make the sticker thin along its face normal.
                    size = vector(
                        0.025 if normal.x else 0.86,
                        0.025 if normal.y else 0.86,
                        0.025 if normal.z else 0.86,
                    )

                    sticker_colour = self.cube.faces[face].grid[row][column]

                    sticker = box(
                        pos=position,
                        size=size,
                        color=self.colours[sticker_colour],
                    )
                    self.objects.append(sticker)

    def animate_move(self, move):
        normal = self.faces[move[0]][0]

        # Select everything belonging to the moving layer.
        layer = [
            obj for obj in self.objects
            if obj.pos.dot(normal) > 0.5
        ]

        # Clockwise when looking directly at the selected face.
        angle = -math.pi / 2

        if move.endswith("'"):
            angle = -angle
        elif move.endswith("2"):
            angle *= 2

        frames = 36 if move.endswith("2") else 18

        for _ in range(frames):
            rate(10)

            for obj in layer:
                obj.rotate(
                    angle=angle / frames,
                    axis=normal,
                    origin=vector(0, 0, 0),
                )

        self.cube.apply_moves([move])

    def run(self):
        scrambled = Solver()
        scrambled.scrambler()

        scramble = [
            face + ("'" if direction == "anticlockwise" else "")
            for face, direction in scrambled.move_history
        ]


        self.scene.caption = "Scrambling: " + " ".join(scramble)

        for move in scramble:
            self.animate_move(move)

        # Solve a separate copy so the displayed cube stays scrambled.
        worker_cube = copy.deepcopy(scrambled)

        self.scene.caption = "Finding a solution..."
        rate(30)
        
       
        solution = worker_cube.solve()

        for move in solution:
            self.scene.caption = f"Applying: {move}"
            self.animate_move(move)

        self.scene.caption = (
            "Solved!" if self.cube.is_solved() else "Failed to solve")


        while True:
            rate(30)

