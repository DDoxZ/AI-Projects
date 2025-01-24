# Projeto 1 IIA 2024/2025
# Grupo 1
# 59886 - Pedro Silva
# 60447 - Diogo Lopes

from searchPlus import *

linha1= "  ##### \n"
linha2= "###...# \n"
linha3= "#o@$..# \n"
linha4= "###.$o# \n"
linha5= "#o##..# \n"
linha6= "#.#...##\n"
linha7= "#$.....#\n"
linha8= "#......#\n"
linha9= "########\n"
mundoStandard=linha1+linha2+linha3+linha4+linha5+linha6+linha7+linha8+linha9

class SokobanState:
    """Represents the state in Sokoban with the Sokoban and the boxes positions."""

    def __init__(self, position, boxes):
        """Initializes the SokobanState with the Sokoban and the boxes positions."""
        self.position = position  # (row, col) tuple
        self.boxes = tuple(boxes)  # Tuple of box positions, each (row, col)

    def __eq__(self, other):
        """States are the same if the Sokoban's position and the boxes positions are the same."""
        # return isinstance(other, SokobanState) and self.position == other.position and self.boxes == other.boxes
        # doesnt work if the tuple is in a different order
        return isinstance(other, SokobanState) and self.position == other.position and set(self.boxes) == set(other.boxes)

    def __hash__(self):
        """Hashes the state to ensure it can be used in sets and as dictionary keys."""
        return hash((self.position, self.boxes))

    def __repr__(self):
        """Returns a string representation of the state for debugging purposes."""
        return f"SokobanState(position={self.position}, boxes={self.boxes})"

class Sokoban(Problem):
    def __init__(self, situacaoInicial=mundoStandard):
        # Parses the maze from the string and store the information that does not change between states.
        self.height, self.width, self.goals, self.walls, self.free, sokoban, boxes = self.parse_maze(situacaoInicial)
        
        # Create and store the initial state.
        self.initial = SokobanState(sokoban, boxes)
        
    def parse_maze(self, maze):
        """Auxiliary method to parse the maze string and return the Sokoban game data structures."""

        lines = maze.splitlines()
        height = len(lines)
        width = max(len(line) for line in lines)
        walls = set()
        free = set()
        boxes = set()
        goals = set()
        sokoban = None
        # Sets to ensure that there are no duplicate positions.

        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                pos = (row, col)
                if char == '#':
                    walls.add(pos)

                elif char == 'o':
                    goals.add(pos)
                    free.add(pos)

                elif char == '@':
                    sokoban = pos
                    free.add(pos)

                elif char == '+':
                    sokoban = pos
                    goals.add(pos)
                    free.add(pos)

                elif char == '$':
                    boxes.add(pos)
                    free.add(pos)

                elif char == '*':
                    boxes.add(pos)
                    goals.add(pos)

                elif char == '.':
                    free.add(pos)

        return height, width, goals, walls, free, sokoban, boxes
   
    def actions(self, state):
        """Returns the list of actions that can be used in the given state."""

        base_actions = ['N', 'W', 'E', 'S']

        actions = []
        for action in base_actions:
            if self.is_valid_move(state, action):
                actions.append(action)

        return actions
        
    def is_valid_move(self, state, action):
        """Auxiliary method to check if a move is valid (including the corner restrictions)."""

        row, col = state.position
        row_offset, col_offset = self.get_offset(action)
        new_position = (row + row_offset, col + col_offset)

        # Check if the new position is a wall.
        if new_position in self.walls:
            return False

        # Check if the new position is a box.
        if new_position in state.boxes:
            new_box_position = (row + 2 * row_offset, col + 2 * col_offset)

            # Check if the new box position is blocked by a wall or another box.
            if new_box_position in self.walls or new_box_position in state.boxes:
                return False
            
            # Allow pushing through tunnels if the next position after the box is empty
            next_position = (row + 3 * row_offset, col + 3 * col_offset)
            if (next_position not in self.free or next_position in state.boxes) and (self.is_corner(new_box_position, action) and new_box_position not in self.goals):
                return False  # Block the move if the box is pushed into a corner
        
        return True

    def get_offset(self, action):
        """Returns the movement offset (row, col) for the given action."""

        return {
            'N': (-1, 0),
            'W': (0, -1),
            'E': (0, 1),
            'S': (1, 0)
        }[action]

    def is_corner(self, pos, action):
        """Auxiliary method to check if a position is a corner."""
        row, col = pos
    
        # Check for walls around the position
        north_wall = (row - 1, col) in self.walls
        south_wall = (row + 1, col) in self.walls
        west_wall = (row, col - 1) in self.walls
        east_wall = (row, col + 1) in self.walls

        # Determine if this position is a corner based on wall presence
        if action == 'N':
            return north_wall and (west_wall or east_wall)
        if action == 'W':
            return west_wall and (north_wall or south_wall)
        if action == 'E':
            return east_wall and (north_wall or south_wall)
        if action == 'S':
            return south_wall and (west_wall or east_wall)

    def goal_test(self, state):
        """Checks if all boxes are in the goal positions. (Game won)"""
        return all(box in self.goals for box in state.boxes)

    def result(self, state, action):
        """Returns a new state with the Sokoban and the boxes positions updated based on the given action."""

        row, col = state.position
        row_offset, col_offset = self.get_offset(action)

        new_position = (row + row_offset, col + col_offset)
        new_boxes = set(state.boxes)
        
        if new_position in state.boxes:
            new_box_position = (row + 2 * row_offset, col + 2 * col_offset)
            new_boxes.remove(new_position)
            new_boxes.add(new_box_position)

        return SokobanState(new_position, tuple(new_boxes))
        
    def executa(self,state,actions):
        """Starting from the given state, executes a sequence of actions and returns the last executed state."""

        nstate=state
        for a in actions:
            nstate=self.result(nstate,a)
        return nstate
    
    def display(self, state):
        """Returns a string representation of the Sokoban game state in a grid format"""

        # Create a grid to copy the initial layout
        display_grid = []
        for row in range(self.height):
            display_grid.append([' '] * self.width)

        # Place walls, goals, and free spaces
        for (row, col) in self.free:
            display_grid[row][col] = '.'  # Lower priority than goals
        for (row, col) in self.walls:
            display_grid[row][col] = '#'
        for (row, col) in self.goals:
            display_grid[row][col] = 'o'

        # Place boxes
        for (row, col) in state.boxes:
            if (row, col) in self.goals:
                display_grid[row][col] = '*'  # Box on goal
            else:
                display_grid[row][col] = '$'  # Box on regular floor

        # Place Sokoban
        row, col = state.position
        if (row, col) in self.goals:
            display_grid[row][col] = '+'  # Sokoban on goal
        else:
            display_grid[row][col] = '@'  # Sokoban on floor

        return '\n'.join([''.join(line) for line in display_grid]) + '\n'
