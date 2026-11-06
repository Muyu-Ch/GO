class Board:
    def __init__(self):
        self.size = 19
        self.grid = [
            ['*' if i == 0 or i == self.size + 1 or j == 0 or j == self.size + 1 else '.'
                for j in range(self.size + 2)]
                for i in range(self.size + 2)
            ]   
        self.current_player = 'B'  

    def display(self):
        for row in self.grid:
            print(' '.join(row))

    def get_current_player(self):
        return "BLACK" if self.current_player == 'B' else "WHITE"
    
    def opposite_color(self):
        if self.current_player == 'B':
            return 'W'
        elif self.current_player == 'W':
            return 'B'
        else:
            raise ValueError("Color must be 'B' for black or 'W' for white.")

    def change_player(self):
        self.current_player = self.opposite_color()

    def count_breath(self,x,y):
        color=self.grid[x][y]
        if color!="B" and color!="W":
            return False
        breath=set()
        visited=set()
        visited.add((x,y))
        ifadded=True
        while ifadded:
            newcounted=set()
            ifadded=False
            for i in visited:
                for j in [(i[0]+1,i[1]),(i[0]-1,i[1]),(i[0],i[1]+1),(i[0],i[1]-1)]:
                    if self.grid[j[0]][j[1]]=='.' and j not in breath:
                        breath.add(j)
                        ifadded=True
                    elif self.grid[j[0]][j[1]]==color and j not in visited:
                        newcounted.add(j)
                        ifadded=True
            visited.update(newcounted)
        return len(breath)

    def eat_stone(self):
        ifeaten=False
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                if self.grid[i][j] == self.opposite_color() and self.count_breath(i, j) == 0:
                    self.grid[i][j] = '.'
                    ifeaten=True
        return ifeaten
    
    def move(self, x, y):
        if not (1 <= x <= self.size and 1 <= y <= self.size):
            return False
        if self.grid[x][y] != '.' :
            return False
        
        self.grid[x][y]= self.current_player

        if self.eat_stone():
            self.change_player()
            return True

        if self.count_breath(x,y)==0:
            self.grid[x][y]='.'
            return False

        self.change_player()
        return True
    
board = Board()

while True:
    board.display()
    print(f"Current player: {board.get_current_player()}")
    move = input("Enter your move (x y) or 'q' to quit: ")
    if move.lower() == 'q':
        break
    try:
        x, y = map(int, move.split())
        if board.move(x, y):
            pass
        else:
            print("Invalid move. Try again.")
    except ValueError:
        print("Invalid input. Please enter two integers separated by a space.")
board.display()