from collections import defaultdict, OrderedDict
import hashlib
import getpass
import datetime

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
    print("[5] = Display History")
    print("[6] = Logout")

#obtains the daily expenses (if selected)
def set_user_expense():
    selectedCategory = validate_input("Category = ")
    if selectedCategory == 5:
        display_user_expense_history()
    elif selectedCategory == 6:
        global userDet
        logout_user(userDet)

    endRequest = validate_input("Enter [1] to proceed: ")
    if endRequest not in [0,1]:
        print("Invalid input value, only [0] and [1] are allowed...")
        
    userItems = defaultdict(list)    
    while endRequest != 0 and endRequest == 1:
        amount = validate_input("Enter the expense amount: ")
        match selectedCategory:
            case 0:
                categories["food"]["food"].append(amount)
                userItems["food"].append(amount)
            case 1:
                categories["transport"]["transport"].append(amount)
                userItems["transport"].append(amount)
            case 2:
                categories["books"]["books"].append(amount)
                userItems["books"].append(amount)
            case 3:
                categories["bills"]["bills"].append(amount)
                userItems["bills"].append(amount)
            case 4:
                categories["entertainment"]["entertainment"].append(amount)
                userItems["entertainment"].append(amount)
            case _:
                print("This category doesn't exists!!!")
        
        endRequest = validate_input("Enter [0] to terminate and [1] to proceed: ")
    user = user_session(userDet)
    user["Category"] = categories #stores the category data in the user session
    continueProcess = validate_input("Would you like to continue the process? [0] for no, [1] for yes: ")
    if continueProcess == 1:
        display_category()
        set_user_expense()
    else:
        categoriesKey = categories.keys()
        process_sum_message(categoriesKey)
        update_user_expense_db(userItems)
        user_dashboard(userDet)

# Processes the sum total
def process_sum_message(name):
    """Processes sums for given categories and updates user session."""
    global userDet
    name = sorted(name)
    sorted_categories = OrderedDict(sorted(categories.items()))
    user = user_session(userDet)
    i = 0
    for category_name, category_data in sorted_categories.items():
        if i < len(name) and category_name == name[i]:  # Check if i is within bounds
            if name[i] in category_data:
                total = sum(category_data[name[i]])
                user["Total_Cost"] = total
                print(f"Total of {name[i].capitalize()} sum = {total}")
            i += 1
        elif i >= len(name):
            break; #Prevents index out of bounds error.


def update_user_expense_db(userItems):
    global userDet
    user = user_session(userDet)
    userId = user["userId"]
    userExpense = user["Total_Cost"]
    try:
        with open("users_expenses.txt", "a") as file:
            now = datetime.datetime.now()
            food_items = userItems.get("food", [])
            transport_items = userItems.get("transport", [])
            books_items = userItems.get("books", [])
            bills_items = userItems.get("bills", [])
            entertainment_items = userItems.get("entertainment", [])
            unavailable_items = userItems.get("unavailable", [])

            userDetails = str(userId) + "\t\t" + str(userExpense) + "\t\t\t" + now.strftime("%d / %m / %Y") + \
                          f" Food: {food_items}, Transport: {transport_items}, Books: {books_items}, Bills: {bills_items}, Entertainment: {entertainment_items}, Unavailable: {unavailable_items}\n"
            file.write(userDetails)
            print("--------- Successfully Updated your details ----------")
    except FileNotFoundError:
        print(f"Failed to locate users_expenses.txt. Ensure it exists...")
        return 1
    except Exception as e:
        print(f"Error: Failed to update_user_expense_db, ErrorType: {e} Quitting/Logging out...")
        logout_user(user)
    file.close()


def get_user_expense():
    pass

# Shows the user expenses from the db
def display_user_expense_history():
    global userDet
    user = user_session(userDet)
    userId = user["userId"]
    print("\n--------------- YOUR HISTORY ------------")
    try:
        with open("users_expenses.txt", "r") as file:
            print("Id\tTotal_Spent\tDate\t\tItems")
            result = False
            for data in file:
                if str(userId) in data:
                    print(data.strip())
                    result = True
                    break
            if not result:
                print("\t...No data was found...") # no data was found
            user_dashboard(user)
    except FileNotFoundError:
        print(f"Failed to locate {file}. Ensure it exists...")
        return 1
    except Exception as e:
        print("Error: Failed to display_user_expense_history... Quiting/Logging out...")
        logout_user(user)
    file.close()

  
# USER VALIDATION

def user_session(details):
    """saves the user details over time"""
    return details

def generate_user_id():
    """Generating a unique user id"""    
    try:
        with open("users.txt", "r") as file:
          userId = len(file.readlines()) + 1 #generates a new id
          return userId
    except FileNotFoundError:
        print(f"The file {file} does not exists!!!")
        return 1
    except Exception as e:
        print(f"Error: Something went wrong while generationg an ID. ErrorType: {e}")
        return None
    file.close()


def get_user_id(name, password):
    """Obtains the user id."""
    currentIndex = 0
    while currentIndex < len(usersList) - 1: #Prevent index error
        if usersList[currentIndex] == name and usersList[currentIndex + 1] == str(password):
            return usersList[currentIndex + 2]
        currentIndex += 1
    return False

def set_password(name, password, userId):
    """Inserts the password into the password db"""
    try:
        with open("password.txt", "a") as file:
            userDetails = str(name) + "\t" + str(password) + "\t" + str(userId) + "\n"
            file.write(userDetails)
    except FileNotFoundError:
        print(f"Failed to open the file {file}...")
    except Exception as e:
        print(f"Error: Something went wrong while setting the password. ErrorType: {e}")
    file.close()


def get_password(userId):
    try:
        with open("password.txt", "r") as f:
            lines_arr = f.read().split()  
            current_index = 0
            for value in lines_arr:
                if value == str(userId):
                    return lines_arr[current_index - 1]  #gets the hashed password
                current_index += 1

    except FileNotFoundError:
        print(f"Failed to open the file {f}...")
        return 1
    except Exception as e:
        print(f"Error: Something went wrong while setting the password. ErrorType: {e}")
        return 0
    f.close()

    
def user_exists(name, password):
    """Determines if a user exists and stores all passwords for a given username."""
    currentIndex = 0
    existing_data = open("password.txt", "r")
    existing_data_list = existing_data.read().split() 

    for data in existing_data_list:
        if data == str(name) and existing_data_list[currentIndex + 1] == str(password): #determines if the user exists
            return True 
        currentIndex += 1
    return False

def hash_password(password):
    password = str(password)
    return hashlib.sha256(password.encode()).hexdigest()

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
                    userId = generate_user_id()
                    set_password(newUserName, hash_password(newUserPassword), userId) #sets a hashed password into the password db
                    userDetails = str(newUserName) + " " + str(newUserPassword) + "\t" + str(userId) + "\n"
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
            
            # Login user
            response = "Press [0] to quit and login again: "
            validated_response = validate_input(response)
            if validated_response == 0:
                print("\t\t--------- Goodbye ----------")
                exit()
    except Exception as e:
        print(f"Something went wrong in inserting the user data... {e}")
    
    file.close()

# Login user
def login_user(name, password):
    global userDet 
    password_hashed = hash_password(password)
    exists = user_exists(name, password_hashed)
    if exists:
        try:
            userDetails = {}
            userDetails["name"] = name
            userDetails["password"] = password
            userDetails["userId"] = get_user_id(name, password)
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
    # print("\nFinal summary:\n", session)
    print(session.clear())
    print("\nWe will be glad to see you soon...\n\t...... Goodbye .....")
    exit()

# user dashboard
def user_dashboard(userDetails):
    print(f"\n--------- Welcome {userDetails["name"]}, ID = {userDetails["userId"]} -------------")

    display_category() #display the available options
    set_user_expense()



# process
name = input("name>> ")
password = getpass.getpass("password>> ")
name = name.capitalize()
login_user(name, password) 

usersFile.close()