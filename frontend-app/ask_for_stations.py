from datetime import datetime

# Welcome message
print("""Welcome to the train arrival predictor! Choose your stations of departure and arrival and the machine learning model will predict if your train will arrive on time (=max 5:59 min late) at the final station.""")

# The list of itineraries that the model has analyzed and that the user can choose from
numbered_stations = [
    [1, "Stockholm", "Göteborg"],
    [2, "Göteborg", "Stockholm"],
    [3, "Stockholm", "Malmö"],
    [4, "Malmö", "Stockholm"] #TO DO: Add more options
]
# Getting user input
print("You can choose from the following itineraries:\n")

# Loop to print each row in a legible format
for row in numbered_stations:
    print(f"{row[0]} {row[1]}-{row[2]}")
user_stations_nb = int(input("Please enter a number: "))

def get_user_date():
    while True:
        user_input = input("Please enter a date (yyyy-mm-dd): ")
        try:
            return datetime.strptime(user_input, "%Y-%m-%d").date()
        except ValueError:
            print("Incorrect format, please enter the date in yyyy-mm-dd format.")

def get_user_time():
    while True:
        user_input = input("Please enter the time in hh:mm format: ")
        try:
            return datetime.strptime(user_input, "%H:%M").time()
        except ValueError:
            print("The time format should be hh:mm (24-hour format). Please try again.")

# Get user input
user_date = get_user_date()
user_time = get_user_time()

# Displaying user input
print(f"You have chosen {numbered_stations[user_stations_nb-1][1]}-{numbered_stations[user_stations_nb-1][2]} on {user_date} at {user_time}")

# Code needs to be added here, calling the ML model. The result from the ML model is in the code below named "model_output". 
# The program calls the model that predicts the time deviation at arrival of last stop. 

# Example model output
model_output = "on time"  # Remove this when the ML model works. 

# Final output message
print(f"When you travel {numbered_stations[user_stations_nb-1][1]}-{numbered_stations[user_stations_nb-1][2]} on {user_date} at approximately {user_time} this model predicts that you will arrive {model_output}")
