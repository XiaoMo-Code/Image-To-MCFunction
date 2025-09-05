import tkinter as tk
from tkinter import  messagebox as message, filedialog as file
from PIL import ImageTk, Image
from .color_themes import COLOR_THEMES
from .block_rgbdata import blockrgbdata
from .ui_utils import make_rounded_canvas,get_font,getImage,showTips
from .tickingareaGet import tickingarea as tickGet,setCode
from .optimize import optimize
from .app_info import __version__
import requests , os
class ITMApp:
    def __init__(self, root):
        self.root = root
        self.colors = COLOR_THEMES['black'].copy()
        self.colorFile = 'dark_sw_icon.jpg'
        self.swURL = 'https://c-ssl.dtstatic.com/uploads/blog/202311/15/B8SVZ252HlwblBZ.thumb.1000_0.jpg'
        self.geometry = ''
        self.imageSizeX = self.imageSizeY = 0
        self.maxX = self.maxY = self.inputImport = self.inputSave = ''
        self.global_image_ref = None
        self.canGetRGB = False
        self.timer_id = self.fadeID = None
        self.inputImportFile = self.inputSaveFile = self.saveSizeX = self.saveSizeY = self.canvas = self.button_convert = self.frame = self.sw = None
        self.skip_transparent = True
        self.commandRaw = False
        self.tick_area = True
        self.optimize_btn = False
        self.sizeText = None
        self.initWindow()
    def create_rounded_button(self, root, x, y, width, height, radius, color, text, command, convert=False):
        canvas = make_rounded_canvas(root, x, y, width, height, radius,self.colors['outline'], self.colors['btn_color'], 5, color, 2, bg=self.colors['frame'])
        btn_text = text+'\nConvert' if convert else text
        btn_fg = self.colors['convert_btn'] if convert else color
        btn_font = (None,20,'bold') if convert else None
        btn = tk.Button(root, text=btn_text, font=btn_font, bd=0, fg=btn_fg, highlightthickness=0,bg=self.colors['btn_color'], activebackground=self.colors['click_btn'], command=command)
        canvas.create_window(width//2, height//2, window=btn, width=width-4, height=height-4)
        return canvas, btn
    def create_rounded_entry(self, root, x, y, width, height, radius, color, thickness, placeholder=""):
        canvas = make_rounded_canvas(root, x, y, width, height, radius,self.colors['outline'], self.colors['entry_fill'], 5, color, thickness, bg=self.colors['frame'])
        entry = tk.Entry(root, bd=0, highlightthickness=0, bg=self.colors['entry_fill'])
        canvas.create_window(width//2, height//2, window=entry, width=width-20)
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=self.colors['entry_in'])
        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg=self.colors['entry_out'])
        entry.insert(0, placeholder)
        entry.config(fg=self.colors['color1'])
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        return canvas, entry
    def select_file(self, entry, save=False):
        filename = file.asksaveasfilename() if save else file.askopenfilename()
        if filename:
            entry.delete(0, tk.END)
            entry.insert(0, filename.replace('/', '\\'))
    def getRGB(self):
        image_path = self.inputImportFile.get()
        if not self.canGetRGB: return None
        sizeX = self.saveSizeX.get()
        sizeY = self.saveSizeY.get()
        imgInfo = getImage(image_path,sizeX,sizeY,info=True)
        img = imgInfo['image']
        pixels = img.load()
        w, h = img.size
        if self.skip_transparent:return [{'rgb': pixels[x, y][:3], 'position': [x, y]} for y in range(h) for x in range(w) if pixels[x, y][3] != 0]
        else:return [{'rgb': pixels[x, y][:3], 'position': [x, y]} for y in range(h) for x in range(w)]
    def getBlocks(self):
        rgb_data = self.getRGB()
        if not rgb_data: return None
        result = []
        for item in rgb_data:
            pixel_rgb = item['rgb']
            nearest = min(blockrgbdata.items(),key=lambda kv: sum((pixel_rgb[i] - kv[1][i]) ** 2 for i in range(3)))
            result.append({nearest[0]: item['position']})
        return result
    def startWindow(self):
        self.root.geometry(self.geometry)
        self.root.title('IMT')
    def start(self):
        path = self.inputSaveFile.get()
        try:
            with open(path, 'w', encoding='utf-8') as f:f.close()
            if self.tick_area:ticks = tickGet(self.commandRaw,self.saveSizeX.get(),self.saveSizeY.get(),self.inputImportFile.get(),self.canGetRGB)
            dicts = self.getBlocks()
            cr = '/' if self.commandRaw else ''
            fileText = ''.join(f'{cr}setblock ~{i[k][0]} ~ ~{i[k][1]} {k} []\n' for i in dicts for k in i)
            if self.tick_area:
                try:fileText = setCode(fileText,ticks).replace('\n\n','\n')
                except:pass
            if self.optimize_btn:
                try:fileText = optimize(fileText,self.commandRaw)
                except:pass
            with open(path, 'a', encoding='utf-8') as f:f.write(fileText)
            self.root.after(ms=1000, func=self.startWindow)
        except:
            self.root.after(ms=1000, func=self.startWindow)
            message.showerror(title='打包', message='导出失败！')
    def saveToFunction(self):
        self.geometry = self.root.geometry()
        self.root.geometry('100x100+10000+10000')
        self.root.after(ms=50, func=self.start)
    def after(self):
        try:
            self.canvas.delete("all")
            path = self.inputImportFile.get()
            try:
                img = getImage(path,info=True)
                img_pil = img['image']
                ow, oh = img['rawSize']
                ratio = min(340 / ow, 340 / oh)
                new_size = (int(ow * ratio), int(oh * ratio))
                resized_img = img_pil.resize(new_size, Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(resized_img)
                self.global_image_ref = img_tk
                x = (340 - new_size[0]) // 2
                y = (340 - new_size[1]) // 2
                self.canvas.create_image(x+2, y+2, anchor=tk.NW, image=img_tk)
                self.canGetRGB = True
                mx, my = ow, oh
            except:
                self.canGetRGB = False
                mx = my = 0
            try: mx = int(self.saveSizeX.get())
            except: pass
            try: my = int(self.saveSizeY.get())
            except: pass
            self.imageSizeX, self.imageSizeY = mx, my
            self.button_convert['text'] = f'开 始 转 换\n{mx}×{my}'
            self.sizeText.text = f'大小 {self.imageSizeX} * {self.imageSizeY}'
        except: pass
        self.root.after(50, self.after)
    def getInput(self):
        self.maxX = self.saveSizeX.get()
        self.maxY = self.saveSizeY.get()
        self.inputSave = self.inputSaveFile.get()
        self.inputImport = self.inputImportFile.get()
    def turnColor(self, event):
        self.getInput()
        self.colors = COLOR_THEMES['black' if self.colors['colorStyle'] == 'white' else 'white'].copy()
        if self.colors['colorStyle'] == 'black':
            self.colorFile = 'dark_sw_icon.jpg'
            self.swURL = 'https://c-ssl.dtstatic.com/uploads/blog/202311/15/B8SVZ252HlwblBZ.thumb.1000_0.jpg'
        else:
            self.colorFile = 'light_sw_icon.jpg'
            self.swURL = 'https://b0.bdstatic.com/ugc/THz0VIn4KuzU3ef2eMxYdA0ad12b29accbec4a7c421e748dfafe10.jpg'
        self.initWindow()
        return event
    def show_theme_menu(self, event):
        menu = tk.Menu(self.frame, tearoff=False)
        menu.configure(bg = self.colors['frame'],fg = self.colors['title_font'],activebackground = self.colors['btn_bg'],activeforeground = self.colors['btn_color'])
        skip_transparent_text = f"跳过透明 {'✔' if self.skip_transparent else '✘'}"
        commandRaw = f"添加斜杠 {'✔' if self.commandRaw else '✘'}"
        tick_area = f"常加载区 {'✔' if self.tick_area else '✘'}"
        tick_refine = f"二维优化 {'✔' if self.optimize_btn else '✘'}"
        colorStyle = f"{'浅色' if self.colors['colorStyle'] == 'black' else '深色'}模式"
        def toggle_tick_area():self.tick_area = not self.tick_area
        def toggle_skip_transparent():self.skip_transparent = not self.skip_transparent
        def toggle_command_raw():self.commandRaw = not self.commandRaw
        def toggle_tick_refine():self.optimize_btn = not self.optimize_btn
        menu.add_command(label=colorStyle, command = lambda: self.turnColor(event))
        menu.add_separator()
        menu.add_command(label=skip_transparent_text, command=toggle_skip_transparent)
        menu.add_command(label=commandRaw, command=toggle_command_raw)
        menu.add_command(label=tick_area, command=toggle_tick_area)
        menu.add_command(label=tick_refine, command=toggle_tick_refine)
        menu.tk_popup(event.x_root, event.y_root)
    def initWindow(self, event=None):
        try: self.frame.destroy()
        except: pass
        try: self.sw.destroy()
        except: pass
        self.frame = tk.Frame(self.root, width=800, height=530, bg=self.colors['frame'])
        self.frame.place(x=0, y=0)
        self.root.overrideredirect(True)
        self.root.geometry("800x530")
        if self.geometry: self.root.geometry(self.geometry)
        title = tk.Frame(self.frame, width=800, height=30, bg=self.colors['title'])
        title.place(x=0, y=0)
        def motion(event):
            if hasattr(motion, 'start_x') and hasattr(motion, 'start_y'):
                x = self.root.winfo_x() + (event.x - motion.start_x)
                y = self.root.winfo_y() + (event.y - motion.start_y)
                self.root.geometry(f"+{x}+{y}")
        def start_move(event): motion.start_x, motion.start_y = event.x, event.y
        def stop_move(event):
            if hasattr(motion, 'start_x'): del motion.start_x
            if hasattr(motion, 'start_y'): del motion.start_y
            return event
        def quit(event): self.root.destroy(); return event
        def intoEventClose(event): close['bg'] = '#ee7777'; return event
        def leaveEventClose(event): close['bg'] = self.colors['title']; return event
        def intoEventSW(event): smWindow['bg'] = '#ee7777'; return event
        def leaveEventSW(event): smWindow['bg'] = self.colors['title']; return event
        title.bind("<ButtonPress-1>", start_move)
        title.bind("<ButtonRelease-1>", stop_move)
        title.bind("<B1-Motion>", motion)
        label = tk.Label(title, bg=self.colors['title'])
        try:
            url = 'https://c-ssl.dtstatic.com/uploads/blog/202311/15/B8SVZ252HlwblBZ.thumb.1000_0.jpg' if self.colors['colorStyle'] == 'white' else 'https://b0.bdstatic.com/ugc/THz0VIn4KuzU3ef2eMxYdA0ad12b29accbec4a7c421e748dfafe10.jpg'
            file = 'dark_title.jpg' if self.colors['colorStyle'] == 'black' else 'light_title.jpg'
            fileName = f"{os.environ.get('TEMP') or os.environ.get('TMP')}/{file}"
            if not os.path.exists(fileName):
                response = requests.get(url)
                with open(fileName, 'wb+') as f:
                    f.write(response.content)
                    f.close()
            img = getImage(fileName,26,26)
            img_tk = ImageTk.PhotoImage(img)
            self.global_image_ref = img_tk
            label.config(image=img_tk, text='')
            label.place(x=2, y=2, width=26, height=26)
        except Exception as e:
            label.config(image='', text='[ITM]', font=get_font(60), fg=self.colors['ITMText'])
            label.place(x=-3, y=2, width=26, height=26)
        text = tk.Label(title, text='你好呀~欢迎使用哦！', font=get_font(25), bg=self.colors['title'], fg=self.colors['title_font'])
        text.place(x=35, y=5)
        for w in (text,label):
            w.bind("<ButtonPress-1>", start_move)
            w.bind("<ButtonRelease-1>", stop_move)
            w.bind("<B1-Motion>", motion)
        close = tk.Label(title, text='X', font=get_font(33), bg=self.colors['title'], fg=self.colors['title_font'], width=2)
        close.bind('<Button-1>', quit)
        close.bind('<Enter>', intoEventClose)
        close.bind('<Leave>', leaveEventClose)
        close.place(x=760, y=-3)
        smWindow = tk.Label(title, text='O', font=get_font(33), bg=self.colors['title'], fg=self.colors['title_font'], width=2)
        smWindow.bind('<Button-1>', self.smallWindow)
        smWindow.bind('<Enter>', intoEventSW)
        smWindow.bind('<Leave>', leaveEventSW)
        smWindow.place(x=720, y=-3)
        _, self.button_convert = self.create_rounded_button(self.frame, 440, 380, 200, 90, 10, self.colors['color1'], "开 始 转 换", self.saveToFunction, convert=True)
        self.sizeText = showTips(self.root, self.button_convert, f'大小 {self.imageSizeX} * {self.imageSizeY}', self.colors['title_font'], self.colors['frame'],(None,10,'bold'))
        label_cfg = [
            ('Image', 200, 450, 'name',get_font(50)), ('To', 260, 520, 'name',get_font(50)), ('MCFunction', 320, 480, 'name',get_font(50)),
            ('+', 260, 420, 'font1',get_font(50)), ('+', 240, 650, 'font2',get_font(50)), ('+', 380, 660, 'font3',get_font(50)),
            ('+', 320, 760, 'font1',get_font(50)), ('+', 150, 620, 'font4',get_font(50)), ('+', 170, 420, 'font4',get_font(50)), 
            ('+', 180, 720, 'font4',get_font(50)),('画布大小 340×340', 505, 130, 'pis_size',(None, 12, 'bold')),
            ('图像位置:',40,250,'entry_font',get_font(30)),('导出路径:',100,250,'entry_font',get_font(30)),
            ('长:',40,20,'entry_font',get_font(30)),('宽:',100,20,'entry_font',get_font(30)),(f'Version {__version__}', 510, 675, 'name',get_font(10,underline=True))
        ]
        for text, y, x, color, font in label_cfg:
            lbl = tk.Label(self.frame, text=text, font=font, bg=self.colors['frame'], fg=self.colors[color])
            lbl.place(y=y, x=x)
            lbl.bind("<Button-3>", self.show_theme_menu)
            if 'Version' in text:
                showTips(self.root, lbl, text, self.colors['title_font'], self.colors['frame'],(None,10,'bold'))
        _, self.inputImportFile = self.create_rounded_entry(self.frame, 410, 43, 350, 30, 10, self.colors['color1'], 2, "选择打开文件...")
        _, _ = self.create_rounded_button(self.frame, 760, 43, 30, 30, 10, self.colors['color1'], "· · ·", lambda: self.select_file(self.inputImportFile))
        _, self.inputSaveFile = self.create_rounded_entry(self.frame, 410, 103, 350, 30, 10, self.colors['color1'], 2, "选择导出文件...")
        _, _ = self.create_rounded_button(self.frame, 760, 103, 30, 30, 10, self.colors['color1'], "· · ·", lambda: self.select_file(self.inputSaveFile, save=True))
        self.frame.bind("<Button-3>", self.show_theme_menu)
        self.canvas_sizeX, self.saveSizeX = self.create_rounded_entry(self.frame, 80, 43, 150, 30, 10, self.colors['color1'], 2, " Width X")
        self.canvas_sizeY, self.saveSizeY = self.create_rounded_entry(self.frame, 80, 103, 150, 30, 10, self.colors['color1'], 2, " Height Y")
        canva = tk.Canvas(self.frame, width=350, height=350, bg=self.colors['canvas_outline'])
        canva.place(x=40, y=150)
        self.canvas = tk.Canvas(canva, width=340, height=340, bg=self.colors['canvas_pic'])
        self.canvas.place(x=5, y=5)
        if self.maxX: self.saveSizeX.delete(0, tk.END); self.saveSizeX.insert(0, self.maxX)
        if self.maxY: self.saveSizeY.delete(0, tk.END); self.saveSizeY.insert(0, self.maxY)
        if self.inputImport: self.inputImportFile.delete(0, tk.END); self.inputImportFile.insert(0, self.inputImport)
        if self.inputSave: self.inputSaveFile.delete(0, tk.END); self.inputSaveFile.insert(0, self.inputSave)
        return event
    def smallWindow(self, event=None):
        self.getInput()
        def motion(event):
            if hasattr(motion, 'start_x') and hasattr(motion, 'start_y'):
                x = self.root.winfo_x() + (event.x - motion.start_x)
                y = self.root.winfo_y() + (event.y - motion.start_y)
                self.root.geometry(f"+{x}+{y}")
                reset_timer()
        def start_move(event): motion.start_x, motion.start_y = event.x, event.y; reset_timer()
        def stop_move(event):
            if hasattr(motion, 'start_x'): del motion.start_x
            if hasattr(motion, 'start_y'): del motion.start_y
            reset_timer(); return event
        def reset_timer():
            self.root.after_cancel(timer_id)
            self.root.attributes('-alpha', 1.0)
            start_fade_timer()
        def start_fade_timer():
            global timer_id
            timer_id = self.root.after(5000, fade_window)
        def intoWindow(event):
            global fadeID
            self.initWindow()
            try: self.root.after_cancel(fadeID)
            except: pass
            self.root.after_cancel(timer_id)
            self.root.attributes('-alpha', 1.0)
            return event
        def fade_window():
            global fadeID
            current_alpha = self.root.attributes('-alpha')
            if current_alpha > 0.6:
                self.root.attributes('-alpha', current_alpha - 0.05)
                fadeID = self.root.after(150, fade_window)
            else:self.root.attributes('-alpha', 0.6)
        self.frame.destroy()
        self.root.geometry('100x100')
        self.sw = tk.Frame(self.root, width=100, height=100, bg=self.colors['smallWindow'])
        self.sw.bind("<ButtonPress-1>", start_move)
        self.sw.bind("<ButtonRelease-1>", stop_move)
        self.sw.bind("<B1-Motion>", motion)
        if event != "I":self.sw.bind("<Double-Button-1>", intoWindow)
        self.sw.place(x=0, y=0)
        label = tk.Label(self.sw, bg=self.colors['smallWindow'])
        label.bind("<ButtonPress-1>", start_move)
        label.bind("<ButtonRelease-1>", stop_move)
        label.bind("<B1-Motion>", motion)
        if event != "I":label.bind("<Double-Button-1>", intoWindow)
        def update_icon_img():
            try:
                fileName = f"{os.environ.get('TEMP') or os.environ.get('TMP')}/{self.colorFile}"
                if not os.path.exists(fileName):
                    response = requests.get(self.swURL)
                    with open(fileName, 'wb+') as f:
                        f.write(response.content)
                        f.close()
                img = getImage(fileName,100,100)
                img_tk = ImageTk.PhotoImage(img)
                self.global_image_ref = img_tk
                label.config(image=img_tk, text='')
                label.place(x=0, y=0, width=100, height=100)
            except Exception as e:
                label.config(image='', text='ITM', font=get_font(60), fg=self.colors['ITMText'])
                label.place(x=-5, y=0, width=100, height=100)
        update_icon_img()
        if event != 'I':start_fade_timer()
        return event
if __name__ != "__main__":
    print(f'{__name__} enabled')