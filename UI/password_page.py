from tkinter import *
from tkinter import messagebox

from password_manager import get_passwords
import UI.main_page_ui

MAIN_LOGO = './Assets/logo.png'
WIN_WIDTH = 720
WIN_HEIGHT = 480
FONT = ("aerial", 8, "bold")


def get_password_info() -> tuple[list[str], list[str], list[str]] | None:
    pw_data = get_passwords()
    if pw_data is None:
        messagebox.showerror(title='No passwords', message='You have no stored passwords')
        return [], [], []

    else:
        sites = [website for website in pw_data]
        usernames = [data['username'] for data in pw_data.values()]
        passwords = [data['password'] for data in pw_data.values()]
        return sites, usernames, passwords


def create_label(text):
    new_label = Label(text=text, bg="light blue", font=FONT, padx=10, pady=10)
    return new_label


def show_page() -> None:
    # Window
    pw_window = Tk()
    pw_window.title("Intro Window")
    pw_window.config(padx=25, pady=25, bg='light blue',
                     width=WIN_WIDTH, height=WIN_HEIGHT)  # Adds padding and sets up win size
    # Labels
    site_title = Label(text='Websites', bg="light blue", fg='red', font=FONT)
    username_title = Label(text='Usernames', bg="light blue", fg='red', font=FONT)
    password_title = Label(text='Passwords', bg="light blue", fg='red', font=FONT)
    sites, usernames, passwords = get_password_info()  # Get the sites, usernames, and passwords lists

    site_labels = [create_label(site) for site in sites]  # Create a list of all the site labels
    username_labels = [create_label(username) for username in usernames]  # Create a list of all the username labels
    password_labels = [create_label(password) for password in passwords]  # Create a list of all the password labels

    # Button Functions:
    def transition_home() -> None:
        """
        Kills the current window and transitions back to the main page
        :return: None
        """
        pw_window.destroy()  # Kills the current window
        UI.main_page_ui.show_main_page()  # Draws the main window

    # Buttons
    back_button = Button(text="Back", width=12, command=transition_home)

    '''
                  0         1          2
            |----------|----------|----------|
           0| Back(b)  |          |          |
            |----------|----------|----------|
           1|  SITE(l) |   UN(L)  |   PW(l)  |
            |----------|----------|----------|
           2|   SITE   | username | password |
            |----------|----------|----------|
           3|   SITE   | username | password |
            |----------|----------|----------|
           4|   SITE   | username | password |
            |----------|----------|----------|
    '''
    back_button.grid(row=0, column=0)
    site_title.grid(row=1, column=0)
    username_title.grid(row=1, column=1)
    password_title.grid(row=1, column=2)

    # Display the site, username, and password labels
    for i in range(0, len(site_labels)):
        site_labels[i].grid(row=i + 2, column=0)
        username_labels[i].grid(row=i + 2, column=1)
        password_labels[i].grid(row=i + 2, column=2)

    pw_window.mainloop()
