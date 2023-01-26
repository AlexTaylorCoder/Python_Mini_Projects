from tkinter import *

DEFAULT_FONT = ("Arial",22)
UNIT_FONT = ("Arial",12)

window = Tk()

window.title("Miles to Kilos")
window.minsize(height=500,width=500)
window.config(padx=75,pady=75)

def get_input():
    inp = user_input.get()
    try:
        float(inp)
    except:
        kilo_label["text"] = "Enter a valid number"
    else:
        kilos = round(float(inp) * 1.609, 2)
        kilo_label["text"] = str(kilos)

label = Label(text="Enter number of miles",font=DEFAULT_FONT)
miles_unit_label = Label(text="Miles",font=UNIT_FONT)
kilos_unit_label = Label(text="Km",font=UNIT_FONT)

user_input = Entry()
button = Button(text="Convert",command=get_input)
kilo_label = Label(text="0",font=DEFAULT_FONT)

label.grid(column=1,row=0,padx=3,pady=3)
miles_unit_label.grid(column=2,row=1)
kilos_unit_label.grid(column=2,row=3)

user_input.grid(column=1,row=1,padx=3,pady=3)
user_input.config(width=10)
kilo_label.grid(column=1,row=2,padx=3,pady=3)
button.grid(column=1,row=3,padx=3,pady=3)



window.mainloop()
