from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- DELETE ENTRY------------------------------- #
def delete_entry():
    website = website_entry.get()

    if len(website) != 0:
        try:
            with open("password_data.json", mode="r") as data_file:
                # Reading the old data
                data = json.load(data_file)  # converts data into python dict
                if website not in data:  # if no data saved for website
                    messagebox.showinfo(message=f"You do not have data saved for {website}")
        except FileNotFoundError:
            messagebox.showinfo(message="Error: No Data File Found.")

        else:
            should_delete = messagebox.askokcancel(message=f"Do you wish to delete saved {website} data?\n"
                                                           f"Username/Email: {data[website]['email']}\n"
                                                           f"Password: {data[website]['password']}")
            if should_delete:
                del data[website]

            with open("password_data.json", mode="w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)

    else:
        messagebox.showinfo(message="Error: No website entered.")


# ---------------------------- VIEW ALL PASSWORDS------------------------------- #
def view_all_passwords():
    try:
        with open("password_data.json", mode="r") as data_file:
            # Reading the old data
            data = json.load(data_file)  # converts data into python dict
    except FileNotFoundError:
        messagebox.showinfo(message="Error: No Data File Found.")
    else:
        all_passwords = Tk()
        all_passwords.title("Website | Username/Email | Password")
        text = Text(all_passwords)  # figure out how this works
        text.pack()
        sorted_dict = {key: value for key, value in sorted(data.items())}  # Alphabetizes when displaying
        for info in sorted_dict:
            text.insert(END, f"{info} | {data[info]['email']} | {data[info]['password']}\n")

        all_passwords.mainloop()


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    email = email_username_entry.get()
    try:
        with open("password_data.json", mode="r") as data_file:
            data = json.load(data_file)  # converts data into python dict

    except FileNotFoundError:
        messagebox.showinfo(message="Error: No Data File Found.")
    else:
        if len(website) == 0:
            messagebox.showinfo(message="Please enter website to search.")

        elif website in data and email in data[website]["email"]:  # checks if email website combo are in data
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(message=f"{website}\nEmail/Username: {email} \nPassword: {password}")
            pyperclip.copy(password)
        else:
            messagebox.showinfo(message=f"No information saved for {website}")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password = password_entry.get()
    if len(password) == 0:
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u',
                   'v',
                   'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                   'Q',
                   'R',
                   'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        password_list = []
        [password_list.append(choice(letters)) for _ in range(randint(8, 10))]
        [password_list.append(choice(symbols)) for _ in range(randint(2, 4))]
        [password_list.append(choice(numbers)) for _ in range(randint(2, 4))]

        shuffle(password_list)

        password = "".join(password_list)
        password_entry.insert(0, password)
        pyperclip.copy(password)
    else:
        password_entry.delete(0, END)
        generate_password()


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    # Checks for any empty Entries
    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showwarning(message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(message=f"These are the details entered: \nWebsite:{website} \nEmail: {email} \n"
                                               f"Password: {password} \nIs this OK to save?")

        if is_ok:
            try:
                with open("password_data.json", mode="r") as data_file:
                    # Reading the old data
                    data = json.load(data_file)  # converts data into python dict
            except FileNotFoundError:
                with open("password_data.json", mode="w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:

                if website in data:
                    update = messagebox.askyesno(message=f"You already have a password for"
                                                         f" {website} account with {data[website]['email']} "
                                                         f"Would you like to override this?")
                    if update:
                        data.update(new_data)
                        with open("password_data.json", mode="w") as data_file:
                            # Saving updated data
                            json.dump(data, data_file, indent=4)
                else:
                    # Updating old data with new data if try went through
                    data.update(new_data)
                    with open("password_data.json", mode="w") as data_file:
                        # Saving updated data
                        json.dump(data, data_file, indent=4)

            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")  # reads a photo from a file
canvas.create_image(150, 100, image=logo_img)
canvas.grid(column=1, row=0)
# Website label
website_label = Label(text="Website")
website_label.grid(column=0, row=1)
# Email/username label
email_username_label = Label(text="Email/Username")
email_username_label.grid(column=0, row=2)
# Password Label
password_label = Label(text="Password")
password_label.grid(column=0, row=3)
# Website Entry
website_entry = Entry(width=23)
website_entry.grid(column=1, row=1)
website_entry.focus()
# Email/Username Entry
email_username_entry = Entry(width=40)
email_username_entry.grid(column=1, row=2, columnspan=2)
email_username_entry.insert(0, string="myemail@gmail.com")
# Password Entry
password_entry = Entry(width=23)
password_entry.grid(column=1, row=3)
# Generate button
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)
# Add Button
add_button = Button(text="Add", width=38, command=save)
add_button.grid(column=1, row=4, columnspan=2)
# Search Button
search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(column=2, row=1)
# View Passwords Button
view_passwords = Button(text="View Passwords", width=21, command=view_all_passwords)
view_passwords.grid(column=1, row=6)
# Delete button
delete_button = Button(text="Delete Entry", width=13, command=delete_entry)
delete_button.grid(column=2, row=6)

window.mainloop()

