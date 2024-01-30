# Python-Sudoku
Fun Sudoku game a classmate paid me to write.
I thought it was kind of cool so I figured why not post it on GitHub.
If you're reading this, I turned the repo public which means me and said classmate both graduated.
Hi meneer Weert :D 🥧!

It creates a random possible grid by first creating a random completed
grid and removing a random amount of cells from that completed grid.

The random completed grid is made by using an algorithm to
randomly (optional) solve the grid, so it also has a built-in Sudoku solver.

You can also place subvalues to keep track of what might be what,
and there's a possibility to save a grid to a json file and load it again later.

Keybinds:

- Left Mouse Button: Select a cell to give it a value
- Right Mouse Button: Select a cell to give it a subvalue (subvalues do not do anything, they are just "notes")
- 1-9: Give a cell a (sub)value
- Backspace: Restart a game
- L or Right Shift: Load a game from the save file
- S or Return: Save the current grid to the save file
- Forward Slash: Try to solve the current grid with the built-in Sudoku solver
- Middle Mouse Button: Debug the cell you're hovering over



![ZOvc5Gz](https://user-images.githubusercontent.com/104533077/214709033-eabaa58f-a88c-4fee-9c0d-0a97f251f223.png)
