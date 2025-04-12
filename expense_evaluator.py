from collections import defaultdict

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
    """Determines if a user exists"""
    sameNameDict = defaultdict(list)
    currentIndex = 0
    for userDetail in usersList:
        if userDetail == name and usersList[currentIndex + 1] == password:
            sameNameDict[name] = usersList[currentIndex + 1] #gets and store all the users with the same username
            return True
        currentIndex  = currentIndex + 1


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

def available_options():
    pass

def login_user(name, password):
    exists = user_exists(name, password)
    if exists:
        try:
            available_options()
        except Exception as e:
            print(f"Unable to process login now... {e}\nQuiting...")
    else:
        message = "The user does not exists. Would you like to create an account? [1] for yes, [0] for no: "
        response = validate_input(message)
        if response in [0,1]: # ensure the value is either 0 or 1
            if response == 1:
                create_user()
            else:
                print("Ending Session...\nOpen app to try again...")
                exit()



        
login_user("charles", 0000)         
usersFile.close()