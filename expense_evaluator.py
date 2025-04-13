from collections import defaultdict

categories = {
    "food" : defaultdict(list),
    "transport" : defaultdict(list),
    "books" : defaultdict(list),
    "bills" : defaultdict(list),
    "entertainment" : defaultdict(list),
    "unavailable" : defaultdict(list)
}
userDet = {}
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

#displays the available category to the user
def display_category():
    print("\nThese are the available category for you to choose from. Use the index numbers 0,1,... to select an option.")
    index = 0
    for option in categories:
        if index == 5:
            break
        print("[", str(index), "] = ", option)
        index = index + 1
    print("[5] = Logout")

#obtains the daily expenses (if selected)
def get_expense():
    selectedCategory = validate_input("Category = ")
    if selectedCategory == 5:
        logout_user(userDet)
    endRequest = validate_input("Enter [1] to proceed: ")
    if endRequest not in [0,1]:
        print("Invalid input value, only [0] and [1] are allowed...")
        
    while endRequest != 0 and endRequest == 1:
        amount = validate_input("Enter the expense amount: ")
        match selectedCategory:
            case 0:
                categories["food"]["food"].append(amount)
            case 1:
                categories["transport"]["transport"].append(amount)
            case 2:
                categories["books"]["books"].append(amount)
            case 3:
                categories["bills"]["bills"].append(amount)
            case 4:
                categories["entertainment"]["entertainment"].append(amount)
            case _:
                print("This category doesn't exists!!!")
        
        endRequest = validate_input("Enter [0] to terminate and [1] to proceed: ")
    continueProcess = validate_input("Would you like to continue the process? [0] for no, [1] for yes")
    if continueProcess == 1:
        get_expense()

def process_sum_message(name):
    for items, value in categories.items():
        if items == name:
            if name in value:
                total = sum(value[name])
                print(f"Total of {name.capitalize()} sum = ", total)
            else:
                print(f"No values were found for {name.capitalize()}...")


def display_user_expense():
    #for food
    process_sum_message("food")
    #for transportation
    process_sum_message("transport")
    #for books
    process_sum_message("books")
    #for bills
    process_sum_message("bills")
    #for entertainment
    process_sum_message("entertainment")
  

# USER VALIDATION
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

# Login user
def login_user(name, password):
    exists = user_exists(name, password)
    if exists:
        try:
            userDetails = {}
            userDetails["name"] = name
            userDetails["password"] = password
            global userDet 
            userDet = userDetails
            user_session(userDetails)
            user_dashboard(userDet)
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

# Logout user
def logout_user(sessionDetails):
    session = user_session(sessionDetails)
    print(session.clear())
    print("\nWe will be glad to see you soon...\n\t...... Goodbye .....")
    exit()

# user dashboard
def user_dashboard(userDetails):
    print(f"\n--------- Welcome {userDetails["name"]} -------------")

    display_category() #display the available options
    get_expense()



# process
name = input("name>> ")
password = input("password>> ")
login_user(name, password) 
usersFile.close()