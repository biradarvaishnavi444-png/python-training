# dictionary
# Hostel Visitor Log System

hostel_visitors = {
    "hostel_name": "Government Polytechnic Hostel",
    "warden":"Mrs. Desai",
    "city": "Hingoli",
    "contact": "1234567890",
}

# List of Dictionaries (5 Records)

visitors = [
    {"ID": 1, "Name": "Samiksha", "Room": 101,  "Entry": "10:00 AM", "Status": "Inside"},
    {"ID": 2, "Name": "Priya", "Room": 102, "Entry": "10:30 AM", "Status": "Exited"},
    {"ID": 3, "Name": "Tejal", "Room": 103, "Entry": "11:00 AM", "Status": "Inside"},
    {"ID": 4, "Name": "Anuja", "Room": 104,  "Entry": "11:30 AM", "Status": "Inside"},
    {"ID": 5, "Name": "Divya", "Room": 105, "Entry": "12:00 PM", "Status": "Exited"}
]

# Bonus: Second Dictionary Type
room_warden = {
    101: "Mr. Patil",
    102: "Mr. Sharma",
    103: "Mrs. Joshi",
    104: "Mr. Kulkarni",
    105: "Mrs. Desai"
}

# Function to get visitor status
def get_status(visitor_id):
    for visitor in visitors:
        if visitor["ID"] == visitor_id:
            return visitor["Status"]
    return "Visitor Not Found"

# Function to search records
def search_records(name):
    for visitor in visitors:
        if visitor["Name"].lower() == name.lower():
            return visitor
    return "Record Not Found"

# Print all records using loop
print("HOSTEL VISITOR LOG SYSTEM")
print("-" * 40)

for visitor in visitors:
    print("ID:", visitor["ID"])
    print("Name:", visitor["Name"])
    print("Room:", visitor["Room"])
    print("Entry Time:", visitor["Entry"])
    print("Status:", visitor["Status"])
    print("Warden:", room_warden[visitor["Room"]])
    print("-" * 40)

# Test get_status()
print("\nVisitor Status:")
print("Visitor ID 3:", get_status(3))

# Test search_records()
print("\nSearch Record:")
print(search_records("Anuja"))