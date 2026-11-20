from Face_class import Face
import random


class RubiksCube:
    def __init__(self) -> None:
        
        self.faces = {
                    "U": Face("W"),
                    "D": Face("Y"),
                    "F": Face("G"),
                    "B": Face("B"),
                    "L": Face("O"),
                    "R": Face("R")
                    }
        
        self.adjacent = {
                    "U": [
                        ("F", "top", False),
                        ("L", "top", False),
                        ("B", "top", False),
                        ("R", "top", False)
                    ],

                    "D": [
                        ("F", "bottom", False),
                        ("R", "bottom", False),
                        ("B", "bottom", False),
                        ("L", "bottom", False)
                    ],

                    "F": [
                        ("U", "bottom", False),
                        ("R", "left", False),
                        ("D", "top", True),
                        ("L", "right", True)
                    ],

                    "B": [
                        ("U", "top", False),
                        ("L", "left", True),
                        ("D", "bottom", True),
                        ("R", "right", False)
                    ],

                    "L": [
                        ("U", "left", False),
                        ("F", "left", False),
                        ("D", "left", False),
                        ("B", "right", True)
                    ],

                    "R": [
                        ("U", "right", False),
                        ("B", "left", True),
                        ("D", "right", False),
                        ("F", "right", False)
                    ]
                    }
        
        
        
        self.move_history = []
        
    def is_solved(self) -> bool:
        for face in self.faces.values():
            if not face.is_solved():
                return False

        return True
    
    def get_edge(self, face : str, edge : str, reverse=False):

        grid = self.faces[face].grid

        if edge == "top":
            values = grid[0][:]

        elif edge == "bottom":
            values = grid[2][:]

        elif edge == "left":
            values = [row[0] for row in grid]

        elif edge == "right":
            values = [row[2] for row in grid]

        else:
            raise ValueError("Invalid edge")

        if reverse:
            values.reverse()

        return values
            
    
    def set_edge(self, face : str, edge : str, values : "str", reverse=False):

        grid = self.faces[face].grid
        values = list(values)

        if reverse:
            values.reverse()

        if edge == "top":
            grid[0] = values

        elif edge == "bottom":
            grid[2] = values

        elif edge == "left":
            for i in range(3):
                grid[i][0] = values[i]

        elif edge == "right":
            for i in range(3):
                grid[i][2] = values[i]

        else:
            raise ValueError("Invalid edge")
        
    
    def rotate(self, face, direction) -> None:    
       
        # Get the four affected edges
        neighbours = self.adjacent[face]

        # Save their current values
        edges = [
            self.get_edge(f, e, reverse)
            for f, e, reverse in neighbours
        ]

        # Rotate the selected face
        if direction == "clockwise":
            self.faces[face].rotate_clockwise()
            shift = -1

        elif direction == "anticlockwise":
            self.faces[face].rotate_anti_clockwise()
            shift = 1

        else:
            raise ValueError("Invalid direction")

        for i in range(4):
            f, e, reverse = neighbours[i]

            self.set_edge(
                f,
                e,
                edges[(i + shift) % 4],
                reverse
            )

        self.move_history.append((face, direction))
        
    
    
    def scrambler(self):
        
        number_shuffles = random.randint(6,6)
        for i in range(number_shuffles):
            selected_face = random.choice(list(self.faces.keys()))
            random_rotation = random.choice(["clockwise", "anticlockwise"])
            self.rotate(selected_face, random_rotation)





