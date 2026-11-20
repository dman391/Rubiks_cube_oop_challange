from RubiksCube_class import RubiksCube
import queue
import copy

#use superclass
class Solver(RubiksCube):
    def __init__(self) -> None:
        super().__init__()

    def get_state_id(self, cube: RubiksCube):
        
        return tuple(
            (side, str(cube.faces[side].grid)) 
            for side in ['U', 'D', 'F', 'B', 'L', 'R']
        )

    def reconstruct_path(self, parent: dict, end_id):
        
        path = []
        curr = end_id
        while parent[curr] is not None:
            prev_id, move = parent[curr]
            path.append(move)
            curr = prev_id
        path.reverse()
        return path

    def bfs(self, allowed_moves, state_fn, goal_fn):
        q = queue.Queue()
        start_cube = copy.deepcopy(self)
        start_id = state_fn(start_cube)

        q.put(start_cube)
        visited = {start_id}
        parent = {start_id: None}

        while not q.empty():
            current = q.get()
            current_id = state_fn(current)

            # 1. Check if we reached G1 (all 12 edges Good)
            if goal_fn(current):
                return self.reconstruct_path(parent, current_id)

            for move in allowed_moves:
                next_cube = copy.deepcopy(current)
                
                if "'" in move:
                    next_cube.rotate(move[0], "anticlockwise")
                elif "2" in move:
                    next_cube.rotate(move[0], "clockwise")
                    next_cube.rotate(move[0], "clockwise")
                else:
                    next_cube.rotate(move, "clockwise")

                next_id = state_fn(next_cube)

                if next_id not in visited:
                    visited.add(next_id)
                    parent[next_id] = (current_id, move)
                    q.put(next_cube)

        return None
                    
    def get_g1_state(self, cube: RubiksCube) -> tuple:
        f = cube.faces
        ud_colors = {f['U'].grid[1][1], f['D'].grid[1][1]}  
        fb_colors = {f['F'].grid[1][1], f['B'].grid[1][1]}  


        edges = [
            (f['U'].grid[2][1], f['F'].grid[0][1]),  # UF
            (f['U'].grid[0][1], f['B'].grid[0][1]),  # UB
            (f['U'].grid[1][0], f['L'].grid[0][1]),  # UL
            (f['U'].grid[1][2], f['R'].grid[0][1]),  # UR

            (f['D'].grid[0][1], f['F'].grid[2][1]),  # DF
            (f['D'].grid[2][1], f['B'].grid[2][1]),  # DB
            (f['D'].grid[1][0], f['L'].grid[2][1]),  # DL
            (f['D'].grid[1][2], f['R'].grid[2][1]),  # DR

            (f['F'].grid[1][2], f['R'].grid[1][0]),  # FR
            (f['F'].grid[1][0], f['L'].grid[1][2]),  # FL
            (f['B'].grid[1][0], f['R'].grid[1][2]),  # BR
            (f['B'].grid[1][2], f['L'].grid[1][0]),  # BL
        ]

        return tuple(
            (primary in ud_colors) or (primary in fb_colors and secondary not in ud_colors)
            for primary, secondary in edges
        )

    def is_g1(self, cube: RubiksCube) -> bool:
        return all(self.get_g1_state(cube))    

        
        # Allowed moves for reaching each group.
    G1_MOVES = tuple(
        face + suffix
        for face in "UDFBLR"
        for suffix in ("", "'", "2")
    )

    G2_MOVES = (
        "U", "U'", "U2", "D", "D'", "D2",
        "L", "L'", "L2", "R", "R'", "R2",
        "F2", "B2",
    )

    G3_MOVES = (
        "U", "U'", "U2", "D", "D'", "D2",
        "L2", "R2", "F2", "B2",
    )

    G4_MOVES = ("U2", "D2", "F2", "B2", "L2", "R2")

    # Each position contains (face, row, column) coordinates.
    EDGE_POSITIONS = (
        (("U", 2, 1), ("F", 0, 1)),  # UF
        (("U", 0, 1), ("B", 0, 1)),  # UB
        (("U", 1, 0), ("L", 0, 1)),  # UL
        (("U", 1, 2), ("R", 0, 1)),  # UR
        (("D", 0, 1), ("F", 2, 1)),  # DF
        (("D", 2, 1), ("B", 2, 1)),  # DB
        (("D", 1, 0), ("L", 2, 1)),  # DL
        (("D", 1, 2), ("R", 2, 1)),  # DR
        (("F", 1, 2), ("R", 1, 0)),  # FR
        (("F", 1, 0), ("L", 1, 2)),  # FL
        (("B", 1, 0), ("R", 1, 2)),  # BR
        (("B", 1, 2), ("L", 1, 0)),  # BL
    )

    CORNER_POSITIONS = (
        (("U", 2, 2), ("R", 0, 0), ("F", 0, 2)),  # URF
        (("U", 2, 0), ("F", 0, 0), ("L", 0, 2)),  # UFL
        (("U", 0, 0), ("L", 0, 0), ("B", 0, 2)),  # ULB
        (("U", 0, 2), ("B", 0, 0), ("R", 0, 2)),  # UBR
        (("D", 0, 2), ("F", 2, 2), ("R", 2, 0)),  # DFR
        (("D", 0, 0), ("L", 2, 2), ("F", 2, 0)),  # DLF
        (("D", 2, 0), ("B", 2, 2), ("L", 2, 0)),  # DBL
        (("D", 2, 2), ("R", 2, 2), ("B", 2, 0)),  # DRB
    )

    _half_turn_corners = None

    @staticmethod
    def apply_move(cube: RubiksCube, move: str) -> None:
        """Apply a move such as U, R', or F2."""
        if move not in Solver.G1_MOVES:
            raise ValueError(f"Invalid move: {move}")

        direction = (
            "anticlockwise" if move.endswith("'") else "clockwise"
        )
        turns = 2 if move.endswith("2") else 1

        for _ in range(turns):
            cube.rotate(move[0], direction)

    def apply_moves(self, moves) -> None:
        """Apply a sequence of moves to this solver's cube."""
        for move in moves:
            self.apply_move(self, move)

    def _piece_permutation(self, cube, positions) -> tuple:
        """Identify which piece occupies each position.

        A piece's number is the index of its position when solved.
        Centre colours tell us which colours belong on each face.
        """
        homes = {}

        for index, position in enumerate(positions):
            colours = frozenset(
                cube.faces[face].grid[1][1]
                for face, _, _ in position
            )
            homes[colours] = index

        permutation = []

        for position in positions:
            colours = frozenset(
                cube.faces[face].grid[row][column]
                for face, row, column in position
            )
            permutation.append(homes[colours])

        return tuple(permutation)

    def get_corner_orientation(self, cube: RubiksCube) -> tuple:
        """Return eight corner twists: 0, 1, or 2."""
        ud_colours = {
            cube.faces["U"].grid[1][1],
            cube.faces["D"].grid[1][1],
        }

        orientations = []

        for position in self.CORNER_POSITIONS:
            for index, (face, row, column) in enumerate(position):
                if cube.faces[face].grid[row][column] in ud_colours:
                    orientations.append(index)
                    break
            else:
                raise ValueError("Corner has no U/D colour")

        return tuple(orientations)

    def get_g2_state(self, cube: RubiksCube) -> tuple:
        """Phase 2 key: corner twists and middle-slice edges.

        Use after reaching G1, with G2_MOVES.
        """
        edges = self._piece_permutation(
            cube, self.EDGE_POSITIONS
        )

        # Pieces 8–11 are FR, FL, BR, BL.
        middle_slice_edges = tuple(piece >= 8 for piece in edges)

        return (
            self.get_corner_orientation(cube),
            middle_slice_edges,
        )

    def is_g2(self, cube: RubiksCube) -> bool:
        twists, middle_slice_edges = self.get_g2_state(cube)

        return (
            self.is_g1(cube)
            and all(twist == 0 for twist in twists)
            and middle_slice_edges == (False,) * 8 + (True,) * 4
        )

    @staticmethod
    def permutation_parity(permutation) -> int:
        """Return 0 for even parity or 1 for odd parity."""
        inversions = 0

        for i in range(len(permutation)):
            for j in range(i + 1, len(permutation)):
                if permutation[i] > permutation[j]:
                    inversions += 1

        return inversions % 2

    def _get_half_turn_corners(self) -> tuple:
        """Find the 96 corner permutations allowed in G3.

        Generate them once using half turns from the solved state.
        """
        if Solver._half_turn_corners is not None:
            return Solver._half_turn_corners

        generators = []

        for move in self.G4_MOVES:
            cube = RubiksCube()
            self.apply_move(cube, move)

            generators.append(
                self._piece_permutation(cube, self.CORNER_POSITIONS)
            )

        identity = tuple(range(8))
        seen = {identity}
        pending = [identity]

        while pending:
            current = pending.pop()

            for generator in generators:
                successor = tuple(current[i] for i in generator)

                if successor not in seen:
                    seen.add(successor)
                    pending.append(successor)

        Solver._half_turn_corners = tuple(sorted(seen))
        return Solver._half_turn_corners

    def get_g3_state(self, cube: RubiksCube) -> tuple:
        """Phase 3 key: corner arrangement, edge slices, and parity.

        Use after reaching G2, with G3_MOVES.
        """
        corners = self._piece_permutation(
            cube, self.CORNER_POSITIONS
        )
        edges = self._piece_permutation(
            cube, self.EDGE_POSITIONS
        )

        corner_coset = min(
            tuple(relabel[piece] for piece in corners)
            for relabel in self._get_half_turn_corners()
        )

        edge_orbit = (0, 0, 1, 1, 0, 0, 1, 1, 2, 2, 2, 2)

        return (
            corner_coset,
            tuple(edge_orbit[piece] for piece in edges),
            self.permutation_parity(edges),
        )

    def is_g3(self, cube: RubiksCube) -> bool:
        if not self.is_g2(cube):
            return False

        corners, edge_orbits, parity = self.get_g3_state(cube)

        return (
            corners == tuple(range(8))
            and edge_orbits == (0, 0, 1, 1, 0, 0, 1, 1, 2, 2, 2, 2)
            and parity == 0
        )

    def get_g4_state(self, cube: RubiksCube) -> tuple:
        """Phase 4 tracks the complete cube state."""
        return self.get_state_id(cube)

    def is_g4(self, cube: RubiksCube) -> bool:
        return cube.is_solved()


    def solve(self):

        phases = [
            (self.G1_MOVES, self.get_g1_state, self.is_g1),
            (self.G2_MOVES, self.get_g2_state, self.is_g2),
            (self.G3_MOVES, self.get_g3_state, self.is_g3),
            (self.G4_MOVES, self.get_g4_state, self.is_g4),
        ]

        solution = []

        for phase in phases:
            info = self.bfs(phase[0], phase[1], phase[2])
            if info != None:
                self.apply_moves(info)
                solution.extend(info)      
        return solution



"""
solver = Solver()
solver.scrambler()

solution = solver.solve()

print("Solution:", solution)
assert solver.is_solved(), "Failed: cube is not solved!"
print("Test passed!")
"""