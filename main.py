import tkinter as tk
import sys
from src.itm_app import ITMApp
def main():
    root = tk.Tk()
    app = ITMApp(root)
    root.geometry('800x530+380+150')
    root.iconbitmap(sys.argv[0])
    root.attributes('-topmost', True)
    app.after()
    root.mainloop()
if __name__ == '__main__':
    main()
else:
    print(f'{__name__} enabled')