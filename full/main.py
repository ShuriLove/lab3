import tkinter as tk
import random
import string
import pygame
import threading

def generate_key():
    num = entry.get().strip()
    if not num.isdigit() or len(num) != 6:
        key_label.config(text="Введите 6 цифр")
        return

    d1, d2, d3, d4, d5, d6 = num

    n1_str = d2 + d1 + d3      

    n2_str = d5 + d4 + d6      
    
    block1 = n1_str + "".join(random.choice(string.ascii_uppercase) for _ in range(2))
    
    block2 = n2_str + "".join(random.choice(string.ascii_uppercase) for _ in range(2))

    block3_int = int(n1_str) + int(n2_str)
    block3 = f"{block3_int:04d}"

    key_label.config(text=f"{block1}-{block2}-{block3}")


def play_music():
    pygame.mixer.init()
    try:
        pygame.mixer.music.load("music.mp3")
        pygame.mixer.music.play(-1)
    except Exception as e:
        print("Не удалось проиграть музыку:", e)

def start_music_thread():
    t = threading.Thread(target=play_music, daemon=True)
    t.start()


def animate():
    global bg_y, pulse, grow, animation_counter

    if animation_counter <= 0:
        return  

    animation_counter -= 1

    bg_y += 0.25
    if bg_y > 0:
        bg_y = -30
    canvas.coords(bg_img_id, 0, bg_y)

    if grow:
        pulse += 1
        if pulse > 23:
            grow = False
    else:
        pulse -= 1
        if pulse < 0:
            grow = True

    cv = max(0, min(255, 80 + pulse * 6))
    hexv = f"{cv:02x}"
    color = f"#{hexv}{hexv}ff"
    canvas.itemconfig(title_text, fill=color)

    root.after(50, animate)


root = tk.Tk()
root.title("Hollow Knight KeyGen (pygame)")

try:
    bg_photo = tk.PhotoImage(file="window.png")
except Exception:
    print("Ошибка: нет window.png")
    exit()

W = bg_photo.width()
H = bg_photo.height()
root.geometry(f"{W}x{H}")

canvas = tk.Canvas(root, width=W, height=H, highlightthickness=0)
canvas.pack()

bg_y = -30
bg_img_id = canvas.create_image(0, bg_y, image=bg_photo, anchor="nw")

cx = W // 2  

pulse = 0
grow = True
title_text = canvas.create_text(
    cx, 40,
    text="Hollow Knight KeyGen",
    font=("Arial", 26, "bold"),
    fill="blue"
)

entry = tk.Entry(root, font=("Arial", 16), justify="center")
canvas.create_window(cx, 120, window=entry, width=260)

btn = tk.Button(root, text="Generate Key", font=("Arial", 14), command=generate_key)
canvas.create_window(cx, 170, window=btn, width=180)

key_label = tk.Label(root, text="", bg="white", font=("Consolas", 18))
canvas.create_window(cx, 240, window=key_label, width=420)

hint = tk.Label(root, text="Введите 6-значное число (например 726911)", bg="white")
canvas.create_window(cx, H - 15, window=hint)

start_music_thread()

animation_counter = 100
animate()

root.mainloop()
