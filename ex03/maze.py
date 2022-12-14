import tkinter as tk
import maze_maker as mm

from tkinter import messagebox

def key_down(event):
    global key
    key = event.keysym
    
def key_up(event):
    global key
    key = ""
    
def main_proc():
    global mx, my, cx, cy
    if key == "Up":
        my -= 1
    if key == "Down":
        my += 1
    if key == "Left":
        mx -= 1
    if key == "Right":
        mx += 1

    if maze_lst[my][mx] == 0:
        cx, cy = mx*100+50, my*100+50
    else:
        if key == "Up":
            my += 1
        if key == "Down":
            my -= 1
        if key == "Left":
            mx += 1
        if key == "Right":
            mx -= 1
          
    canv.coords("tori", cx, cy)
    root.after(100, main_proc)
    
def click_close():
    if messagebox.askokcancel("確認", "本当に閉じていいですか？"):
        root.destroy()
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("10秒迷路")
    canv = tk.Canvas(width=1500, height=900, bg="pink")
    canv.pack()
    maze_lst = mm.make_maze(15, 9)
    mm.show_maze(canv, maze_lst)
    
    print(maze_lst)
    tori = tk.PhotoImage(file="fig/10.png")
    knife = tk.PhotoImage(file="fig/knife.png")
    mx, my = 1, 1
    cx, cy = mx*100+50, my*100+50
    canv.create_image(cx, cy, image=tori, tag="tori")
    canv.create_image(1450, 750, image=knife, tag="knife")
    
    key = ""
    
    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)
    
    main_proc()
    root.protocol("WM_DELETE_WINDOW", click_close)
    root.after(10000, root.destroy)
    root.mainloop()
    
    #abc