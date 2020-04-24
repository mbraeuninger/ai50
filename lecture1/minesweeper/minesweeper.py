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
        if self.count == len(self.cells):
            return (cell for cell in self.cells)

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return (cell for cell in self.cells)

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells and self.count > 0:
            self.cells.remove(cell)
            self.count - 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells and self.count > 0:
            self.cells.remove(cell)


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
        border_width_max = min(self.width, cell[1] + 1)
        border_width_min = max(0, cell[1] - 1)
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
        print(f"count is {count}")
        print(f"cell is {cell}")
        self.moves_made.add(cell)
        self.safes.add(cell)
        surr_cells = self._get_surrounding_cells(cell)
        new_sentence = Sentence(surr_cells, count)
        print(f"sentence is {new_sentence}")
        # mark safes
        if count == 0:
            for surr_cell in surr_cells:
                new_sentence.mark_safe(surr_cell)
                self.safes.add(surr_cell)
                if surr_cell in self.mines:
                    self.mines.remove(surr_cell)

        # check for other known safes if there are mines in surrounding cells
        else:
            temp_cell_set = set()
            for surr_cell in surr_cells:
                if surr_cell in self.safes:
                    temp_cell_set.add(surr_cell)
            new_sentence = Sentence(surr_cells - temp_cell_set, count)

        # get all cells as mines when length is the same
        if count == len(surr_cells):
            for surr_cell in surr_cells:
                new_sentence.mark_mine(surr_cell)
                self.mines.add(surr_cell)

        print("Knowledge method Pt. 1 is done.")
        print(f"Known safes are {self.safes}")
        print(f"Known mines are {self.mines}")
        print("Start comparison with other sentences")
        # compare information with other sentences
        for sentence in self.knowledge:
            print(f"Comparing current {surr_cells} with {sentence.cells}")
            sentence = self._update_sentence(sentence)
        print("Comparison is done")
        print(f"Known safes are {self.safes}")
        print(f"Known mines are {self.mines}")
        self.knowledge.append(new_sentence)
        print(f"New sentence added to knowledge base")

    def _update_sentence(self, sentence):
        """
        Updates a given sentence with the knowledge about mines and safes.
        """
        if sentence.count > 0:
            # get rid of mines to find safes
            for mine in self.mines:
                if mine in sentence.cells:
                    sentence.cells.remove(mine)
                    sentence.count -= 1
                if len(sentence.cells) == 0:
                    for cell in sentence.cells:
                        # sentence.mark_safe(cell)
                        self.safes.add(cell)
            # get rid of safes to identify mines
            for safe in self.safes:
                sentence.cells.remove(safe) if safe in sentence.cells else None
                if len(sentence.cells) == sentence.count:
                    for cell in sentence.cells:
                        # sentence.mark_mine(cell)
                        sentence.count -= 1
                        self.mines.add(cell)
        return sentence


    def _compare_two_sentences(self, s1, s2):
        """
        Compares a new sentence with all existing sentences in knowledge base
        """
        print("start comparison method")
        s1_count = s1.count
        s1_cells = s1.cells
        s2_count = s2.count
        s2_cells = s2.cells

        # check if they are the same
        if s1_cells == s2_cells:
            return print("Sentences are the same. Abort")

        # assign anonymous variables to facilitate comparison
        if s1_cells.issubset(s2_cells) and s1_count <= s2_count:
            x_count = s1_count
            x_cells = s1_cells
            y_count = s2_count
            y_cells = s2_cells
        elif s2_cells.issubset(s1_cells) and s2_count <= s1_count:
            x_count = s2_count
            x_cells = s2_cells
            y_count = s1_count
            y_cells = s1_cells
        else:
            return print(f"Set 1 {s1_cells} and set 2 {s2_cells} are not related")

        # generate new sentence parameters
        new_cells = y_cells - x_cells
        new_count = y_count - x_count
        new_count = new_count if new_count > 0 else 0
        new_sentence = Sentence(new_cells, new_count)
        print(f"New sentence was generated with cells {new_cells} and length {new_count}")

        # check is safety is guaranteed
        if new_count == 0:
            print("New sentence is safe")
            for cell in new_cells:
                new_sentence.mark_safe(cell)
                self.safes.add(cell)
        elif new_count == len(new_cells):
            print("New sentence is conclusive about mines")
            for cell in new_cells:
                new_sentence.mark_mine(cell)
                self.mines.add(cell)

        # add new sentence to knowledge
        self.knowledge.append(new_sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        cells = self._get_all_cells()
        save_moves = []
        for cell in cells:
            if cell not in self.moves_made and cell in self.safes:
                save_moves.append(cell)
        if len(save_moves) == 0:
            return None
        else:
            return random.choice(save_moves)

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        if self.make_safe_move() == None:
            # get all moves
            cells = self._get_all_cells()
            potential_moves = []
            for cell in cells:
                if cell not in self.moves_made and cell not in self.mines:
                    potential_moves.append(cell)
            if len(potential_moves) == 0:
                return None
            else:
                return random.choice(potential_moves)
