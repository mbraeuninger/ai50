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

    def _print(self, assignment):
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
        for var in self.domains:
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
            # print(f"""var x: {x} overlaps at {i}\nx words: {self.domains[x]}\nvar y: {y} overlaps at {j}\ny words: {self.domains[y]}\n""")
            
            revision_counter = 0
            words = copy.deepcopy(self.domains[x])
            for word in words:
                letters_y = [w[j] for w in self.domains[y]]
                if word[i] not in letters_y:
                    self.domains[x].remove(word)
                    revision_counter =+ 1
                    # print(f"1 added to revision for {word} at {i} and {letters_y}\n")
            
            if revision_counter > 0:
                # print(f"revised {revision_counter} words\nnew domain for {x} is {self.domains[x]}")
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
                        if var != arc[1]:
                            arcs.append((var, arc[0]))

        # check for empty domains
        if all(value is not None for value in self.domains.values()):
            return True
        else:
            return False
        

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
        if len(set([value for value in assignment.values()])) != len(set(assignment.values())):
            return False

        for var, word in assignment.items():
            
            if var.length != len(word):
                return False
            
            for n in self.crossword.neighbors(var).intersection(assignment.keys()):
                i = self.crossword.overlaps[var, n][0]
                j = self.crossword.overlaps[var, n][1]
                if word[i] != assignment[n][j]:
                    return False
        
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # get dict with all values in domain of var
        domain_dict = {word: 0 for word in self.domains[var]}
        # get neighbors of var
        neighbors = {neighbor: None for neighbor in self.crossword.neighbors(var)}
        # find neighbors domain values and remove assigned
        for word in self.domains[var]:
            for neighbor in (neighbors.keys() - assignment.keys()):
                i = self.crossword.overlaps[var, neighbor][0]
                j = self.crossword.overlaps[var, neighbor][1]
                for neighbor_word in self.domains[neighbor]:
                    # increment counter in domain dict if there is a match
                    if word[i] != neighbor_word[j]:
                        domain_dict[word] += 1
        
        domain_dict_sorted = sorted(domain_dict.items(), key=lambda x:x[1])

        return [word[0] for word in domain_dict_sorted]


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # find unassigned vars
        unassigned = self.domains.keys() - assignment.keys()
        
        # check how many values they have and pick var with lowest
        values = {var: len(self.domains[var]) for var in unassigned}
        sorted_values = sorted(values.items(), key=lambda x: x[1])
        
        # check degree (number of neighbors) in case you have multiple options
        if len(sorted_values) == 1 or sorted_values[0][1] < sorted_values[1][1]:
            return sorted_values[0][0]
        else:
            neighbors = {var: len(self.crossword.neighbors(var)) for var in unassigned}
            sorted_neighbors = sorted(neighbors.items(), key=lambda x: x[1], reverse=True)
            return sorted_neighbors[0][0]
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        print(f"init backtrack with assignment {assignment}")
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for word in self.order_domain_values(var, assignment):
            # try if consistent
            temp_assignment = copy.deepcopy(assignment)
            temp_assignment[var] = word
            if self.consistent(temp_assignment):
                assignment[var] = word
                print(f"found new assignment {assignment} in backtrack")
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            assignment[var] = None
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
