from tkinter import *

BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

card = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
card.create_image(400, 263, image=card_front_img)
card.create_text(400, 150, text="French", font=("Arial", 40, "italic"))
card.create_text(400, 263, text="trouve", font=("Arial", 60, "bold"))
card.grid(column=0, row=0, columnspan=2)

correct_img = PhotoImage(file="./images/right.png")
correct_button = Button(image=correct_img, highlightbackground=BACKGROUND_COLOR)
correct_button.grid(column=0, row=1)

incorrect_img = PhotoImage(file="./images/wrong.png")
incorrect_button = Button(image=incorrect_img, highlightbackground=BACKGROUND_COLOR)
incorrect_button.grid(column=1, row=1)

window.mainloop()
