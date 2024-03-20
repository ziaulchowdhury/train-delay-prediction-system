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
user_response = int(input("Please enter a number: "))

# Displaying user input
print("You entered:", user_response)

# Code needs to be added here. General idea:
# The program calls the model that predicts the time deviation at arrival of last stop. 

# Example model output
model_output = "on time"  # This is a placeholder for the actual model prediction
percentage = "48" #example percentage. 

# Final output message
print("When you travel by train from", numbered_stations[user_response-1][1],"to",numbered_stations[user_response-1][2],", this model predicts that you will arrive", model_output,"with",percentage,"% probability.")
