Project for being able to put things into a ranked ELO list. In order to run it run the command
```
python ranking.py <name of the file that will save your ranks>
```

## Input File Columns

When you provide the input file (which can be empty on your first run), these are the column headers to look out for in your CSV you make

1. Title: Required column providing the name of the item
2. Elo: Required and will store the ELO value
3. year: Optional to provide the date associated with the item
4. W: Optional to keep track of number of wins of item
5. L: Optional to keep track of number of losses of item
6. <any other column of yours>: Optional and will be prompted to be filled out whenever you enter an item (suggested to be called genre)

## Functions of the Program
0. Quit: **NOTE YOUR LIST ONLY SAVES IF YOU GRACEFULLY QUIT THIS WAY**. Hitting any key thats not one of the below options also will gracefully quit.
1. Enter a new item: Follow the prompts to add a new item to the list. You will the be prompted to match it up against 10 random items of your list
2. Random Match: Select between two random items
3. Rankings: Print the rankings
4. Ranked Match: Select between two items with "close" elo scores
5. Partial Rankings: Print the rankings of a specific search criteria found in a "genre" column (if you have one)
6. Plot Elo: Plot out the elo scores in a scatter plot
7. Search: Provide the rank of a specific item
8. Choose a match: Select between two items you choose