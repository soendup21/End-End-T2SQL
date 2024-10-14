print("Number of Bad mark chip is 27.")
print("Number of good chip is 22.")

# Ask the user if the information is correct
user_input = input("Is this correct? (Y for yes, N for no): ")

# Check user response
if user_input.upper() == "Y":
    print("Data sent to database.")
else:
    print("Please verify the data.")