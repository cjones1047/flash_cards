from tkinter import *
from random import choice
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
STARTING_SECONDS = 5
timer = ""


def flip_card():
    window.after_cancel(timer)
    # get English translation of shown French word
    french_word = card.itemcget(word, "text")
    word_row = word_df.loc[word_df["French"] == french_word]
    english_word = word_row["English"].item()
    # flip card over
    card.itemconfig(language, text="English")
    card.itemconfig(word, text=english_word)
    card.itemconfig(card_side, image=card_back_img)


def countdown(seconds_left):
    if seconds_left > 0:
        global timer
        timer = window.after(1000, countdown, seconds_left - 1)
    else:
        flip_card()


def pick_word():
    word_picked = choice(word_dict)["French"]
    card.itemconfig(language, text="French")
    card.itemconfig(word, text=word_picked)
    card.itemconfig(card_side, image=card_front_img)
    global STARTING_SECONDS
    countdown(STARTING_SECONDS)


word_df = pd.read_csv("./data/french_words.csv")
word_dict = word_df.to_dict(orient="records")

window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

card = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
card_side = card.create_image(400, 263, image="")
language = card.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word = card.create_text(400, 263, text="", font=("Arial", 60, "bold"))
card.grid(column=0, row=0, columnspan=2)

correct_img = PhotoImage(file="./images/right.png")
correct_button = Button(image=correct_img, highlightbackground=BACKGROUND_COLOR, command=pick_word)
correct_button.grid(column=0, row=1)

incorrect_img = PhotoImage(file="./images/wrong.png")
incorrect_button = Button(image=incorrect_img, highlightbackground=BACKGROUND_COLOR, command=pick_word)
incorrect_button.grid(column=1, row=1)

pick_word()

window.mainloop()
