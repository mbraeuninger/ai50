import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # ToDo: When number of cells = count all are mines
        if self.count == len(self.cells):
            return (cell for cell in self.cells)
        # raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # ToDo: When count in a sentence = 0 then all cells in sentence are safe
        if self.count == 0:
            return (cell for cell in self.cells)
        # raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # ToDo: If cell is in sentence, then remove it and reduce number of mines by 1
        if cell in self.cells and self.count > 0:
            self.cells.remove(cell)
            self.count - 1

        # raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # ToDo: If cell is in sentence where cell count > mine count: Remove it
        if cell in self.cells and self.count > 0:
            self.cells.remove(cell)

        # raise NotImplementedError


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def _get_all_cells(self):
        """
        Returns a set of all cells on the board
        """
        all_cells = set()
        for i in range(self.height):
            for j in range(self.width):
                all_cells.add((i, j))
        return all_cells

    def _get_surrounding_cells(self, cell):
        """
        Returns a set of all surrounding cells of a cell
        """
        # find correct limits for cells
        border_height_max = min(self.height, cell[0] + 1)
        border_height_min = max(0, cell[0] - 1)
        border_width_max = min(self.height, cell[1] + 1)
        border_width_min = max(0, cell[1] + 1)
        surr_cells = set()
        for i in range(border_height_min, border_height_max + 1):
            for j in range(border_width_min, border_width_max + 1):
                if (i, j) != cell:
                    surr_cells.add((i, j))
        return surr_cells

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # ToDo: mark cell as moved
        self.moves_made.add(cell)
        # ToDo: mark cell as safe
        self.safes.add(cell)
        # ToDo: create a new sentence
        count = Minesweeper.nearby_mines(cell)
        cells = self._get_surrounding_cells(cell)
        sentence = Sentence(cells, count)
        # ToDo: mark additional cells based on new knowledge
        # get mines
        if count == len(cells):
            sentence.mark_mine(cells)
        # mark safes
        if count == 0:
            sentence.mark_safe()
        # ToDo: add new sentence to knowledge base
        self.knowledge.append(sentence)

        # raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # ToDo: check if there are safe cells that are not on moves_made: Play one
        # ToDo: else return None
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

        # raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # ToDo: If make_safe_move is None play a random cell that has not been played yet, and is not in known mines
        if self.make_safe_move() == None:
            # get all moves
            cells = self._get_all_cells()
            potential_moves = set()
            for cell in cells:
                if cell not in self.moves_made and cell not in self.mines:
                    potential_moves.add(cell)
            if len(potential_moves) == 0:
                return None
            else:
                return random.choice(potential_moves)


        # raise NotImplementedError
