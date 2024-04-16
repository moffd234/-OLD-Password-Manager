import random
import string
import json


def check_for_app_password() -> str | None:
    with open(file='data/settings.json', mode='r') as data_file:
        data = json.load(data_file)  # Read the settings from the settings file
        return data['app_password']['password']  # Return the app password


def autofill() -> str | None:
    try:
        with open(file='data/settings.json', mode='r') as data_file:
            data = json.load(data_file)  # Read the settings from the settings file
            return data['settings']['autofill']
    except KeyError:
        # ASSERT: Autofill hasn't been setup yet
        return None


def add_autofill(settings_params) -> None:
    with open(file='data/settings.json', mode='r') as data_file:
        # ASSERT: data.json is already created
        data = json.load(data_file)  # Loads the current data in the JSON file

    data.update(settings_params)  # Update the JSON data to include the autofill setting

    with open(file='data/settings.json', mode='w') as data_file:
        json.dump(data, data_file, indent=4)  # Writes the default username to the settings file


def add_password(pwd_data: dict) -> None:
    try:
        with open(file='data/data.json', mode='r') as data_file:
            # ASSERT: data.json is already created
            data = json.load(data_file)  # Loads the current data in the JSON file

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        # ASSERT: File was not readable either because it didn't exist or was empty
        with open(file='data/data.json', mode='w') as data_file:
            json.dump(pwd_data, data_file, indent=4)  # Dumps pwd_data to the data file

    else:
        # ASSERT: No error was thrown
        data.update(pwd_data)
        with open(file='data/data.json', mode='w') as data_file:
            json.dump(data, data_file, indent=4)  # Writes the password to the password file


def gen_password() -> str:
    # Generate a random password using 5 lowercase letters, 5 uppercase letters, 5 digits, and 5 special characters
    password = (
            ''.join(random.choice(string.ascii_lowercase) for _ in range(5)) +
            ''.join(random.choice(string.ascii_uppercase) for _ in range(5)) +
            ''.join(random.choice(string.digits) for _ in range(5)) +
            ''.join(random.choice(string.punctuation) for _ in range(5))
    )

    password_list = list(password)  # Convert the password to a list
    random.shuffle(password_list)  # Shuffle the password to make it more random
    return ''.join(password_list)  # Convert password back to a string and return it


def search(website) -> tuple | None:
    try:
        with open(file='data/data.json', mode='r') as data_file:
            data = json.load(fp=data_file)  # Load the password file
            username = data[website]['username']  # Get the username for the given website
            password = data[website]['password']  # Get the password for the given website
            return username, password  # Return username and password as a tuple

    except (FileNotFoundError, KeyError, json.decoder.JSONDecodeError) as error:
        # ASSERT: Website doesn't exist in the file either because the file is unable to be read or the user hasn't
        # added info for that site
        print(error)
        return None


def get_passwords() -> dict | None:
    try:
        with open(file='data/data.json') as data_file:
            data = json.load(fp=data_file)  # Gets the password data from the data file
            return data  # Return password data
    except FileNotFoundError:
        # ASSERT: No websites have been added, so we return none
        return None
