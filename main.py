#To Do
#Store information in encrypted JSON
#Edit or delete entries
#Password generation
#Cross reference passwords to rockyou.txt



import hashlib
import getpass
import pyfiglet
import json
import os

# Define a file to store the usernames and hashed passwords
data_file = "password_manager.json"
saved_passwords_file = "password_entries.json"

# Create a dictionary to store the username and password
password_manager = {}
saved_passwords = {}

# Load the data from the file if it exists
def load_passwords():
    global password_manager, saved_passwords
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            password_manager = json.load(file)
            
    if os.path.exists(saved_passwords_file):
        with open(saved_passwords_file, 'r') as file:
            content = file.read().strip()  # Read the file and strip whitespace
            if content:  # Check if content is not empty
                saved_passwords = json.loads(content)  # Load JSON only if it's not empty
            else:
                saved_passwords = {}  

# Save the data to a file
def save_passwords():
    with open(data_file, 'w') as file:
        json.dump(password_manager, file)
        
    with open(saved_passwords_file, 'w') as file:
        json.dump(saved_passwords, file)

def welcome():
    welcome_msg = pyfiglet.figlet_format("pyPass")
    print(welcome_msg)
    print("Welcome to the password manager")

def register():
    # Get the username and password from the user
    username = input("Enter your username:\n>//")
    password = getpass.getpass("Enter your password:\n>// ")
    pswdHint = input("Enter a hint for your password:\n>// ")
    pswdHash = hashlib.sha256(password.encode()).hexdigest()

    # Store the username and password hash in the dictionary
    password_manager[username] = pswdHash
    save_passwords()  # Save the updated dictionary to the file
    print("User register complete")

def login():
    username = input("Enter your username:\n>//")
    password = getpass.getpass("Enter your password:\n>//")
    pswdHash = hashlib.sha256(password.encode()).hexdigest()

    # Check if login exists
    if username in password_manager and password_manager[username] == pswdHash:
        print("Login Authorized")
        main()
    else:
        print("Your username or password is invalid")

def handle_user():
    while True:
        choice = input("Enter 1 to log in, 2 to create account:\n>// ")
        if choice == "1":
            login()
        elif choice == "2":
            register()
        else:
            print("Goodbye!")
            break
        
def main():
    while True:
        choice = input("Press 1 to add new entry | Press 2 to view passwords | Press 0 to exit:\n>//")
        if choice == "1":
            pswd_name = input("Enter password name\n Example: Google\n>//")
            password = getpass.getpass("Enter your password:\n>// ")
            pswdHash = hashlib.sha256(password.encode()).hexdigest()
            saved_passwords[pswd_name] = {
                "hashed" : pswdHash,
                "unhashed" : password
            }
            save_passwords()
        if choice == "2":
            with open(saved_passwords_file, 'r') as file:
                saved_info = json.load(file)
            for service, _password in saved_info.items():
                print(f"{service}: {_password['unhashed']}")  
        if choice == "0":
            return
            
            
        

welcome()

if __name__ == "__main__":
    load_passwords()  # Load the stored passwords when the program starts
    handle_user()
