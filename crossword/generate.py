import sys

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

    def print(self, assignment):
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
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
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
        # For each domain check lenghts of words and lengeth of variables. If differs remove word from domain
        for var in self.crossword.variables:
            for word in self.domains[var].copy():
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps.get((x, y))
        revision = False
        if overlap:
            for wordx in self.domains[x].copy():
                # Check if exist posibble y for wordx
                exists = False
                # For every wordy check if it fits and if not remove wordx from x's domain
                if not any([x[overlap[1]] == wordx[overlap[0]] for x in self.domains[y]]):
                    self.domains[x].remove(wordx)
                    revision = True
        return revision                    

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            queue = []
            for x in self.crossword.variables:
                for y in self.crossword.variables:
                    if x != y:
                        queue.append((x, y))
        else:
            queue = arcs
            
        while queue:
            X, Y = queue.pop(0)
            if self.revise(X, Y):
                if len(self.domains[X]) == 0:
                    return False
                for y in self.crossword.neighbors(X):
                    if y != Y:
                        queue.append((y, X))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(self.crossword.variables) == len(assignment):
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for var, word in assignment.items():
            # check word lenghts
            if var.length != len(word):
                return False
            # check colisions
            for n in self.crossword.neighbors(var):
                if n in assignment.keys():
                    overlap = self.crossword.overlaps[var, n]
                    if word[overlap[0]] != assignment[n][overlap[1]]:
                        return False
        return True
        

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        lista = []
        # Iterate over domain
        for val in self.domains[var]:
            counter = 0
            # iterate over neighbours
            for n in self.crossword.neighbors(var):
                if val in self.domains[n]:
                    counter += 1
            lista.append([val, counter])
        lista.sort(key=lambda x: x[1], reverse=False)
        return [x[0] for x in lista]
        
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        minval = 100000
        minnode = None
        # Iterate over nodes
        for var in self.crossword.variables:
            if var not in assignment:
                if len(self.domains[var]) < minval:
                    minval = len(self.domains[var])
                    minnode = var
                elif len(self.domains[var]) == minval:
                    # check number of neighbours
                    old_n = self.crossword.neighbors(minnode)
                    new_n = self.crossword.neighbors(var)
                    if new_n > old_n:
                        minval = len(self.domains[var])
                        minnode = var
        return minnode
                        
                    
                    


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        for word in self.order_domain_values(var, assignment):
            assignment[var] = word
            if self.consistent(assignment):
                val = self.backtrack(assignment)
                if val is None:
                    del assignment[var]
                else:
                    return val


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
