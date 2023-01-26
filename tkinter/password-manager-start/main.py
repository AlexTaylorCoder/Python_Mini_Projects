import json
from random import choice, randint
import string
from tkinter import messagebox
from tkinter import *

# ---------------------------- THINGS TO DO ------------------------------- #
# Fix copy to clipboard
# Encryption
# Better UI

import pyperclip
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password qualifications
    #Need to pick random chars between a-z 
def random_password():
    password = ""
    digits_required = False
    pun_required = False
    for n in range(randint(12,15)):
        match randint(0,2):
            case 0:
                password += choice(string.ascii_letters)
            case 1:
                password += choice(string.digits)
                digits_required = True
            case 2: 
                password += choice(string.punctuation)
                pun_required = True
    # if not digits_required:
    #     password += choice(string.digits)
    # if not pun_required:
    #     password += choice(string.punctuation)

    #This part is buggy for ubuntu
    pyperclip.copy(password)
    password_input.delete(0,END)
    password_input.insert(0,password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_inputs():
    
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()


    #Can use regex for further validation testing 
    if (not password or not website or not email):
        messagebox.showinfo(title="Blank",message="Please fill blank field(s)")
    elif len(password) < 8:
        messagebox.showinfo(title="Invalid Length",message="Password must be at least 8 characters!")
    else:
        data = { website: {"email":email,"password":password} } 
        isOkay = messagebox.askokcancel(title="Save Password",message=f"Website:{website}\n Email:{email}\n Password:{password}")

        if isOkay:
            #Open file as read
            try:
                with open("passwords.json","r") as f:
                    #Read old data
                    old_data = json.load(f)
                    #Update old data
                    old_data.update(data)
                #Open file to write
            except FileNotFoundError:
                write_to_file(data)
            else:
                write_to_file(old_data)
            finally:
                website_input.delete(0,END)
                password_input.delete(0,END)

def write_to_file(data):
    with open("passwords.json","w") as f:
        json.dump(data,f,indent=4)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_pass():
    search = website_input.get()
    with open("passwords.json","r") as f:
        data = json.load(f)
        try:
            info = data[search]
        except KeyError:
            messagebox.showinfo(title="Not Found",message='Website not found!')
        else:
            messagebox.showinfo(title="Details",message=f'Email: {info["email"]}\n Password: {info["password"]}')
    

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Generator")
window.config(padx=20,pady=20)
window.minsize(500,400)

#Image
canvas = Canvas(width=230,height=255)
photo = PhotoImage(file="logo.png")
canvas.create_image(170,150,image=photo)

#Labels
website_label = Label(text="Website:")
email_label = Label(text="Email:")
password_label = Label(text="Password:")

#Inputs

generate = Button(text="Generate Password",command=random_password)

website_input = Entry(width=20)
website_input.focus()

email_input = Entry(width=35)
email_input.insert(0,"alextaylor515@gmail.com")
password_input = Entry(width=21)

#Save password

save = Button(text="Add",width=20,command=save_inputs)
find = Button(text="Search",width=20,command=find_pass)

#Element layout
canvas.grid(row=0,column=1)

website_label.grid(row=1,column=0)
email_label.grid(row=2,column=0)
password_label.grid(row=3,column=0)

website_input.grid(row=1,column=1,columnspan=1)
email_input.grid(row=2,column=1,columnspan=2)
password_input.grid(row=3,column=1)
generate.grid(row=3,column=2)
save.grid(row=4,column=1,columnspan=3)
find.grid(row=1,column=2)

#Mainloop
window.mainloop()