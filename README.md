# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: We solve the naked twins through constraint propogation by using the fact that if a unit (row, column or box) have two boxes such that they have identical possible values and number of thse possible values in two as well, then we can conclude that within the unit only these two boxes can have these two possible values and we can safely remove these two possible values from all of the unit. We are propogating the constraint by removing these two values from the posible values from the rest of the unit. 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We are adding two more units to the sudoku board and these re the two diagno that are formed. We will treat them just like column or row or box constraint. By haing additional constraint we can move towards solution quicker.

