import Node
import PlacementNode


class Map:
    totalNodes = 0
    nodes: [Node] = []              # coordinates of nodes
    placements: [PlacementNode] = []         # coordinates of placed nodes

    start = [0, 0]          # where the placement nodes need to start
    scale = 0               # distance between placements
    radius = 0              # distance that a placed node can claim nodes
    maxPlacementNodes = 0   # max placable nodes

    def __init__(self, start, scale, radius, mPN):
        self.start = start
        self.scale = scale
        self.radius = radius
        self.maxPlacementNodes = mPN

    def createNode(self, s, x, y):      # x-, y- coordinates
        self.totalNodes += 1
        self.nodes.append(Node.Node(s, x, y))


