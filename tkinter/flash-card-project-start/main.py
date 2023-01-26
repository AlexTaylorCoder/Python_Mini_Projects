from tkinter import *
from random import randint
import pandas as pd
BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Ariel",40,"italic")
DETAILS_FONT = ("Ariel",60,"bold")
SCORE_FONT = ("Ariel",20,"bold")
flippable = False
timer = None
count = 0

#Create window
window = Tk()
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)
window.title("Flashy")

#Get data
df = pd.read_csv("./data/french_words.csv")

#Need state managment
def flip_timer():
    global timer, flippable
    #Need cleanup for flip timer
    flippable = False
    window.after_cancel(timer)
    print(timer)
    timer = window.after(3000,flip_card)

def random_word():
    line = randint(0,101)
    info = df.loc[line]
    card_front.grid(row=0,column=0,columnspan=2)
    card_front.itemconfig(details,text=info["French"])
    card_back.itemconfig(details_back,text=info["English"])
    card_back.itemconfig(details_back,text=info["English"])
def display_random_word():
    global flippable
    if flippable:
        random_word()
        flip_timer()

def flip_card():
    global flippable
    flippable = True
    card_front.grid_forget()
    window.after_cancel(timer)

def correct():
    global count
    display_random_word()
    count += 1
    score["text"] = count
    word = card_front.itemcget(details,'text')
    print(word)
    loc = df[df["French"] == word]
    print(loc)
    # pd.DataFrame.to_csv("words_to_learn.csv",index=False)

def incorrect():
    display_random_word()

yes_image = PhotoImage(file="./images/right.png")
no_image = PhotoImage(file="./images/wrong.png")
card_front_image = PhotoImage(file="./images/card_front.png")
card_back_image = PhotoImage(file="./images/card_back.png")

card_back = Canvas(width=800,height=526,bg=BACKGROUND_COLOR,highlightthickness=0)
card_front = Canvas(width=800,height=526,bg=BACKGROUND_COLOR,highlightthickness=0)

score = Label(font=SCORE_FONT,text=count,bg=BACKGROUND_COLOR)

card_front.create_image(400,263,image=card_front_image)
card_back.create_image(400,263,image=card_back_image)

#Card info Front
title = card_front.create_text(400,150,text="French",font=TITLE_FONT)
details = card_front.create_text(400,263,text="Details",font=DETAILS_FONT)

#Card info Back
title_back = card_back.create_text(400,150,text="English",font=TITLE_FONT,fill="white")
details_back = card_back.create_text(400,263,text="Details",font=DETAILS_FONT,fill="white")
#Response Button
yes_button = Button(image=yes_image, highlightthickness=0,command=correct)
no_button = Button(image=no_image, highlightthickness=0,command=incorrect)

no_button.grid(row=1,column=0)
yes_button.grid(row=1,column=1)
card_front.grid(row=0,column=0,columnspan=2)
card_back.grid(row=0,column=0,columnspan=2)
score.grid(row=0,column=2)

random_word()
timer = window.after(3000,flip_card)
flip_timer()

window.mainloop()


