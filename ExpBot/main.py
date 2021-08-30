import Map
import PlacementBot

world = Map.Map([0, 0], 1, 1, 1)
# start coords, scale, radius, maxPlacementNodes

# world.createNode(1, 1, 1)
# weight(currently does nothing), x, y

world.createNode(1, 0.2, 0.4)
world.createNode(1, 0.5, 0.6)
world.createNode(1, 0.5, 0.3)

bot = PlacementBot.Bot(world)
bot.botGo()

for node in bot.map.placements:
    print(node.pos)
