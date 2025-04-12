from collections import defaultdict

categories = {
    "food" : defaultdict(list),
    "transport" : defaultdict(list),
    "books" : defaultdict(list),
    "bills" : defaultdict(list),
    "entertainment" : defaultdict(list),
    "unavailable" : defaultdict(list)
}

usersFile = open("users.txt", "r")

usersList = (usersFile.read()).split()

def validate_input(message):
    while True:
        value = input(message)
        try:
            value = int(value)
            break
        except ValueError:
            try:
                value  = float(value)
                break
            except ValueError:
                print("Ensure the input value a whole number")
    return value

def user_exists(name, password):
    """Determines if a user exists and stores all passwords for a given username."""
    sameNameDict = defaultdict(list)
    currentIndex = 0
    while currentIndex < len(usersList) - 1: #Prevent index error
        if usersList[currentIndex] == name and usersList[currentIndex + 1] == str(password):
            # print("user = ", usersList[currentIndex], "password = ", usersList[currentIndex + 1])
            sameNameDict[name].append(usersList[currentIndex + 1])  # Store passwords as a list
            return sameNameDict
        currentIndex += 1
    return False

# saves the user details over time
def user_session(details):
    return details


def create_user():
    """Inserts a new user"""
    try:
        with open("users.txt", "a") as file:
            newUserName = newUserPassword = None
            check = True
            while check:
                newUserName  = input("Enter your name>> ")
                newUserPassword  = input("Enter your password>> ")

                exists = user_exists(newUserName, newUserPassword) #checks if the user exists
                if not exists:
                    userDetails = newUserName + " " + newUserPassword
                    file.write(userDetails)
                    if not newUserName and not newUserPassword:
                        print("\nError...ENTER a NAME and a PASSWORD. Try again!")
                        create_user()
                    else:
                        print("New user Created Successfully...")
                        check = False
                else:
                    print("User Already Exists, Quiting...")
                    exit()
    except Exception as e:
        print(f"Something went wrong in inserting the user data... {e}")

#displays the available category to the user
def display_category():
    print("\nThese are the available category for you to choose from. Use the index numbers 0,1,... to select an option.")
    index = 0
    for option in categories:
        if index == 5:
            break
        print("[", str(index), "] = ", option)
        index = index + 1

# user dashboard
def user_dashboard(userDetails):
    print(f"\n--------- Welcome {userDetails["name"]} -------------")
    display_category()

    

def login_user(name, password):
    exists = user_exists(name, password)
    if exists:
        try:
            userDetails = {}
            userDetails["name"] = name
            userDetails["password"] = password
            user_dashboard(userDetails)
        except Exception as e:
            print(f"Unable to process login now... \tErrorDetail: {e}\nQuiting...")
    else:
        message = "The user does not exists. Would you like to create an account? [1] for yes, [0] for no: "
        response = validate_input(message)
        if response in [0,1]: # ensure the value is either 0 or 1
            if response == 1:
                create_user()
            else:
                print("Ending Session...\nOpen app to try again...")
                exit()


# process
name = input("name>> ")
password = input("password>> ")
login_user(name, password)         
usersFile.close()