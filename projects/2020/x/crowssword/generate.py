import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def _rint(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains.keys():
            words = copy.deepcopy(self.domains[var])
            for word in words:
                if var.length != len(word):
                    self.domains[var].remove(word)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        if self.crossword.overlaps[x, y]:
            i = self.crossword.overlaps[x, y][0]
            j = self.crossword.overlaps[x, y][1]
            
            revision_counter = 0
            for word in self.domains[x]:
                letters_y = [w[j] for w in self.domains[y]]
                if word[i] not in letters_y:
                    self.domains[x].remove(word)
                    revision_counter =+ 1
            
            if revision_counter > 0:
                return True
            else:
                return False

        else:
            return False


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # build list of arcs and puts them in queue
        if not arcs:
            arcs = []
            vars = [var for var in self.domains.keys()]
            for var in vars:
                # print(f"var: {var}")
                # print(f"overlaps:\n{self.crossword.overlaps}")
                for var2 in vars:
                    if var == var2: # skip when variable is same
                        continue
                    if self.crossword.overlaps[var, var2]:
                        arcs.append((var, var2))

        while len(arcs) > 0:
            for arc in arcs:
                arcs.remove(arc)
                if self.revise(arc[0], arc[1]):
                    if len(self.domains[arc[0]]) == 0:
                        return False
                    for var in self.crossword.neighbors(arc[0]):
                        arcs.append(var, arc[0])
        return True
        

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for key in self.domains.keys():
            if not assignment.get(key) or not assignment[key]:
                return False
        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # check if values are distinct:
        if len([value for value in assignment.values()]) > len(set(assignment.values())):
            return False

        for var, word in assignment.items():
            if self.domains[var].length != len(word):
                return False
            
            for n in self.crowssword.neighbors(var):
                i = self.crowssword.overlaps[x, y][0]
                j = self.crowssword.overlaps[x, y][1]
                if assignment[var][i] != assignment[n][j]:
                    return False
        
        return True
        

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # get neighbors of var
        neighbors = self.crossword.neighbors(var)
        # get domain of variable
        words = self.domains[var]
        # find domain for each neighbor
        word_dict = {n: self.domains[neighbor] for neighbor in neighbors}
        # create dict with domain values 
        output_dict = {}
        for word in words:
            output_dict[w]: len([word if word in word_dict[neighbor] else None for neighbor in neighbors])
        # sort by matching values counted
        output_dict = {w: l for w, l in sorted(output_dict.items(), key=lambda x: x[1])}        

        return list(output_dict.keys())


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # find unassigned vars
        unassigned = list(self.domains.keys())
        # check how many values they have and pick var with lowest
        values = {var: len(self.domains[var]) for var in unassigned}
        results = [var for var in values if values[var] == min(values.values())]
        # check degree (number of neighbors)
        if len(results) > 1:
            neighbors = {var: len(self.crossword.neighbors(var)) for var in unassigned}
            results = [var for var in neighbors if neighbors[var] == min(neighbors.values())]
            return results[0]
        else:
            return results[0]
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if assignment_complete(assignment):
            return assignment
        else:
            var = select_unassigned_variable(assignment)
            for word in order_domain_values(var, assignment):
                if consistent(assignment): #TODO: That does not make sens with the current function
                    self.domains[var].add(word)
                    result = backtrack(assignment)
                    if assignment_complete(result):
                        return result
                    else:
                        self.domains[var].remove(word)
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
