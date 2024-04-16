import UI.password_page
from tkinter import *
import password_manager
from tkinter import messagebox, simpledialog

MAIN_LOGO = './Assets/logo.png'
WIN_WIDTH = 720
WIN_HEIGHT = 480
FONT = ("aerial", 8, "bold")


def show_main_page():
    # Window
    main_window = Tk()
    main_window.title("Intro Window")
    main_window.config(padx=25, pady=25, bg='light blue',
                       width=WIN_WIDTH, height=WIN_HEIGHT)  # Adds padding and sets up win size
    # Canvas
    canvas_image = PhotoImage(file=MAIN_LOGO)  # Creates a PhotoImage object
    canvas = Canvas(width=WIN_WIDTH / 2, height=WIN_HEIGHT / 2,
                    bg='light blue', highlightthickness=0)  # Creates the canvas for the logo
    canvas.create_image(180, 120, image=canvas_image)

    # Labels
    site_label = Label(master=main_window, text='Website', bg="light blue", font=FONT)
    username_label = Label(master=main_window, text='Username/Email', bg="light blue", fg='black', font=FONT)
    password_label = Label(master=main_window, text='Password', bg="light blue", font=FONT)

    # Entries
    site_entry = Entry(width=50, bg="light green", font=FONT)
    site_entry.focus()  # Makes it so that the entry is automatically selected
    username_entry = Entry(width=50, bg="light green", font=FONT)
    password_entry = Entry(width=50, bg="light green", font=FONT)

    def add_password() -> None:
        # Get the text from the entries
        website = site_entry.get().lower()
        username = username_entry.get().lower()
        password = password_entry.get().lower()

        if website == '' or username == '' or password == '':
            # ASSERT: One of the fields are empty
            messagebox.showerror(title='Incomplete Form', message='Please make sure to fill out all fields')
        else:
            # Clear the fields
            site_entry.delete(first=0, last="end")
            username_entry.delete(first=0, last="end")
            password_entry.delete(first=0, last="end")

            # Create a pwd_data dictionary so that we can write to the file using json
            pwd_data = {
                website: {
                    "username": username,
                    "password": password,
                }
            }
            password_manager.add_password(pwd_data)  # Write the password to the file

    def create_autofill_prompt() -> str:
        # Prompt user to create a password
        result = simpledialog.askstring(title="Autofill Prompt",
                                        prompt="Create a default username to autofill")

        # Check if the user entered a valid username and return it if so. If not then re-prompt the user
        if result is not None:
            return result
        else:
            while result is None or result == '':
                # ASSERT: User didn't enter a username
                result = simpledialog.askstring(title="Username cannot be blank",
                                                prompt="Create a default username to autofill")

    def autofill() -> None:
        auto_username = password_manager.autofill()  # Get the default autofill username if it is available
        if auto_username is not None:
            username_entry.insert(index=0, string=auto_username)  # Insert the default autofill username
        else:
            new_autofill = create_autofill_prompt()  # Prompts the user to create a default autofill username
            settings_params = {
                'settings': {
                    "autofill": new_autofill,
                }
            }
            password_manager.add_autofill(settings_params)  # Add the new default username to the settings file
            username_entry.insert(index=0, string=new_autofill)  # Insert the default autofill username

    def search_for_site() -> None:
        website = site_entry.get().lower()  # Get the website being searched for
        site_info = password_manager.search(website)  # Get stored website info if available
        if site_info is not None:
            # Display the site info to the user
            messagebox.showinfo(title='site info', message=f'Username = {site_info[0]}\nPassword = {site_info[1]}')
        else:
            # ASSERT: No info was found for the given website
            messagebox.showerror(title='site not found', message=f'No info for {website} was found')

    def generate_password() -> None:
        password = password_manager.gen_password()  # Generate a random password
        password_entry.delete(first=0, last='end')  # Clear the password entry
        password_entry.insert(0, password)  # Populate the password entry with the random password
        main_window.clipboard_clear()  # Clears the clipboard
        main_window.clipboard_append(string=password)  # Copy the random password to the clipboard

    def transition_to_pw_page():
        main_window.destroy()
        UI.password_page.show_page()

    # Menu
    menubar = Menu(main_window)  # Creates a menu bar
    main_window.config(menu=menubar)  # Sets the window's menu to the menu bar
    options_menu = Menu(menubar)

    # Menu Buttons
    options_menu.add_command(label='Saved Passwords',
                             command=transition_to_pw_page)  # Creates a Saved Passwords button
    options_menu.add_command(label='Settings',
                             command=main_window.destroy)  # Creates a Settings button
    options_menu.add_command(label='Exit',
                             command=main_window.destroy)  # Creates an Exit button

    menubar.add_cascade(label="Options", menu=options_menu)  # add the Options menu to the menubar

    # Buttons
    search_button = Button(text="Search", width=15, command=search_for_site)
    autofill_button = Button(text="Autofill", width=15, command=autofill)
    gen_button = Button(text="Generate", width=15, command=generate_password)
    add_button = Button(text="Add", width=42, command=add_password)

    """
              0         1          2
        |----------|----------|----------|
       0|          |   LOGO   |          |
        |----------|----------|----------|
       1|  SITE(L) |  SITE(E) | SEARCH(B)|
        |----------|----------|----------|
       2|   UN(L)  |   UN(E)  |  AUTO(B) |
        |----------|----------|----------|
       3|   PW(L)  |   PW(E)  |   GEN(B) |
        |----------|----------|----------|
       4|          |   ADD(B) |   ADD(B) |
        |----------|----------|----------|
    """

    canvas.grid(row=0, column=1, columnspan=1)
    site_label.grid(row=1, column=0)
    site_entry.grid(row=1, column=1)
    search_button.grid(row=1, column=2)
    username_label.grid(row=2, column=0)
    username_entry.grid(row=2, column=1)
    autofill_button.grid(row=2, column=2)
    password_label.grid(row=3, column=0)
    password_entry.grid(row=3, column=1)
    gen_button.grid(row=3, column=2)
    add_button.grid(row=4, column=1)

    main_window.mainloop()
