assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'




def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

diag_units = [[r+c for r,c in zip(rows, cols)], [r+c for r,c in zip(reversed(rows), cols)]] 
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
 
def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    d = {}
    index = 0
    for s in grid:
        if(s == '.'):
            d[boxes[index]] = cols
        else:
            d[boxes[index]] = s
        index = index+1
    return d

def eliminate(values):
    """
    If a value is assigned to the box then we need to remove it as a possible value from all its peers.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the assigned values removed as posible values from peers.

    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit, ''))
    return values



def only_choice(values):
    """
    If there is only one box in the unit (box, column or row) that can have a value i.e. no other box in the group
    has this value as possible value then we know that this value has to be assigned to this box. We implement this
    strategy in this method
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the only choice values are assigned.

    """
    for u in unitlist:
        for x in range(1,10):
            index = -1
            for i1 in u:
                val = values[i1]
                if isinstance(val,str) and str(x) in val:
                    if index==-1:
                        index = i1
                    else:
                        index = 0
            if index !=-1 and index != 0:
                assign_value(values, index, str(x))
    return values



def reduce_puzzle(values):
    """
    In this method we apply all the strategies to solve our puzzle. We first apply the eliminate strategy, then only_choice and then naked_twins.
    We keep on doing this until we reach point that iterating is not solving our problem anymore
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the reduced sudoku puzzle or Flase if reach the state where we have incorrect solution

    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        eliminate(values)
        # Your code here: Use the Only Choice Strategy
        only_choice(values)
        naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values




def search(values):
    """
    In this method we reduce the puzzle and then we pick the boxes with least possible values and then assign these possibe values to the box and recursive callable
    call this method thus implementing depth first search  
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the solved sudoku puzzle or Flase if reach the state where we have incorrect solution

    """
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for x1 in values[s]:
        c1 = values.copy()
        c1[s] = x1
        at = search(c1)
        if at != False:
            return at
    return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    grd = grid_values(grid)
    return search(grd)




def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    units_with_2_val = [v for v in boxes if len(values[v])==2]

    for u in units_with_2_val:
        rows_u_belongs_to = [r for r in row_units if u in r]
        rows_twin = [r for r in rows_u_belongs_to[0] if values[r] == values[u]]

        cols_u_belongs_to = [c for c in column_units if u in c]
        cols_twin = [c for c in cols_u_belongs_to[0] if values[c] == values[u]]

        box_u_belongs_to = [b for b in column_units if u in b]
        box_twin = [b for b in box_u_belongs_to[0] if values[b] == values[u]]
        
        replaceTwinValues(values, rows_u_belongs_to[0], rows_twin, values[u])
        replaceTwinValues(values, cols_u_belongs_to[0], cols_twin, values[u])
        replaceTwinValues(values, box_u_belongs_to[0], box_twin, values[u])

    return values
   
def replaceTwinValues(values, arr, twins, valuesToReplace):
    """
    This is helper method to remove values from a group (box, row or column). It is used in naked_twins method only
    """
     if len(twins) == 2:
            for rp in arr:
                if rp not in twins:
                    for s in valuesToReplace:
                        assign_value(values, rp,values[rp].replace(s, ''))
    
    
   

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
