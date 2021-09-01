import math

import Map
import PlacementBot


world = Map.Map([1, 1], 1, 1, 3)
# start coords, scale, radius, maxPlacementNodes

# world.createNode(1, 1, 1)
# weight(currently does nothing), x, y

world.createNode(1, 1, 4)

bot = PlacementBot.Bot(world)
bot.botGo()

for node in bot.map.placements:
    print(node.pos)
print(bot.unclaimedNodes)
print(bot.placeableNodesLeft)

print(math.sqrt((1 - 0.7276) ** 2 + (4 - 2.9103) ** 2))
