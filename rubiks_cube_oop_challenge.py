class Face:
    def __init__(self, colour : str, grid : list) -> None:
            self.colour = colour 
            self.grid = grid

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

f1 = Face("white", [[1,2,3],[4,5,6],[7,8,9]])
f1.rotate_clockwise()
#f1.rotate_anti_clockwise()

print(f1.is_solved())
