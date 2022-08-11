from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_pwd():
    pwd = []

    password_entry.delete(0, END)

    pwd += [random.choice(LETTERS) for _ in range(5)]
    pwd += [random.choice(NUMBERS) for _ in range(4)]
    pwd += [random.choice(SYMBOLS) for _ in range(4)]

    # for _ in range(5):
    #     pwd.append(random.choice(LETTERS))
    #
    # for _ in range(4):
    #     pwd.append(random.choice(NUMBERS))
    #
    # for _ in range(4):
    #     pwd.append(random.choice(SYMBOLS))

    random.shuffle(pwd)
    pwd_str = ''.join(pwd)

    password_entry.insert(0, pwd_str)
    pyperclip.copy(pwd_str)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_pwd():
    website = website_entry.get()
    email = email_usr_entry.get()
    password = password_entry.get()

    # data_line = f"{website} | {email} | {password}\n"

    # Commenting the lines of code used for writing a text file
    # if len(website) == 0 or len(email) == 0 or len(password) == 0:
    #     messagebox.showinfo(title='OOPS', message='You should not leave fields empty')
    # else:
    #     is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email}"
    #                                                   f"\nPassword: {password}\n Is it OK to save?")
    #     if is_ok:
    #         with open('data.txt', mode='a') as out_w:
    #             out_w.write(data_line)
    #             website_entry.delete(0, END)
    #             password_entry.delete(0, END)

    new_data_dict = {
        website: {
            "email": email,
            "password": password
        }
    }
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title='OOPS', message='You should not leave fields empty')
    else:
        try:
            with open('data.json', mode='r') as out_w:
                exist_data_dict = json.load(out_w)
        except FileNotFoundError:
            with open('data.json', mode='w') as out_w:
                json.dump(new_data_dict, out_w, indent=4)
        else:
            exist_data_dict.update(new_data_dict)
            with open('data.json', mode='w') as out_w:
                json.dump(exist_data_dict, out_w, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

            # Write data into JSON file
            # json.dump(data_dict, out_w, indent=4)

            # Read data from JSON file
            # data_dict2 = json.load(out_w)
            # print(data_dict2)

            # Update data into JSON file
            # (1. Reading the existing data 2. Updating old data with new data from the screen
            # 3. Saving the updated data
            # data_dict2 = json.load(out_w)
            # data_dict2.update(data_dict)
            # json.dump(data_dict2, out_w, indent=4)


def search_button():

    srch_str = website_entry.get()
    new_dict_str = {}
    if len(srch_str) > 0:
        try:
            with open('data.json', mode='r') as out_w:
                srch_data = json.load(out_w)
        except FileNotFoundError:
            messagebox.showinfo(title='Error', message='No data file found')
        else:
            try:
                if srch_data[srch_str]:
                    new_dict_str = {
                        'email': srch_data[srch_str]['email'],
                        'password': srch_data[srch_str]['password']
                    }
            except KeyError:
                messagebox.showinfo(title='Error', message='No data found in the file')
            else:
                msg_line = f"Email id: {new_dict_str['email']}\nPassword: {new_dict_str['password']}"
                messagebox.showinfo(title=srch_str, message=msg_line)


# ---------------------------- UI SETUP ------------------------------- #
# Create a window
window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

# Get the image
lock_img = PhotoImage(file='logo.png')

# Create a canvas object to place the image
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# label 1 - Website
website_label = Label(text='Website:')
website_label.grid(column=0, row=1)

# label 2 - Email/Username
email_usr_label = Label(text='Email/Username:')
email_usr_label.grid(column=0, row=2)

# label 3 - Password
password_label = Label(text='Password:')
password_label.grid(column=0, row=3)

# Entry 1 - Website
website_entry = Entry(width=33)
website_entry.grid(column=1, row=1, sticky='w')
website_entry.focus()

# Entry 2 - Email/Username
email_usr_entry = Entry(width=52)
email_usr_entry.grid(column=1, row=2, columnspan=2, sticky='w')
email_usr_entry.insert(0, '*******@*****.com')

# Entry 3 - Password
password_entry = Entry(width=33)
password_entry.grid(column=1, row=3, sticky='w')

# Button 1 - Generate Password
gen_pwd_button = Button(text='Generate Password', command=gen_pwd)
gen_pwd_button.grid(column=2, row=3, sticky='w')

# Button 2 - Add
add_button = Button(text='Add', width=44, command=save_pwd)
add_button.grid(column=1, row=4, columnspan=2, sticky='w')

# Button 3 - Search
search_button = Button(text='Search', width=15, command=search_button)
search_button.grid(column=2, row=1, sticky='w')

window.mainloop()