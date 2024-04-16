import os
import json
from tkinter import *
from tkinter import simpledialog
from UI.main_page_ui import show_main_page
import password_manager

HOME_LOGO = './Assets/Home Logo.png'


def show_intro():

    intro_window = Tk()
    intro_window.title("Intro Window")
    intro_window.config(bg='light blue')
    intro_window.geometry("720x480")  # Set the initial window size
    intro_window.resizable(False, False)  # Prevent the window from being resized

    # Create photo image and display it on a canvas
    canvas_image = PhotoImage(file=HOME_LOGO)
    canvas = Canvas(bg='light blue', highlightthickness=0, width=720, height=480)  # Creates the canvas for the logo
    canvas.create_image(360, 240, image=canvas_image)
    canvas.grid(column=0, row=0)

    prompt_for_password(intro_window)  # Shows dialog box to prompt user for their password if available
    intro_window.mainloop()


def create_password_prompt() -> str:
    # Prompt user to create a password
    result = simpledialog.askstring(title="Password prompt",
                                    prompt="Create a password to login to the application")
    # Check if the user entered a valid password and return it if so. If not then re-prompt the user
    if result is not None:
        return result
    else:
        while result is None or result == '':
            # ASSERT: User didn't enter a password
            result = simpledialog.askstring(title="Password cannot be blank",
                                            prompt="Create a password to login to the application")


def prompt_for_password(window: Tk):
    if os.path.exists('./data/settings.json'):
        correct_password = password_manager.check_for_app_password()

    else:
        # ASSERT: This is the first time the user has used the app and the user has not setup their password yet
        os.makedirs('./data')
        with open(file='./data/settings.json', mode='w') as data_file:
            password = create_password_prompt()  # Prompt the user to enter a password for the app
            settings_params = {
                'app_password': {
                    "password": password,
                }
            }
            print("HERE")
            json.dump(settings_params, fp=data_file, indent=4)  # Write the password to the app password file
            return None  # Returns None to show that there was no password made previously

    if correct_password is not None:
        # ASSERT: There is already a password setup and we need to prompt for it
        result = simpledialog.askstring(title="Password prompt",
                                        prompt="Enter your application password")
        if result != correct_password:
            # ASSERT: User entered an incorrect password
            while result != correct_password:
                result = simpledialog.askstring(title="Password prompt",
                                                prompt="Password is incorrect. Try again")

    window.destroy()  # Destroy the intro window
    show_main_page()  # Transitions to the main application screen
