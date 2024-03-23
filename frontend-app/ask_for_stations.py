# NEW VERSION 2024-03-23
from datetime import datetime

# Welcome message
print("""Welcome to the train arrival predictor! Choose your stations of departure and arrival and the machine learning model will predict if your train will arrive on time (=max 5 min late) at the final station.""")

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

# Ask the user to input a date in the Swedish format
user_input = input("Please enter a date (yyyy-mm-dd): ")

# Convert the string to a datetime object
try:
    user_date = datetime.strptime(user_input, "%Y-%m-%d")
#    print(f"You entered: {user_date.date()}")
except ValueError:
    print("Incorrect format, please enter the date in yyyy-mm-dd format.")

# Displaying user input
print(f"You have chosen {numbered_stations[user_stations_nb-1][1]}-{numbered_stations[user_stations_nb-1][2]} on {user_date.date()}")

# Code needs to be added here, calling the ML model. The result from the ML model is in the code below named "model_output". 
# The program calls the model that predicts the time deviation at arrival of last stop. 

# Example model output
model_output = "on time"  # Remove this when the ML model works. 

# Final output message
print(f"When you travel {numbered_stations[user_stations_nb-1][1]}-{numbered_stations[user_stations_nb-1][2]} on {user_date.date()} this model predicts that you will arrive {model_output}")
