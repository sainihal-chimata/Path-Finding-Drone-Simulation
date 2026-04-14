import pygame
import time
import math

graph = {
    'S': [('B', 4), ('C', 7), ('D', 6)],
    'B': [('E', 3), ('F', 5)],
    'C': [('F', 2), ('G', 4)],
    'D': [('G', 3), ('H', 6)],
    'E': [('T', 8)],
    'F': [('T', 5)],
    'G': [('T', 4)],
    'H': [('T', 7)]
}

alpha, beta, gamma = 1, 2, 0.5
W1, W2, W3, W4 = 1, 1, 1, 1
P = 2
V = 5

def dfs(node, path, dist, paths):
    if node == 'T':
        paths.append((path, dist))
        return
    for neighbor, d in graph[node]:
        dfs(neighbor, path + [neighbor], dist + d, paths)

paths = []
dfs('S', ['S'], 0, paths)

results = []

for path, D in paths:
    E = alpha * D + beta * P + gamma * (V ** 2)
    T = D / V
    C = W1*D + W2*E + W3*T + W4*P
    results.append((path, C))

best = min(results, key=lambda x: x[1])

print("\nAll Paths and Costs:")
for path, cost in results:
    print(f"Path: {path}, Cost: {cost:.2f}")

print("\nBest Path:", best)

positions = {
    'S': (0.1, 0.5),
    'B': (0.3, 0.3),
    'C': (0.3, 0.5),
    'D': (0.3, 0.7),
    'E': (0.6, 0.35),
    'F': (0.6, 0.5),
    'G': (0.6, 0.65),
    'H': (0.6, 0.8),
    'T': (0.85, 0.5)
}

pygame.init()

win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = win.get_size()

pygame.display.set_caption("Drone Path Optimization")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

font_small = pygame.font.SysFont(None, 28)
font_large = pygame.font.SysFont(None, 40)

def get_pixel_pos(node):
    return (int(positions[node][0] * WIDTH),
            int(positions[node][1] * HEIGHT))

def draw_graph():
    win.fill(WHITE)

    title = font_large.render("Drone Path Optimization", True, BLACK)
    win.blit(title, (WIDTH//2 - 200, 20))

    for node in graph:
        for neighbor, _ in graph[node]:
            pygame.draw.line(win, BLACK, get_pixel_pos(node), get_pixel_pos(neighbor), 2)

    for node in positions:
        pos = get_pixel_pos(node)
        pygame.draw.circle(win, RED, pos, 12)
        label = font_small.render(node, True, BLACK)
        win.blit(label, (pos[0] + 10, pos[1] - 10))

def draw_path(path, color):
    for i in range(len(path)-1):
        pygame.draw.line(win, color,
                         get_pixel_pos(path[i]),
                         get_pixel_pos(path[i+1]), 5)

def draw_ui(current_cost=None, best_cost=None):
    if current_cost is not None:
        text1 = font_large.render(f"Path Cost: {current_cost:.2f}", True, BLACK)
        win.blit(text1, (20, 80))

    if best_cost is not None:
        text2 = font_large.render(f"Best Cost: {best_cost:.2f}", True, BLACK)
        win.blit(text2, (20, 140))

def animate_drone(path, color, cost, best_cost=None):
    clock = pygame.time.Clock()

    for i in range(len(path)-1):
        start = get_pixel_pos(path[i])
        end = get_pixel_pos(path[i+1])

        steps = 80

        for t in range(steps):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return

            x = start[0] + (end[0] - start[0]) * t / steps
            y = start[1] + (end[1] - start[1]) * t / steps

            draw_graph()
            draw_path(path, color)

            draw_ui(current_cost=cost, best_cost=best_cost)

            pulse = 5 + int(3 * math.sin(t * 0.3))
            pygame.draw.circle(win, (0, 180, 255), (int(x), int(y)), pulse + 5)
            pygame.draw.circle(win, (255, 255, 255), (int(x), int(y)), pulse)

            pygame.display.update()
            clock.tick(30)

running = True

draw_graph()
pygame.display.update()
time.sleep(1)

for path, cost in results:
    animate_drone(path, BLUE, cost)
    time.sleep(0.5)

draw_graph()
draw_path(best[0], GREEN)
draw_ui(current_cost=best[1], best_cost=best[1])
pygame.display.update()

animate_drone(best[0], GREEN, best[1], best[1])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

pygame.quit()
