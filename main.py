UP_COST = 1
DOWN_COST = 1
LEFT_COST = 2
RIGHT_COST = 2
EXPANSION_COUNT = 10


class Game:
    def __init__(self):                                                                                     # !!! FUNCTIONAL REQUIREMENT - 1
        self.initialState = self.getState("Initial")                                                        #
        self.goalState = self.getState("Goal")                                                              #
        self.directions = {"UP": UP_COST, "DOWN": DOWN_COST, "LEFT": LEFT_COST, "RIGHT": RIGHT_COST}
    
    def getState(self, name):
        print(f"Enter the {name} State as a 3x3 grid (0 for empty tiles) (Use space between tiles)")
        grid = []
        for i in range(3):
            userInput = input("")
            row = [int(tile) for tile in userInput.strip().split()]
            if len(row) != 3:
                print("Each row must have 3 tiles")
                exit()
            grid.append(row)
        print()
        return State(grid)
    
    def findTile(self, state, value):
        for row in state.tiles:
            for tile in row:
                if (tile.value == value):
                    return tile
    
    def getTilesInOrder(self, state):                                                                       # !!! FUNCTIONAL REQUIREMENT - 3
        tiles = [tile for row in state.tiles for tile in row if tile.value != 0]
        tiles.sort(key=lambda tile: tile.value)
        return tiles
    
    def isGoalState(self, state):
        return state.toGrid() == self.goalState.toGrid()
    
    def heuristic(self, state):
        return sum(
            [tile.getManhattanDistance(self.findTile(self.goalState, tile.value)) 
             for row in state.tiles 
             for tile in row 
             if tile.value != 0]
            )
    
    def printActions(self, state):
        path = []
        while state:
            if state.action:
                path.append(state.action)
            state = state.parent
        path.reverse()
        print("Solution Path:")
        print("---------")
        for i in path:
            print(i)
        print("---------")

    def aStar(self):                                                                                        # !!! FUNCTIONAL REQUIREMENT - 5
        print()
        
        expansionCount = 1

        queue = []
        visitedStates = set()

        initialHeuristic = self.heuristic(self.initialState)                                                # !!! FUNCTIONAL REQUIREMENT - 5
        queue.append((initialHeuristic, 0, self.initialState, None))  # ( f(n), g(n), State, Tile )

        # print(f"F: {initialHeuristic}, G: 0")
        print("Initial State")
        print(self.initialState)

        while queue and expansionCount <= EXPANSION_COUNT+1:                                                # !!! FUNCTIONAL REQUIREMENT - 6
            queue.sort(key=lambda pair: pair[0])
            currentF, currentG, currentState, movedTile = queue.pop(0)

            if expansionCount > 1:
                # print(f"F: {currentF}, G: {currentG}")
                print(f"#{expansionCount-1} Step: move Tile#{movedTile} (from #{currentState.step} Step)")  # !!! FUNCTIONAL REQUIREMENT - 3
                print(currentState)                                                                         # !!! FUNCTIONAL REQUIREMENT - 6

            if self.isGoalState(currentState):                                                              # !!! FUNCTIONAL REQUIREMENT - 6
                print(f"Solution found: #{expansionCount-1} Expansion")
                self.printActions(currentState)
                return
            
            for tile in self.getTilesInOrder(currentState):                                                 # !!! FUNCTIONAL REQUIREMENT - 3

                for direction, cost in self.directions.items():
                    newState = State(currentState.toGrid(), currentState, expansionCount-1)
                    success = newState.move(tile, direction)
                    newState.action = f"#{tile} -> {direction}"

                    if not success:
                        continue

                    G = currentG+cost
                    H = self.heuristic(newState)                                                            # !!! FUNCTIONAL REQUIREMENT - 5
                    F = G + H

                    if str(newState.toGrid()) in visitedStates:
                        continue

                    visitedStates.add(str(newState.toGrid()))
                    queue.append((F, G, newState, tile))

            expansionCount += 1
        
        print(f"No solution found")


class State:
    def __init__(self, state, parent=None, step=0):
        self.tiles = [[Tile(x, y, state[x][y]) for y in range(3)] for x in range(3)]
        self.parent = parent
        self.step = step
        self.action = None

    def toGrid(self):
        return [[self.tiles[x][y].value for y in range(3)] for x in range(3)]

    def swap(self, tile, other):
        self.tiles[tile.x][tile.y].value, self.tiles[other.x][other.y].value = other.value, tile.value

    def move(self, tile, direction):                                                                        # !!! FUNCTIONAL REQUIREMENT - 2
        if direction == "UP" and tile.x > 0:
            neighbourTile = self.tiles[tile.x-1][tile.y]
        elif direction == "DOWN" and tile.x < 2:
            neighbourTile = self.tiles[tile.x+1][tile.y]
        elif direction == "RIGHT" and tile.y < 2:
            neighbourTile = self.tiles[tile.x][tile.y+1]
        elif direction == "LEFT" and tile.y > 0:
            neighbourTile = self.tiles[tile.x][tile.y-1]
        else:
            return False
        
        self.swap(tile, neighbourTile)
        return True
    
    def __str__(self):
        txt = "\n"
        for row in self.tiles:
            txt += "[ "
            for tile in row:
                txt += f"{tile} "
            txt += "]\n"
        return txt


class Tile:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
    
    def getManhattanDistance(self, other):                                                                  # !!! FUNCTIONAL REQUIREMENT - 5
        return abs(self.x-other.x)+abs(self.y-other.y)                                                      #

    def __str__(self):
        return f"{self.value}"


if __name__ == "__main__":
    game = Game()
    game.aStar()
    