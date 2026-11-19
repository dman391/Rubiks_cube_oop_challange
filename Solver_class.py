from RubiksCube_class import RubiksCube
import queue



#use superclass
class Solver(RubiksCube):
    def __init__(self) -> None:
        super().__init__()

    def bfs(self, allowed_moves):
        queue = queue.Queue()
        visted = []

        loop = True
        While loop:
            queue.put(self.faces)

            current = queue.get()
        
            #check if been visted    
            if current not in visted:
                visted.append(current)
            else:
                current = queue.get()

            #check if solved
            if current.is_solved():
                print("cube solved")
                loop = False







