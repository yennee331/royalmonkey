from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font
import os
import pygame

pygame.init()
canvas_width = 800
canvas_height = 400

root = Tk()
root.title("Egg Catcher")
c = Canvas(root, width=canvas_width, height=canvas_height, background="deep sky blue")
c.create_rectangle(-5, canvas_height - 100, canvas_width + 5, canvas_height + 5, fill="sea green", width=0)
c.create_oval(-80, -80, 120, 120, fill='orange', width=0)
c.pack()
color_cycle = cycle(["light blue", "light green", "light pink", "light yellow", "light cyan"])
bomb_width = 40
bomb_height = 50
bomb_interval = 4000
bomb_speed = 50
egg_width = 45
egg_height = 55
egg_score = 10 
bomb_penalty = 1 
egg_speed = 50
egg_interval = 4000
difficulty = 1.0
catcher_color = "blue"
catcher_width = 100
catcher_height = 100
catcher_startx = canvas_width / 2 - catcher_width / 2
catcher_starty = canvas_height - catcher_height - 20
catcher_startx2 = catcher_startx + catcher_width
catcher_starty2 = catcher_starty + catcher_height

background_music = os.path.join('project', 'Music', 'Chicken.mp3')
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)

catcher = c.create_arc(catcher_startx, catcher_starty, catcher_startx2, catcher_starty2,
                       start=200, extent=140, style="arc", outline=catcher_color, width=3)
game_font = font.nametofont("TkFixedFont")
game_font.config(size=18)

score = 0
score_text = c.create_text(10, 10, anchor="nw", font=game_font, fill="darkblue", text="Score: " + str(score))

lives_remaining = 3
lives_text = c.create_text(canvas_width - 10, 10, anchor="ne", font=game_font, fill="darkblue",
                           text="Lives: " + str(lives_remaining))

eggs = []
bombs = []

def create_bomb():
    x = randrange(10, 700)
    y = 40
    new_bomb = c.create_oval(x, y, x + bomb_width, y + bomb_height, fill='black', outline='black')
    bombs.append(new_bomb)
    root.after(bomb_interval, create_bomb)

def move_bombs():
    for bomb in bombs:
        (bombx, bomby, bombx2, bomby2) = c.coords(bomb)
        c.move(bomb, 0, 10)
        if bomby2 > canvas_height:
            bomb_dropped(bomb)
        elif catcher_caught_bomb(bomb):
            bomb_caught(bomb)
    root.after(bomb_speed, move_bombs)

def bomb_dropped(bomb):
    bombs.remove(bomb)
    c.delete(bomb)

def bomb_caught(bomb):
    bombs.remove(bomb)
    c.delete(bomb)
    lose_a_life()  

def create_egg():
    x = randrange(10, 740)
    y = 40
    new_egg = c.create_oval(x, y, x + egg_width, y + egg_height, fill=next(color_cycle), width=0)
    eggs.append(new_egg)
    root.after(egg_interval, create_egg)

def move_eggs():
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg)
        c.move(egg, 0, 10)
        if eggy2 > canvas_height:
            egg_dropped(egg)
        elif catcher_caught_egg(egg):
            egg_caught(egg)
    root.after(egg_speed, move_eggs)

def egg_dropped(egg):
    eggs.remove(egg)
    c.delete(egg)
    decrease_score(egg_score)

def egg_caught(egg):
    eggs.remove(egg)
    c.delete(egg)
    increase_score(egg_score)

def lose_a_life():
    global lives_remaining
    lives_remaining -= 1
    c.itemconfigure(lives_text, text="Lives: " + str(lives_remaining))
    if lives_remaining == 0:
        messagebox.showinfo("Game Over!", "Final Score: " + str(score))
        root.destroy()

def catcher_caught_egg(egg):
    (catcherx, catchery, catcherx2, catchery2) = c.coords(catcher)
    (eggx, eggy, eggx2, eggy2) = c.coords(egg)
    return catcherx < eggx and eggx2 < catcherx2 and catchery2 - eggy2 < 40

def catcher_caught_bomb(bomb):
    (catcherx, catchery, catcherx2, catchery2) = c.coords(catcher)
    (bombx, bomby, bombx2, bomby2) = c.coords(bomb)
    return catcherx < bombx and bombx2 < catcherx2 and catchery2 - bomby2 < 40

def increase_score(points):
    global score
    score += points
    c.itemconfigure(score_text, text="Score: " + str(score))

def decrease_score(points):
    global score
    score -= points
    c.itemconfigure(score_text, text="Score: " + str(score))

def move_left(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x1 > 0:
        c.move(catcher, -20, 0)

def move_right(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher, 20, 0)

c.bind("<Left>", move_left)
c.bind("<Right>", move_right)
c.focus_set()

root.after(1000, create_egg)
root.after(1000, move_eggs)
root.after(1000, create_bomb)
root.after(1000, move_bombs)

root.mainloop()