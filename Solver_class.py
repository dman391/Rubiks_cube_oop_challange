from RubiksCube_class import RubiksCube
import queue
import copy



#use superclass
class Solver(RubiksCube):
    # Moves used to REACH G1, G2, G3, and G4 respectively.
    G1_MOVES = tuple(face + suffix for face in 'UDFBLR' for suffix in ('', "'", '2'))
    G2_MOVES = ('U', "U'", 'U2', 'D', "D'", 'D2',
                'L', "L'", 'L2', 'R', "R'", 'R2', 'F2', 'B2')
    G3_MOVES = ('U', "U'", 'U2', 'D', "D'", 'D2', 'L2', 'R2', 'F2', 'B2')
    G4_MOVES = ('U2', 'D2', 'F2', 'B2', 'L2', 'R2')

    # Ordered sticker positions. Corner order is cyclic, with U/D first.
    EDGE_POSITIONS = (
        (('U', 2, 1), ('F', 0, 1)), (('U', 0, 1), ('B', 0, 1)),
        (('U', 1, 0), ('L', 0, 1)), (('U', 1, 2), ('R', 0, 1)),
        (('D', 0, 1), ('F', 2, 1)), (('D', 2, 1), ('B', 2, 1)),
        (('D', 1, 0), ('L', 2, 1)), (('D', 1, 2), ('R', 2, 1)),
        (('F', 1, 2), ('R', 1, 0)), (('F', 1, 0), ('L', 1, 2)),
        (('B', 1, 0), ('R', 1, 2)), (('B', 1, 2), ('L', 1, 0)),
    )
    CORNER_POSITIONS = (
        (('U', 2, 2), ('R', 0, 0), ('F', 0, 2)),  # URF
        (('U', 2, 0), ('F', 0, 0), ('L', 0, 2)),  # UFL
        (('U', 0, 0), ('L', 0, 0), ('B', 0, 2)),  # ULB
        (('U', 0, 2), ('B', 0, 0), ('R', 0, 2)),  # UBR
        (('D', 0, 2), ('F', 2, 2), ('R', 2, 0)),  # DFR
        (('D', 0, 0), ('L', 2, 2), ('F', 2, 0)),  # DLF
        (('D', 2, 0), ('B', 2, 2), ('L', 2, 0)),  # DBL
        (('D', 2, 2), ('R', 2, 2), ('B', 2, 0)),  # DRB
    )
    _half_turn_corners = None

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

            # Check the target subgroup for the current phase.
            if goal_fn(current):
                return self.reconstruct_path(parent, current_id)

            for move in allowed_moves:
                next_cube = copy.deepcopy(current)

                self.apply_move(next_cube, move)

                # Track only the coordinates needed by this phase.
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


    @staticmethod
    def apply_move(cube: RubiksCube, move: str) -> None:
        """Apply standard notation such as U, R', or F2 to a cube."""
        if move not in Solver.G1_MOVES:
            raise ValueError(f'Invalid move: {move}')
        direction = 'anticlockwise' if move.endswith("'") else 'clockwise'
        for _ in range(2 if move.endswith('2') else 1):
            cube.rotate(move[0], direction)

    def apply_moves(self, moves) -> None:
        """Apply a returned BFS path to this solver before the next phase."""
        for move in moves:
            self.apply_move(self, move)

    def _piece_permutation(self, cube, positions) -> tuple:
        """Return each piece's home index, using centres to identify colours."""
        homes = {
            frozenset(cube.faces[face].grid[1][1] for face, _, _ in slot): i
            for i, slot in enumerate(positions)
        }
        return tuple(homes[frozenset(cube.faces[face].grid[row][col]
                                     for face, row, col in slot)]
                     for slot in positions)

    def get_corner_orientation(self, cube: RubiksCube) -> tuple:
        ud = {cube.faces[face].grid[1][1] for face in 'UD'}
        return tuple(next(i for i, (face, row, col) in enumerate(slot)
                          if cube.faces[face].grid[row][col] in ud)
                     for slot in self.CORNER_POSITIONS)

    def get_g2_state(self, cube: RubiksCube) -> tuple:
        """Phase 2 key: corner twists and positions of the four E-slice edges.

        Use only after reaching G1, with G2_MOVES.
        """
        edges = self._piece_permutation(cube, self.EDGE_POSITIONS)
        return self.get_corner_orientation(cube), tuple(piece >= 8 for piece in edges)

    def is_g2(self, cube: RubiksCube) -> bool:
        twists, slice_edges = self.get_g2_state(cube)
        return (self.is_g1(cube) and not any(twists)
                and slice_edges == (False,) * 8 + (True,) * 4)

    @staticmethod
    def permutation_parity(permutation) -> int:
        """0 for an even permutation; 1 for an odd permutation."""
        return sum(permutation[i] > permutation[j]
                   for i in range(len(permutation))
                   for j in range(i + 1, len(permutation))) % 2

    def _get_half_turn_corners(self) -> tuple:
        """Build the 96 corner permutations reachable using only half turns."""
        if Solver._half_turn_corners is None:
            generators = []
            for move in self.G4_MOVES:
                cube = RubiksCube()
                self.apply_move(cube, move)
                generators.append(self._piece_permutation(cube, self.CORNER_POSITIONS))
            identity = tuple(range(8))
            seen, pending = {identity}, [identity]
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
        """Phase 3 key; use only in G2 with G3_MOVES.

        Canonicalising over all 96 half-turn corner permutations includes
        the tetrad-twist constraint, not just tetrad membership and parity.
        """
        corners = self._piece_permutation(cube, self.CORNER_POSITIONS)
        edges = self._piece_permutation(cube, self.EDGE_POSITIONS)
        corner_coset = min(tuple(relabel[piece] for piece in corners)
                           for relabel in self._get_half_turn_corners())
        # UF/UB/DF/DB, UL/UR/DL/DR, and FR/FL/BR/BL are the three orbits.
        orbit = (0, 0, 1, 1, 0, 0, 1, 1, 2, 2, 2, 2)
        return corner_coset, tuple(orbit[piece] for piece in edges), self.permutation_parity(edges)

    def is_g3(self, cube: RubiksCube) -> bool:
        if not self.is_g2(cube):
            return False
        corners, edge_orbits, parity = self.get_g3_state(cube)
        return (corners == tuple(range(8)) and parity == 0
                and edge_orbits == (0, 0, 1, 1, 0, 0, 1, 1, 2, 2, 2, 2))

    def get_g4_state(self, cube: RubiksCube) -> tuple:
        """Phase 4 needs the complete state, since the target is solved."""
        return self.get_state_id(cube)

    def is_g4(self, cube: RubiksCube) -> bool:
        return cube.is_solved()

if __name__ == '__main__':
    cube = RubiksCube()
    cube.scrambler()
    v1 = Solver()
    print(v1.is_g1(cube))





