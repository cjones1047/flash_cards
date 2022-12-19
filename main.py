from tkinter import *
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
STARTING_SECONDS = 5
timer = ""


def save_learned_words():
    word_df.to_csv("./data/words_to_learn.csv", index=False)


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
    # handle user clicking either button before timer expires and card flips
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
    """
    delete row of previous word from df if the user answered correct
    """
    global word_df
    # consider what translation of word need be searched based on what side of the card is showing
    try:
        word_row_idx = get_french_word_row().index[0]
    except IndexError:
        english_word = card.itemcget(word, "text")
        word_row = word_df.loc[word_df["English"] == english_word]
        word_row_idx = word_row.index[0]
    word_df = word_df.drop(word_row_idx)
    # replace word_df with data from french_words.csv if all words have been learned
    if len(word_df) == 0:
        word_df = pd.read_csv("./data/french_words.csv")
    save_learned_words()
    pick_word()


# Try to extract csv file of learned words if existent, otherwise extract csv file with all words
try:
    word_df = pd.read_csv("./data/words_to_learn.csv")
    print("df from words_to_learn")
except FileNotFoundError:
    word_df = pd.read_csv("./data/french_words.csv")
    print("df from french_words")

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
