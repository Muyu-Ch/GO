import pygame
import math

WINDOW_SIZE = 800

BOARD_COLOR = (210, 170, 110)

BOARD_MARGIN = 50

GRID_COUNT = 19

GRID_SPACING = (WINDOW_SIZE - 2 * BOARD_MARGIN) / (GRID_COUNT - 1)

STONE_RADIUS = 17

POINT_RADIUS = 5

CLICK_RADIUS=10

class Board:
    def __init__(self):
        self.size = 19
        self.grid = [
            ['*' if i == 0 or i == self.size + 1 or j == 0 or j == self.size + 1 else '.'
                for j in range(self.size + 2)]
                for i in range(self.size + 2)
            ]   
        self.current_player = 'B'  

    def draw_board(self, screen):
        screen.fill(BOARD_COLOR)

        for i in range(self.size):
            start_pos = (BOARD_MARGIN, BOARD_MARGIN + i * GRID_SPACING)
            end_pos = (WINDOW_SIZE - BOARD_MARGIN, BOARD_MARGIN + i * GRID_SPACING)
            pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 1)

            start_pos = (BOARD_MARGIN + i * GRID_SPACING, BOARD_MARGIN)
            end_pos = (BOARD_MARGIN + i * GRID_SPACING, WINDOW_SIZE - BOARD_MARGIN)
            pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 1)

        for i in range(3):
            for j in range(3):
                point_x = BOARD_MARGIN + (3 + 6 * i) * GRID_SPACING
                point_y = BOARD_MARGIN + (3 + 6 * j) * GRID_SPACING
                pygame.draw.circle(screen, (0, 0, 0), (int(point_x), int(point_y)), POINT_RADIUS)
        
        pygame.display.flip()

    def draw_stone(self, screen):
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                if self.grid[i][j] == 'B':
                    stone_color = (0, 0, 0)
                elif self.grid[i][j] == 'W':
                    stone_color = (255, 255, 255)
                else:
                    continue
                pos_x = BOARD_MARGIN + (j - 1) * GRID_SPACING
                pos_y = BOARD_MARGIN + (i - 1) * GRID_SPACING
                pygame.draw.circle(screen, stone_color, (int(pos_x), int(pos_y)), STONE_RADIUS)
        pygame.display.flip()

    def check_click(self,x,y):
        for i in range(1,self.size+1):
            for j in range(1,self.size+1):
                pos_x = BOARD_MARGIN + (j - 1) * GRID_SPACING
                pos_y = BOARD_MARGIN + (i - 1) * GRID_SPACING
                if math.sqrt((x-pos_x)**2+(y-pos_y)**2)<=CLICK_RADIUS:
                    return i,j
        return -1,-1
      
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
        eaten=set()
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                if self.grid[i][j] == self.opposite_color() and self.count_breath(i, j) == 0:
                    eaten.add((i,j))
                    ifeaten=True
        for i in eaten:
            self.grid[i[0]][i[1]]='.'
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
pygame.init()
screen=pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
board.draw_board(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                print(mouse_x, mouse_y)
                x,y=board.check_click(mouse_x,mouse_y)
                if board.move(x,y):
                        board.display()
                        board.draw_board(screen)
                        board.draw_stone(screen)
                else:
                    print("Invalid move. Try again.")
