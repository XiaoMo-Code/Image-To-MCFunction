from PIL import Image
import re
def tickingarea(raw_bool,maxX,maxY,file_path,boolean):
    if not boolean: return None
    img = Image.open(file_path).convert('RGBA')
    try:
        ow, oh = img.size
        mx, my = img.size
        try: mx = int(maxX)
        except: pass
        try: my = int(maxY)
        except: pass
        ratioX, ratioY = mx / ow, my / oh
        img = img.resize((int(ow * ratioX), int(oh * ratioY)), Image.LANCZOS)
    except: pass
    X , Y = img.size
    print('creatTickingarea', X, Y, raw_bool)
    cr = '/' if raw_bool else ''
    CountX = int(X / 140 +1)
    CountY = int(Y / 140 +1)
    countAll , lines , line = 0 , {} , 0
    if CountX != 1 and CountY != 1:
        for countX in range(1,CountX):
            for countY in range(1,CountY+1):
                line = 140 * X * (countX - 1) + 140 * (countY - 1) + len(lines)
                lines[line] = []
                if countY != 1 or countX != 1:
                    lines[line].append(f'{cr}tickingarea remove ITM_tick{countAll-1}')
                lines[line].append(f'{cr}tickingarea add ~{countY*140} ~ ~{countX*140} ~{(countY-1)*140} ~ ~{(countX-1)*140} ITM_tick{countAll} true')
                countAll += 1
    elif CountX == 1 and CountY == 1: lines = {0:[f'{cr}tickingarea add ~0 ~ ~0 ~140 ~ ~140 ITM_tick0 true']}
    elif CountY == 1 and CountX != 1:
        for countX in range(1,CountX+1):
            line = 140 * X * (countX - 1) + len(lines)
            lines[line] = []
            if countX != 1:
                lines[line].append(f'{cr}tickingarea remove ITM_tick{countAll-1}')
            lines[line].append(f'{cr}tickingarea add ~{countX*140} ~ ~0 ~{(countX-1)*140} ~ ~140 ITM_tick{countAll} true')
            countAll += 1
    return lines
def setCode(commands,ticks):
    commandList = re.findall(r'(.*?)\n', commands+'\n',re.S)
    counter = 0
    command = ''
    for com in commandList:
        command += com + '\n'
        if counter in ticks:
            command += f'{ticks[counter][0]}\n'
            if len(ticks[counter]) != 1:
                command += f'{ticks[counter][1]}\n'
        counter += 1
    return command
if __name__ == "__main__":
    raw_bool = False
    maxX = 512
    maxY = 51
    file_path = "./icon.ico"
    list = tickingarea(raw_bool,maxX,maxY,file_path,True)
    print(*list.values(),sep='\n')
else:
    print(f'{__name__} enabled')