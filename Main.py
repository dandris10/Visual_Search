import heapq
import pygame
import sys
import random
from collections import deque

WIDTH, HEIGHT = 800, 600
GRID_SIZE = 50
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE
WHITE, BLACK, RED, GREEN, BLUE = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)
VERTICES = ROWS * COLS

PREDEFINED_WALLS = [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (6, 4), (6, 5)]

# Node class
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = WHITE
        self.visited = False
        self.distance = 10000
        self.total_cost = 10000

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.col * GRID_SIZE, self.row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(win, BLACK, (self.col * GRID_SIZE, self.row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)  # Draw grid line

def create_predefined_walls(grid):
    for r, c in PREDEFINED_WALLS:
        grid[r][c].color = BLACK

def get_neighbors(node, grid):
    neighbors = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dr, dc in directions:
        r, c = node.row + dr, node.col + dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            neighbors.append((grid[r][c], random.randint(1,10)))  # Use a tuple to include both neighbor and weight
    return neighbors

def heuristic(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)

def reset_grid(grid):
    # Reset each node to default settings
    for row in grid:
        for node in row:
            node.color = WHITE if node.color != BLACK else BLACK
            node.visited = False
            node.distance = 10000
            node.total_cost = 10000

def a_star_search(grid, start, target, win):
    start.distance = 0
    priority_queue = [(0, id(start), start)]
    previous = {start : None}

    while priority_queue:
        current_distance, _, current_node = heapq.heappop(priority_queue)

        if current_node.visited:
            continue
    
        current_node.visited = 1

        if current_node == target:
            path_node = target
            while path_node is not None:
                if path_node.color != RED:  
                    path_node.color = BLUE 
                    path_node.draw(win)  
                    print(f"({path_node.row}, {path_node.col})")
                    pygame.display.update() 
                    pygame.time.delay(200)  
                path_node = previous[path_node]
            return True

        for neighbor, weight in get_neighbors(current_node, grid):
            if neighbor.color == BLACK:
                continue
            
            if neighbor.visited:
                continue    

            new_total_cost = current_distance + weight + heuristic(neighbor, target)

            if new_total_cost < neighbor.total_cost:
                neighbor.total_cost = new_total_cost
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (new_total_cost, id(neighbor), neighbor))

def dijkstra(grid, start, target, win):
    start.distance = 0
    priority_queue = [(0, id(start), start)]
    previous = {start: None}  

    while priority_queue:
        current_distance, _, current_node = heapq.heappop(priority_queue)

        if current_node.visited:
            continue

        current_node.visited = True

        if current_node == target:
            path_node = target
            while path_node is not None:
                if path_node.color != RED:  
                    path_node.color = BLUE 
                    path_node.draw(win)  
                    print(f"({path_node.row}, {path_node.col})")
                    pygame.display.update() 
                    pygame.time.delay(200)  
                path_node = previous[path_node]
            return True

        for neighbor, weight in get_neighbors(current_node, grid):
            if neighbor.color == BLACK:
                continue
            
            if neighbor.visited:
                continue

            new_distance = current_node.distance + weight

            if new_distance < neighbor.distance:
                neighbor.distance = new_distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, id(neighbor), neighbor))

def bfs(grid, start, end, win):
    queue = deque([start])
    start.visited = True;
    
    while queue:
        current = queue.popleft()
        for neighbor, _ in get_neighbors(current, grid):
            if not neighbor.visited and neighbor.color != BLACK:
                if neighbor == end:
                    print(f"Final node reached: ({neighbor.row}, {neighbor.col})")
                    return True
                print(f"({neighbor.row}, {neighbor.col})")
                neighbor.visited = True
                neighbor.color = BLUE
                neighbor.draw(win)
                pygame.display.update()
                queue.append(neighbor)
                pygame.time.delay(500)
                
    return False

def dfs(grid, node, end, win):
    if node == end:
        print(f"Final node reached: ({node.row}, {node.col})")
        return True  # Found the end node, stop recursion
    
    if node.visited:
        print(f"Final node reached: ({node.row}, {node.col})")
        return False

    node.visited = True
    print(f"({node.row}, {node.col})")

    if node.color != RED:
        node.color = BLUE
        node.draw(win)
        pygame.display.update()
        pygame.time.delay(500)

    for neighbor, _ in get_neighbors(node, grid):
        if neighbor.color != BLACK and not neighbor.visited:
            if dfs(grid, neighbor, end, win):
                return True

    return False

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Graph Algorithms")

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('A=DFS, B=BFS, C=A*, D=Dijkstra', True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, 30)

    grid = [[Node(i, j) for j in range(COLS)] for i in range(ROWS)]
    create_predefined_walls(grid)

    startClick = False
    endClick = False
    start = None
    end = None
    show_text = True

    run = True
    while run:
        win.fill(WHITE)

        for row in grid:
            for node in row:
                node.draw(win)

        if show_text:
            win.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                col, row = x // GRID_SIZE, y // GRID_SIZE

                if not startClick:
                    start = grid[row][col]
                    grid[row][col].color = RED
                    startClick = True

                elif not endClick:
                    end = grid[row][col]
                    grid[row][col].color = GREEN
                    endClick = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:
                    show_text = False
                    dfs(grid, start, end, win)

                elif event.key == pygame.K_b and start and end:
                    show_text = False
                    bfs(grid, start, end, win)

                elif event.key == pygame.K_c and start and end:
                    show_text = False
                    a_star_search(grid, start, end, win)

                elif event.key == pygame.K_d and start and end:
                    show_text = False
                    dijkstra(grid, start, end, win)

                elif event.key == pygame.K_SPACE: 
                    show_text = True
                    reset_grid(grid)
                    startClick = False
                    endClick = False
                    start = None
                    end = None

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()