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
    
    def is_solved(self) -> bool:
        return all(face.is_solved() for face in self.faces.values())


