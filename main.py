from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
"""
AIM:-
1).Now the aim is to store the data in JSON File instead of normal text file such that it will speed up the transferring
of data and provide a better structure for our data such that it can be used efficiently.
2).We will be adding the search button such that when user enter the website name and hit the search button then the
dialog box appears on the screen showing all the credentials of that website

"""
"""
Pyperclip is a cross-platform Python module for copy and paste clipboard functions.
So what we want our program to do that when we generate the password then we want to automatically copied to the
clipboard and then we can paste it anywhere.
"""

# ---------------------------- SEARCH CREDENTIALS ------------------------------- #


def search_credentials():
    website = website_entry.get()
    #For the very first time the file is not created then if we will try to read from it then it will throw error, so we
    #have to be careful about this. Initially we don't have any data, so it must throw error message letting user know
    #that the file has not created, and it doesn't have any data.
    try:
        with open("data.json", "r") as data_file:
            json_data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        if website in json_data:
            email = json_data[website]["email"]
            password = json_data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email} \nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)
    final_pwd = ""
    for x in range(1, nr_letters + 1):
        num = random.randint(0, len(letters) - 1)
        final_pwd += letters[num]
    for y in range(1, nr_symbols + 1):
        sy = random.randint(0, len(symbols) - 1)
        final_pwd += symbols[sy]
    for z in range(1, nr_numbers + 1):
        zz = random.randint(0, len(numbers) - 1)
        final_pwd += numbers[zz]
    list_pwd = list(final_pwd)
    random.shuffle(list_pwd)
    random_pwd = ''.join(list_pwd)
    password_entry.insert(0, string=random_pwd)
    pyperclip.copy(random_pwd)

# ---------------------------- SAVE PASSWORD ------------------------------- #
#We want our file to be open in append mode as we will be writing everytime we don't want our previous file content to
#be deleted. If the file(data.txt) is not created manually then it will automatically create our file when we use append
#("a") or write("w") mode


def save():
    email = email_entry.get()
    website = website_entry.get()
    password = password_entry.get()
    #Since we want to store data in json file, so we have to structure data in json type which is as follows:
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    """
    If the user left any of the entry then we should pop-up a message and if all the fields are properly filled then we
    will again ask the user whether the details they entered are correct or not and if they opt for Ok then it would
    return True in is_ok variable and if opt for Cancel then the variable is_ok will store False.
    So if the user will opt for Ok then we will be adding all the content to the file otherwise the user can change or 
    modify the fields.
    """
    if len(email) == 0 or len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        """
        There is one problem with the code which is that when we will be starting our code from scratch then initially
        we have nothing in the file and also the file hasn't been created so it will throw FileNotFoundError.
        In order to avoid this we will use exception handling method try-except block
        """
        try:
            with open("data.json", "r") as data_file:
                #json.dump() requires so many arguments but important ones are firstly the data which we want to store,
                #secondly, we will put the data file that we want to put our data into in our case it is 'file'
                #Third argument is indent=4 this is used to provide the number of spaces to indent all the JSON Data, so
                #that it becomes much easier to read.
                #json.dump(new_data, file, indent=4)
                #Reading old data
                old_data = json.load(data_file)
                #Updating old data with new data
                old_data.update(new_data)
                print(old_data)
        except:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file)
                """
                We have to do this old_data = new_data because for the very first time as soon it encounters error in 
                line 80 then the rest of the line will not be executed of try block which means that data variable is
                also not declared which can again cause to error in line 103 so in order to avoid this we assign as
                initially first data will be new data as well as old data.
                """
                old_data = new_data
        with open("data.json", "w") as data_file:
            """
            Saving the updated data back into the file and wipe/clear all the previous data as we know that when we use 
            the "w" mode it clears all the data, and then it starts writing the new data, so we are just updating the 
            old data and then adding the new data back to the file.
            """
            json.dump(old_data, data_file, indent=4)
        #Here delete() is used to delete the entry
        #delete between two indices, 0-based
        website_entry.delete(0, 'end')
        password_entry.delete(0, 'end')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)
website_label = Label(text="Website: ")
website_label.grid(row=1, column=0)
website_entry = Entry(width=33)
website_entry.grid(row=1, column=1, columnspan=1, sticky="ew")
#focus() will enable the cursor on website_entry box when we open the window
website_entry.focus()
search_button = Button(text="Search", width=14, command=search_credentials)
search_button.grid(row=1, column=2, sticky="ew")
email_label = Label(text="Email/Username: ")
email_label.grid(row=2, column=0)
email_entry = Entry(width=52)
email_entry.grid(row=2, column=1, columnspan=2)
"""
We know that we use a single email in every website to signup, so it will be a very good idea that if we launch our
email_entry box with by-default email.
Now we will be giving the by-default email and if user wants they can change.This is somehow behaves like a dummy email
Here 0 specify the index position starting it means the text going to be inserted in the first position whereas END
is a constant which defines the end point. Since in our case it doesn't matter we can place anywhere as we are starting
with empty box.In other words the index value just put the cursor where we want to write the string.
"""
email_entry.insert(0, string="mohammadtauseef284@gmail.com")
password_label = Label(text="Password: ")
password_label.grid(row=3, column=0)
password_entry = Entry(width=33)
password_entry.grid(row=3, column=1)
password_generate_button = Button(text="Generate Password", command=generate_password)
password_generate_button.grid(row=3, column=2)
"""
The aim of the project is that when th user hit the 'Add' button it will should save the 
"""
add_button = Button(text="Add", width=44, command=save)
add_button.grid(row=4, column=1, columnspan=2)
window.mainloop()
