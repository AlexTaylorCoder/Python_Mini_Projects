
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
MAX_REPS = 5
reps = 0
timer = None



# ---------------------------- TIMER RESET ------------------------------- # 

def end_timer():
    window.after_cancel(timer)
    global reps
    reps = 0
    canvas.itemconfig(timer_text, text="00:00")
    current_label["text"] = "Timer"
    checkmark["text"] = ""

# ---------------------------- TIMER MECHANISM ------------------------------- # 

def start_timer():
    global reps
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    reps += 1
    #Start with 25 min then 5 min when hits

    if reps % 8 == 0:
        count_down(long_break_sec)
        current_label["text"] = "Long Break"
        current_label["foreground"] = RED
    elif reps % 2 == 0:
        count_down(short_break_sec)
        current_label["text"] = "Short Break"
        current_label["foreground"] = YELLOW
    else:
        count_down(work_sec)
        current_label["text"] = "Work Period"
        current_label["foreground"] = GREEN

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 

def count_down(count):
    global timer
    if count > 0:
        min, sec = divmod(count,60)

        if min == 0:
            min = "00"
        if sec < 10:
            sec = "0" + str(sec)
        canvas.itemconfig(timer_text, text= str(min) + ":" + str(sec))
        timer = window.after(1000,count_down, count-1)
    else:
        start_timer()
        checkmark["text"] = "✓" * (reps // 2)
        print(checkmark["text"])


# ---------------------------- UI SETUP ------------------------------- #

from tkinter import * 

#Window creation
window = Tk()
window.title("Pomodoro")
window.config(padx=100,pady=50,background=YELLOW)

#Image creation
canvas = Canvas(width=200,height=224,background=YELLOW,highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100,112,image=tomato_img)
timer_text = canvas.create_text(100,130,text="00:00",fill="white",font=(FONT_NAME,35,"bold"))

#Work/Break Label
current_label = Label(text="Timer",font=(FONT_NAME,32,"bold"),background=YELLOW,foreground=PINK)

# Button creation
start_button = Button(text="Start")
end_button = Button(text="End")

#Button events
start_button.config(command=start_timer)
end_button.config(command=end_timer)

#Checkmark 
checkmark = Label(text="",bg=YELLOW,fg=GREEN,font=(FONT_NAME,22,"bold"))
checkmark.grid(row=3,column=1)


#Display elements to screen in 3x4 grid
# current_label.grid(column=1,row=0)
current_label.grid(column=1,row=0,padx = 5)
start_button.grid(column=0,row=2,padx=3)
end_button.grid(column=2,row=2,padx=3)
canvas.grid(column=1,row=1,padx=3)

#Event loop
window.mainloop()