import json
import pandas as pd
from tkinter import *
from tkinter import messagebox
import pyperclip
from password_generator import generate_password
from hide import EMAIL

# ---------------------------- SEARCH WEBSITE ------------------------------- #

# The function does the same searches website
# One is for csv pandas and the other is for json
# Remember if we can solve it with if/else use it rather than try/catch!

def find_user() -> None:
  # using pandas csv
  website = website_input.get()
  try:
    data = pd.read_csv("./data.csv")
  except FileNotFoundError:
    messagebox.showerror(title="Error", message="No Data File Found.")
  else:
    found_website = data[data.Website == website]
    if len(found_website) > 0:
      index = int(data[data.Website == website].index[0])
      email = found_website["Emails/Usernames"][index]
      password = found_website["Password"][index]
      messagebox.showinfo(title=website, message=f"Email/Username: {email}\nPassword: {password}")
    else:
      messagebox.showwarning(title="Warning", message=f"No details for {website} exists.")


def find_password() -> None:
  # using the json file
  website = website_input.get()
  try:
    with open("data.json") as data_file:
      data = json.load(data_file)
  except FileNotFoundError:
    messagebox.showerror(title="Error", message="No Data File Found.")
  else:
    if website in data:
      email = data[website]["Email"]
      password = data[website]["Password"]
      messagebox.showinfo(title=website, message=f"Email/Username: {email}\nPassword: {password}")
    else:
      messagebox.showwarning(title="Warning", message=f"No details for {website} exists.")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
  PASSWORD = generate_password()
  password_input.delete(0, END)
  password_input.insert(0, PASSWORD)
  pyperclip.copy(password_input.get())
# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
  website = website_input.get()
  email = email_input.get()
  password = password_input.get()
  save_details = {
    "Website": website,
    "Emails/Usernames": email,
    "Password": password
  }

  new_data = {
    website: {
      "Email": email,
      "Password": password
    }
  }

  if len(website) == 0 or len(email) == 0 or len(password) == 0:
    messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
  else:
    is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} \nPassword: {password} \nIs it okay to save?")

    if is_ok:
    # Pandas
      try:
        read = pd.read_csv("./data.csv")
      except FileNotFoundError:
        length = 0
        df = pd.DataFrame(save_details, index=[length])
      else:
        length = len(read)
        df = pd.DataFrame(save_details, index=[length])
      finally:
        df.to_csv("data.csv", mode="a", header=False if length > 0 else True)
  
    # JSON
      try:
        data_file = open("data.json", mode="r")
        #Read old data
        data = json.load(data_file)
        #Update old data with new data
        data.update(new_data)
      except FileNotFoundError:
        #if error then create the new json file and write to it
        with open("data.json", mode="w") as data_file:
          json.dump(new_data, data_file, indent=4)
      else:
        #If no issues then save the updated data
        data_file = open("data.json", mode="w")
        json.dump(data, data_file, indent=4)
      finally:
        #close the file in the end no matter what update the GUI
        data_file.close()
        website_input.delete(0, END)
        password_input.delete(0, END)
  

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="white")

canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
image = PhotoImage(file="./logo.png")
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)



# Labels
website = Label(text="Website:", bg="white", padx=0)
website.grid(column=0, row=1)

email = Label(text="Email/Username:", bg="white", padx=0)
email.grid(column=0, row=2)

password = Label(text="Password:", bg="white", padx=0)
password.grid(column=0, row=3)


# Entries
website_input = Entry(width=25)
website_input.focus()
website_input.grid(column=1, row=1)

email_input = Entry(width=42)
email_input.insert(0, EMAIL)
email_input.grid(column=1, row=2, columnspan=2)

password_input = Entry(width=25)
password_input.grid(column=1, row=3, padx=0)


# Buttons
search_button = Button(text="Search", width=14, command=find_user)
search_button.grid(column=2, row=1)

generate_button = Button(text="Generate Password", width=14, command=password_generator)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", width=40, command=save)
add_button.grid(column=1, row=4, columnspan=2)


window.mainloop()