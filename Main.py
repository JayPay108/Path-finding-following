from Graph import Graph
from DynamicMovement import Character
from Vector import Vector
import pygame

SIZE = (40, 40) # (columns, rows)

COLS = SIZE[0]
ROWS = SIZE[1]

XPIXELS = COLS * 30
YPIXELS = ROWS * 30

screen = pygame.display.set_mode((XPIXELS, YPIXELS))

graph = Graph(SIZE)
graph.draw(screen)

makingBoard = True
while makingBoard:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:
            makingBoard = False

    clicks = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()

    if clicks[0]:
        selected = graph.getSelected(pos)
        if selected != None:
            graph.nodes[selected].makeWall(True, screen)

    elif clicks[2]:
        selected = graph.getSelected(pos)
        if selected != None:
            graph.nodes[selected].makeWall(False, screen)


graph.findPath(screen)
path = graph.retrievePath()

if path == None:
    graph.nodes[graph.first].draw(screen, True)
    graph.nodes[graph.last].draw(screen, True)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

pathDistance = path.distance[-1]
followPathOffset = 35 / pathDistance

startPos = Vector(graph.nodes[graph.first].xLocation, graph.nodes[graph.first].yLocation)
character = Character(position = startPos, maxSpeed = 2, maxAccleration = 2, offset = followPathOffset)

location = (int(character.position.x), int(character.position.y))
lastLocation = location

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    character.followPath(path)

    location = (int(character.position.x), int(character.position.y))

    pygame.draw.line(screen, (255, 0 , 0), (lastLocation[0] + 15, lastLocation[1] + 15), (location[0] + 15, location[1] + 15), 4)
    pygame.display.update()

    lastLocation = location

