from Face_class import Face



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
        
        for key in list(self.faces.keys):
            if self.faces[key].is_solved == False:
                  return False
            return True

    
    def get_edge(self, face, edge, reverse=False):

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
            
    
    def set_edge(self, face, edge, values, reverse=False):

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
        
    
    #def rotate(face, direction) -> None:    
    
    #apply_moves(moves)
    #get_state()

#class Scrambler

#class Solve


my_cube = RubiksCube()
my_cube.get_edge("U","top")