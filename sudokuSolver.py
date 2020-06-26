from easy_puzzles import easy, one
from hard_puzzles import hard
import random

# The Sudoku solving method was strongly influenced by Peter Norvig's brilliant essay on solving Sudoku puzzles 
# For a more detailed explanation, I highly recommend checking it out at http://norvig.com/sudoku.html
# Sudoku is considered "Solved" when cells in every "Unit" are filled with a permutation of digits 1 to 9. A unit is defined as one of: 
# a row, a column or a 3x3 square. Cells that share a unit are called "Peers".


# Setting up the datastructure for cells, units and peers
digits = "123456789"
rows = "ABCDEFGHI"
cols = digits
cells = [(r + c) for r in rows for c in cols] 
unitlist = ([[(r + c) for r in rows] for c in cols] + # Rows
            [[(r + c) for c in cols] for r in rows] + # Colums
            [[(r + c) for r in rs for c in cs] for rs in ("ABC", "DEF", "GHI") for cs in ("123", "456", "789")]) # Squares


units = dict((c, [u for u in unitlist if c in u]) for c in cells)
peers = dict((cell, set(sum(units[cell], [])) - set([cell])) 
            for cell in cells)


# Conducting some unit tests
def test():
    assert len(cells) == 81
    assert len(unitlist) == 27
    assert all(len(units[cell]) == 3 for cell in cells)
    assert all(len(peers[cell]) == 20 for cell in cells)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers["A1"] == set(['H1', 'A9', 'D1', 'C3', 'A4', 'F1', 'I1', 'E1', 'A5', 
                            'B1', 'A3', 'G1', 'B2', 'C1', 'B3', 'A6', 'A7', 'A8', 'C2', 'A2'])

    print("Tests pass")


test()
grid = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"

def parse_grid(grid):
    values = dict((cell, digits) for cell in cells)
    for cell, d in grid_values(grid).items():
        if d in digits and not assign(values, cell ,d):
            return False
    return values


def grid_values(grid):
    chars = [c for c in grid if c in digits or c in "0."]
    assert len(chars) == 81
    return dict(zip(cells, chars))


def assign(values, cell, d):
    other_values = values[cell].replace(d, "")
    if all(eliminate(values, cell, d2) for d2 in other_values):
        return values
    else:
        return False

def eliminate(values, cell, d):
    if d not in values[cell]:
        return values # Already eliminated
    values[cell] = values[cell].replace(d, "")

    # (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[cell]) == 0:
        return False # Contradiction: removed last value
    elif len(values[cell]) == 1:
        d2 = values[cell]
        if not all(eliminate(values, cell2, d2) for cell2 in peers[cell]):
            return False

    # (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[cell]:
        dplaces = [cell for cell in u if d in values[cell]]
        if len(dplaces) == 0:
            return False # Contradiction: no place for this value
        elif len(dplaces) == 1:
            if not assign(values, dplaces[0], d):
                return False
        
    return values


def display(values):
    width = 1 + max(len(values[cell]) for cell in cells)
    line = "+".join(["-"*(width*3)]*3)
    for r in rows:
        print("".join(values[r+c].center(width)+("|" if c in "36" else "") for c in cols))
        if r in "CF": print(line)
    print


def solve(grid): return search(parse_grid(grid))


def search(values):
    if values is False:
        return False # Failed earlier
    if all(len(values[cell]) == 1 for cell in cells):
        return values  # Solved
    # Choose unfilled cell with fewest possibilities
    _, cell = min((len(values[cell]), cell) for cell in cells if len(values[cell]) > 1)
    return some(search(assign(values.copy(), cell, d)) for d in values[cell])


def some(seq):
    for e in seq:
        if e: return e
    return False


puzzle_choice = random.choice(one)

print("Constraint Propagation")
display(parse_grid(puzzle_choice))

print("Depth first + Constraint Propagation")
display(solve(puzzle_choice))

def reduce_max(values):
    if values is False:
        return False
    
    while True:
        unique = True
        if unique == False:
            return values
        
        rCell = random.choice(cells)
        if values[rCell] not in digits:
            continue
        
        values[rCell] = "."
        newGrid = "".join(map(str, values.values()))
        
        if solve()

        break

reduce_max(solve(puzzle_choice))
