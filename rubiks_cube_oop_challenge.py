class Face:
    def __init__(self, colour : str) -> None:
            self.colour = colour 
            self.grid = [[colour] * 3 for _ in range(3)]
            
    def rotate_anti_clockwise(self) -> None:
        
        row, column = len(self.grid), len(self.grid)
        rotated_face = [[None] * row for i in range(column)]
        
        for i in range(column):
                for j in range(row-1,-1,-1):
                        rotated_face[column-i-1][j] = self.grid[j][i]
        
        self.grid = rotated_face


    def rotate_clockwise(self) -> None:
            
            row, column = len(self.grid), len(self.grid)
            rotated_face = [[None] * row for i in range(column)]
            
            for i in range(column):
                    for j in range(column):
                            rotated_face[j][column-i-1] = self.grid[i][j]
            
            self.grid = rotated_face
    
    def is_solved(self):
        
        middle = self.grid[1][1]
        all_elements = []
        
        for i in self.grid:
            for j in i:
                all_elements.append(j == middle)
        return all(all_elements)
        

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
        self.move_history = []

    def is_solved(self) -> bool:
        
        for key in list(self.faces.keys):
            if self.faces[key].is_solved == False:
                  return False
            return True

    def rotate(face, direction) -> None:    
    
    #apply_moves(moves)
    #get_state()

#class Scrambler

#class Solve

