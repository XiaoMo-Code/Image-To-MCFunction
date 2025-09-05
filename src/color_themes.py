rawColors = {
    'ITMText': '#FF315C',
    'smallWindow':'#CCCCCC',
    'outline': '#333333',
    'btn_bg': '#AAAAAA',
    'btn_color': '#E0E0E0',
    'click_btn': '#D0D0D0',
    'convert_btn': '#777777',
    'entry_bg': '#AAAAAA',
    'entry_fill': '#E0E0E0',
    'entry_in': '#000000',
    'entry_out': '#808080',
    'title': '#D7D7D7',
    'title_font': '#333333',
    'canvas_outline': '#666666',
    'canvas_pic': '#FFFFFF',
    'entry_font': '#676767',
    'name': '#575757',
    'font1': '#A7A7A7',
    'font2': '#979797',
    'font3': '#474747',
    'font4': '#777777',
    'color1': '#808080',
    'frame': '#E7E7E7',
    'pis_size': '#878787'
}
def getOppositeColor(RGB):
    color = '#'
    red = RGB[1:3]
    green = RGB[3:5]
    blue = RGB[5:7]
    redInt = 255 - int(red, 16)
    greenInt = 255 - int(green, 16)
    blueInt = 255 - int(blue, 16)
    color += f'{redInt:02x}{greenInt:02x}{blueInt:02x}'.upper()
    return color
dic = {}
for key, value in rawColors.items():
    dic[key] = getOppositeColor(value)
COLOR_THEMES = {
    'white': {**rawColors, 'colorStyle':'white'},
    'black': {**dic, 'colorStyle':'black','canvas_pic':'#333333'}
}

if __name__ != "__main__":
    print(f'{__name__} enabled')