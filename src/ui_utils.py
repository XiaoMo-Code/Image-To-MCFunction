import tkinter as tk
from tkinter import font
from PIL import Image
def make_rounded_canvas(root, x, y, width, height, radius, outline, fill, width1, outline2=None, width2=None, bg=None):
    theme_gray = '#aaa' if outline in ('#333333', '#aaa') else '#555555'
    canvas = tk.Canvas(root, width=width, height=height, bg=bg if bg is not None else root['bg'], highlightthickness=0)
    canvas.place(x=x, y=y)
    pts = [x+radius+2, y+2, x+width-radius-2, y+2, x+width-2, y+radius+2, x+width-2, y+height-radius-2,x+width-radius-2, y+height-2, x+radius+2, y+height-2, x+2, y+height-radius-2, x+2, y+radius+2, x+radius+2, y+2]
    canvas.create_polygon(pts, outline=theme_gray, width=5, fill=fill, smooth=True)
    if outline2 and width2:
        canvas.create_polygon(pts, outline=outline2, width=width2, fill=fill, smooth=True)
    canvas.create_rectangle(0, 0, width, height, outline=theme_gray, width=6)
    return canvas
def getImage(fileName,sizeX=None,sizeY=None,info=False):
        img = Image.open(fileName).convert('RGBA')
        try:
            ow, oh = img.size
            mx, my = img.size
            try: mx = int(sizeX)
            except: pass
            try: my = int(sizeY)
            except: pass
            ratioX, ratioY = mx / ow, my / oh
            img = img.resize((int(ow * ratioX), int(oh * ratioY)), Image.LANCZOS)
        except: pass
        return img if not info else {'image':img,'newSize':[ow, oh],'rawSize':img.size}
def get_font(size,underline=False,overstrike=False,bold=True):
    return font.Font(
        family="Fixedsys", 
        size=-size, 
        weight="bold" if bold else "normal", 
        underline=underline, 
        overstrike=overstrike
    )

class showTips:
    def __init__(self, windowName, widget, text, backgroundColor, fontColor,tipFont=None):
        self.font = get_font(5) if tipFont is None else tipFont
        self.background = backgroundColor
        self.fontColor = fontColor
        self.root = windowName
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)
    def show(self, event):
        self.x = event.x + self.widget.winfo_rootx() + 20
        self.y = event.y + self.widget.winfo_rooty() + 20
        if self.tipwindow or not self.text:
            return
        self.tipwindow = tw = tk.Toplevel(self.root)
        tw.wm_overrideredirect(True)
        tw.attributes('-topmost',True)
        tw.wm_geometry("+%d+%d" % (self.x, self.y))
        if type(self.text) == str:
            t1 = self.text
        else:
            t1 = self.text['text']
        label = tk.Label(tw, text=t1, justify=tk.LEFT,background=self.background, relief=tk.SOLID, borderwidth=1,font=self.font,fg=self.fontColor)
        label.pack(ipadx=4)
    def hide(self, event):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
        return event
if __name__ != "__main__":
    print(f'{__name__} enabled')