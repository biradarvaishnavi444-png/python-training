# Hostel Visitor Log System

visitors = []
# Function to add visitor
def add_visitor():
    name = input("Enter Visitor Name: ")
    room = input("Enter Room Number: ")
    entry_time = input("Enter Entry Time: ")

    visitor = [name, room, entry_time, "Not Exited"]
    visitors.append(visitor)

    print("====== Visitor Added Successfully!\n======")

# Function to mark exit

def visitor_exit():
    name = input("Enter Visitor Name for Exit: ")

    for visitor in visitors:
        if visitor[0] == name:
            exit_time = input("Enter Exit Time: ")
            visitor[3] = exit_time
            print("======= Exit Recorded Successfully!\n======")
            return

    print("Visitor Not Found!\n")

# Function for Warden Dashboard
def warden_dashboard():
    print("\n--- Warden Dashboard ---")

    if len(visitors) == 0:
        print("No Visitor Records Available.")
    else:
        for i in range(len(visitors)):
            print("Visitor:", visitors[i][0])
            print("Room No:", visitors[i][1])
            print("Entry Time:", visitors[i][2])
            print("Exit Time:", visitors[i][3])
            print("----------------------")

# Main Menu
for _ in range(10):
    choice = input("Enter Choice: ")

    if choice == "1":
        add_visitor()

    elif choice == "2":
        visitor_exit()

    elif choice == "3":
        warden_dashboard()

    elif choice == "4":
        print("Program Ended.")
        break

    else:
        print("Invalid Choice!")