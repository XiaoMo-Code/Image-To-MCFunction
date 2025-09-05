import re
def optimize(command,rawCommand):
    cr = ''
    if rawCommand:cr = '/'
    allCommands = command.split('\n')
    setblockCommands = []
    otherCommands = []
    for cmd in allCommands:
        if cmd.strip() and not cmd.strip().startswith(f'{cr}tickingarea remove'):
            if 'setblock' in cmd:
                setblockCommands.append(cmd)
            else:
                otherCommands.append(cmd)
    commandList = re.findall(r'setblock ~(-?\d+) ~ ~(-?\d+) (\S+) \[\]', '\n'.join(setblockCommands))
    blocksData = {}
    for x, z, blockName in commandList:
        x, z = int(x), int(z)
        blocksData[(x, z)] = blockName
    optimizedCommands = []
    visitedCoords = set()
    sortedCoords = sorted(blocksData.keys(), key=lambda coord: (coord[1], coord[0]))
    for coord in sortedCoords:
        if coord in visitedCoords:
            continue
        x, z = coord
        blockName = blocksData[coord]
        maxWidth = 1
        maxHeight = 1
        while (x + maxWidth, z) in blocksData and blocksData[(x + maxWidth, z)] == blockName:
            maxWidth += 1
        canExpandDown = True
        currentHeight = 1
        while canExpandDown:
            for w in range(maxWidth):
                checkCoord = (x + w, z + currentHeight)
                if checkCoord not in blocksData or blocksData[checkCoord] != blockName:
                    canExpandDown = False
                    break
            if canExpandDown:
                currentHeight += 1
        maxHeight = currentHeight
        for w in range(maxWidth):
            for h in range(maxHeight):
                visitedCoords.add((x + w, z + h))
        if maxWidth > 1 or maxHeight > 1:
            endX = x + maxWidth - 1
            endZ = z + maxHeight - 1
            optimizedCommands.append(f'{cr}fill ~{x} ~ ~{z} ~{endX} ~ ~{endZ} {blockName}')
        else:
            optimizedCommands.append(f'{cr}setblock ~{x} ~ ~{z} {blockName} []')
    finalCommands = otherCommands + optimizedCommands
    return '\n'.join(finalCommands)
if __name__ == '__main__':
    testCommands = '''/setblock ~0 ~ ~0 stone []
/setblock ~0 ~ ~1 stone []
/setblock ~1 ~ ~0 stone []
/tickingarea add ~0 ~ ~0 ~140 ~ ~140 ITM_tick0 true
/tickingarea remove ITM_tick1'''
    result = optimize(testCommands, True)
    print(result)
else:
    print(f'{__name__} enabled')