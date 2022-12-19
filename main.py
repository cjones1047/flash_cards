from tkinter import *
from random import choice
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
STARTING_SECONDS = 5
timer = ""


def get_french_word_row():
    french_word = card.itemcget(word, "text")
    word_row = word_df.loc[word_df["French"] == french_word]
    return word_row


def flip_card():
    # get English translation of shown French word
    word_row = get_french_word_row()
    english_word = word_row["English"].item()
    # flip card over
    card.itemconfig(language, text="English", fill="white")
    card.itemconfig(word, text=english_word, fill="white")
    card.itemconfig(card_side, image=card_back_img)


def pick_word():
    global timer
    # handle user clicking either button before timer expires
    try:
        window.after_cancel(timer)
    except ValueError:
        pass
    # pick new word for card
    word_picked = word_df.sample()["French"].item()
    card.itemconfig(language, text="French", fill="black")
    card.itemconfig(word, text=word_picked, fill="black")
    card.itemconfig(card_side, image=card_front_img)
    global STARTING_SECONDS
    timer = window.after(STARTING_SECONDS * 1000, flip_card)


def remove_word():
    # delete row of previous word from df if the user answered correct
    # consider what translation of word need be searched based on what side of the card is showing
    global word_df
    try:
        word_row_idx = get_french_word_row().index[0]
    except IndexError:
        english_word = card.itemcget(word, "text")
        word_row = word_df.loc[word_df["English"] == english_word]
        word_row_idx = word_row.index[0]
    print(word_row_idx)
    word_df = word_df.drop(word_row_idx)
    print(word_df)
    pick_word()


word_df = pd.read_csv("./data/french_words.csv")

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
correct_button = Button(image=correct_img, highlightbackground=BACKGROUND_COLOR, command=remove_word)
correct_button.grid(column=0, row=1)

incorrect_img = PhotoImage(file="./images/wrong.png")
incorrect_button = Button(image=incorrect_img, highlightbackground=BACKGROUND_COLOR, command=pick_word)
incorrect_button.grid(column=1, row=1)

pick_word()

window.mainloop()
