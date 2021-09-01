
import math

import PlacementNode


class Bot:
    unclaimedNodes = []     # which nodes are not yet claimed
    placeableNodesLeft = 0  # placeable nodes remaining
    lastNode = 0            # which node was placed last
    nodesInRange = []       # all unclaimed nodes in range

    map = 0
    oldScale = 0

    def __init__(self, m):
        self.map = m
        self.unclaimedNodes = self.map.nodes
        self.placeableNodesLeft = self.map.maxPlacementNodes
        self.lastNode = PlacementNode.PlacementNode(self.map.start[0], self.map.start[1])

    def botGo(self):

        while len(self.unclaimedNodes) > 0 and self.placeableNodesLeft > 0:
            placementOptions = self.checkBestPlace()

            if len(placementOptions) == 0:
                self.oldScale += 1
            else:
                self.placeNode(placementOptions[0])

    def checkBestPlace(self):

        self.nodesInRange = checkInRangeOfNode(
            self.lastNode, self.unclaimedNodes, self.map.scale+self.oldScale)
        allNodesInRange = self.nodesInRange
        if len(allNodesInRange) > 1:
            placeOptions = self.checkDistBetweenNodesInRange(self.lastNode, self.unclaimedNodes)
            return convertToPlacements(sortBest(self.checkMultiple(placeOptions)))
        elif len(allNodesInRange) == 1:
            if self.oldScale > 0:
                self.oldScale -= 1
            return [self.furthestOutOneNode(self.lastNode, allNodesInRange[0])]
        else:
            return []

    def placeNode(self, placementNode):
        if not self.placeableNodesLeft:
            return 0    # didnt place node

        self.map.placements.append(placementNode)
        self.lastNode = placementNode
        self.placeableNodesLeft -= 1

        for node in self.unclaimedNodes:
            if distance(self.map.placements[len(self.map.placements) - 1], node) <= self.map.radius:
                self.unclaimedNodes.pop(self.unclaimedNodes.index(node))
        return 1    # placed node

    def furthestOutOneNode(self, starNode, finnishNode):

        opposite = finnishNode.pos[0] - starNode.pos[0]
        adjacent = finnishNode.pos[1] - starNode.pos[1]

        if not opposite or not adjacent:
            angle = 0
        else:
            angle = math.atan(opposite / adjacent)

        x = starNode.pos[0] + math.sin(angle) * self.map.scale
        y = starNode.pos[1] + math.cos(angle) * self.map.scale
        x = round(x, 4)
        y = round(y, 4)

        return PlacementNode.PlacementNode(x, y)

    def checkMultiple(self, placeOptions):
        unsortedMultiples = [placeOptions[0]]

        for pair in placeOptions[1:]:
            placed = 0
            for link in unsortedMultiples:

                duplicate = 0
                for node in link:
                    if node == pair[0]:
                        duplicate += 1
                    elif node == pair[1]:
                        duplicate += 1

                if duplicate != 2:
                    for node in link:
                        placeable = 0
                        if node == pair[0]:
                            placeable = self.returnIfPlacable(pair[1], link)
                        elif node == pair[1]:
                            placeable = self.returnIfPlacable(pair[0], link)
                        if placeable:
                            placed = 1
                            unsortedMultiples[unsortedMultiples.index(link)].append(placeable)
                            break
                else:
                    placed = 1
            if not placed:
                unsortedMultiples.append(pair)

        return unsortedMultiples

    def returnIfPlacable(self, node, link):
        size = len(link)
        xPos = 0
        yPos = 0

        for fNode in link:
            xPos += self.unclaimedNodes[self.unclaimedNodes.index(fNode)].pos[0]
            yPos += self.unclaimedNodes[self.unclaimedNodes.index(fNode)].pos[1]
        xPos = (xPos + self.unclaimedNodes[self.unclaimedNodes.index(node)].pos[0]) / (size + 1)
        yPos = (yPos + self.unclaimedNodes[self.unclaimedNodes.index(node)].pos[1]) / (size + 1)

        potentialLinks = link.copy()
        potentialLinks.append(node)

        inRange = checkInRangeOfNode(PlacementNode.PlacementNode(xPos, yPos), potentialLinks, self.map.radius)

        if len(link) == len(inRange):
            return 0
        else:
            return node

    # Goes through every node that is in range and checks the distance to all the other nodes
    # This is to check the best place to place a node to reach as many nodes as possible
    def checkDistBetweenNodesInRange(self, lastNode, unclaimedNodes):
        self.nodesInRange = checkInRangeOfNode(lastNode, unclaimedNodes, self.oldScale + self.map.radius)
        placeOptions = []
        # n = len(nodesInRange) * (len(nodesInRange) - 1) / 2

        fNode = len(self.nodesInRange)
        while fNode > 0:

            sNode = (fNode - 1)
            while sNode > 0:

                dist = distance(self.nodesInRange[fNode - 1], self.nodesInRange[sNode - 1])
                if dist <= self.map.radius * 2:
                    placeOptions.append([self.unclaimedNodes[fNode - 1], self.unclaimedNodes[sNode - 1]])
                sNode -= 1
            fNode -= 1

        return placeOptions


def convertToPlacements(sortedNodes):
    placements = []

    for nodes in sortedNodes:
        xPos = 0.0
        yPos = 0.0
        for node in nodes:
            xPos += node.pos[0]
            yPos += node.pos[1]
        xPos = xPos / len(nodes)
        yPos = yPos / len(nodes)
        xPos = round(xPos, 4)
        yPos = round(yPos, 4)
        placements.append(PlacementNode.PlacementNode(xPos, yPos))

    return placements


def sortBest(unsorted):
    sortedNodes = [unsorted[0]]

    for nodes in unsorted[1:]:
        for sortNodes in sortedNodes:
            if len(nodes) > len(sortNodes):
                sortedNodes.insert(sortedNodes.index(sortNodes), nodes)
            elif (len(sortedNodes) - 1) == sortedNodes.index(sortNodes):
                sortedNodes.append(nodes)

    return sortedNodes


def checkInRangeOfNode(centerNode, nodes, radius):
    inRange = []

    for node in nodes:
        if distance(centerNode, node) <= radius:
            inRange.append(node)

    return inRange


def distance(startNode, finnishNode):
    return math.sqrt((finnishNode.pos[0] - startNode.pos[0]) ** 2
                     + (finnishNode.pos[1] - startNode.pos[1]) ** 2)
