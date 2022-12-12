from copy import deepcopy

import pygame


class Cell:
    def __init__(self, left, top, size, pos, color="black", type_=0, border=1):
        self.left = left
        self.top = top
        self.size = size
        self.rect = pygame.Rect(left, top, size, size)
        self.color = color
        self.border = border
        self.pos = pos
        self.type_ = type_

    def draw(self, screen):
        if self.type_ == 0:
            rect = pygame.draw.rect(screen, "white", (self.left, self.top, self.size, self.size), self.border)
        else:
            rect = pygame.draw.rect(screen, "green", (self.left, self.top, self.size, self.size), 0)

    def collide_with_point(self, pos):
        return self.rect.collidepoint(pos[0], pos[1])

    def get_cords(self):
        return self.pos

    def set_color(self, color):
        self.color = color

    def set_type(self, type_):
        self.type_ = type_


class Grid:
    def __init__(self, width, height, cell_size=30, left=10, top=10, border=1):
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.border = border
        self.grid = [
            [Cell(self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size, (i, j)) for j in
             range(width)] for i in range(height)]
        self.turn = 0

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                self.grid[i][j].draw(screen)

    def get_cell(self, mouse_pos):
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j].collide_with_point(mouse_pos):
                    return (i, j)
        return None

    def on_click(self, cell_coords):
        self.grid[cell_coords[0]][cell_coords[1]].set_type(1)

    def get_click(self, mouse_pos):
        cell_pos = self.get_cell(mouse_pos)
        if not isinstance(cell_pos, type(None)):
            cell = self.grid[cell_pos[0]][cell_pos[1]]
            if cell.type_ == 0:
                self.on_click(cell_pos)
                self.turn = (self.turn + 1) % 2


class Life(Grid):
    def __init__(self, width, height, cell_size=30, left=10, top=10, border=1):
        super(Life, self).__init__(width, height, cell_size, left, top, border)

    def next_move(self):
        tmp_grid = deepcopy(self.grid)
        flag = False
        for i in range(len(tmp_grid)):
            for j in range(len(tmp_grid[0])):
                to_check_i = [0]
                to_check_j = [0]
                count = 0
                if i > 0:
                    to_check_i.append(-1)
                if j > 0:
                    to_check_j.append(-1)
                if i < len(tmp_grid) - 1:
                    to_check_i.append(1)
                if j < len(tmp_grid[0]) - 1:
                    to_check_j.append(1)
                for z in to_check_i:
                    for w in to_check_j:
                        count += tmp_grid[i + z][j + w].type_
                count -= tmp_grid[i][j].type_
                if self.grid[i][j].type_ == 0 and count == 3:
                    self.grid[i][j].set_type(1)
                    flag = True
                elif self.grid[i][j].type_ == 1 and (count == 3 or count == 2):
                    self.grid[i][j].set_type(1)
                else:
                    if self.grid[i][j] == 1:
                        flag = True
                    self.grid[i][j].set_type(0)
        return flag


pygame.init()
pygame.display.set_caption('aboba')
size = width, height = 800, 400
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
life_board = Life(width // 30, height // 30)
running = True
fps = 60
life_is_going = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                life_is_going = not life_is_going
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(life_board.get_cell(event.pos))
            life_board.get_click(event.pos)
        elif event.type == pygame.MOUSEWHEEL:
            if event.y < 0:
                fps -= 1
            elif event.y > 0:
                fps += 1
    if life_is_going:
        life_is_going = life_board.next_move()
    screen.fill((0, 0, 0))
    clock.tick(fps)
    life_board.render(screen)
    pygame.display.flip()
