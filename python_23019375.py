import random
import datetime
from datetime import datetime, timedelta
import os
# Defining a function to clear the screen for better clarity
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Assigning variables to the text files
RESERVATION_FILE = "reservation_23019375.txt"
MENU_FILE = "menuItems_23019375.txt"

# Defining an add reservation function 
def add_reservation():
    clear_screen()
# Obtaining the customers name and ensuring that the name entered is valid
    while True:
            customer_name = input("Enter customer name : ")
            if not all(c.isalpha() or c.isspace() for c in customer_name):
                print("Please enter a valid name")
                continue

# Prompting the customer to enter a valid reservation date at least 5 days before the current date
            while True:
                date_of_reservation = input("Enter reservation date (YYYY-MM-DD): ")

                # try-except sequence as a precaution against unwanted inputs
                try:
                    date_of_reservation = datetime.strptime(date_of_reservation, "%Y-%m-%d")
                except ValueError:
                    print("Oops it seems like you have entered an incorrect date format, please try again")
                    continue

                # Ensuring current date is at least 5 days before the reservation date
                if date_of_reservation >= datetime.now() + timedelta(days=5) :
                    break
                else:
                    print("Apologies, please ensure that revervation bookings are made at least 5 DAYS in advance \nTodays date is:", datetime.now().strftime("%A, %Y-%m-%d"))
            break
    
# Reading the reservations from the text file
    with open(RESERVATION_FILE, "r") as file:
        reservations = file.readlines()

# Counting the reservations present for each time slot
    time_slot_counts = {
        "Slot 1": 0,
        "Slot 2": 0,
        "Slot 3": 0,
        "Slot 4": 0,
    }

    for reservation in reservations:
        parts = reservation.split("|")
        time_slot = parts[1].strip() 
        if time_slot in time_slot_counts:
            time_slot_counts[time_slot] += 1
        else:
            print(f"Invalid time slot: {time_slot}")

# Displaying the time slots suitable for reservation and number of remaining reservations present and promtpting the user for a desired slot

        reservation_session_prompt = (
            "Enter reservation session (1, 2, 3, 4):\n"
        
            f"1. 12:00 pm - 02:00 pm ({8 - time_slot_counts['Slot 1']} spots left)\n"
            f"2. 02:00 pm - 04:00 pm ({8 - time_slot_counts['Slot 2']} spots left)\n"
            f"3. 06:00 pm - 08:00 pm ({8 - time_slot_counts['Slot 3']} spots left)\n"
            f"4. 08:00 pm - 10:00 pm ({8 - time_slot_counts['Slot 4']} spots left)\n"
        )

# Checking the choice made by the user as well as its validity in accordance with the time slots and the input received
    while True:
        reservation_session_choice = input(reservation_session_prompt)
        if reservation_session_choice in ["1", "2", "3", "4"]:
            reservation_session = {
                "1": "Slot 1",
                "2": "Slot 2",
                "3": "Slot 3",
                "4": "Slot 4",
         }[reservation_session_choice]
            if time_slot_counts[reservation_session] >= 8:
                print("Sorry, the selected time slot is fully booked. Please choose a different time slot.")
            else:
                break
        else:
                print("Apologies, we are unable to find your reservation session, please try again.")


# Enquiring the number of people involved within the booking and ensuring a value between 1 and 4 and checking its validity
    while True:
        try:
            number_of_people = int(input("Enter number of people (Max 4 pax): "))
        except ValueError:
            print("Oops, It seems that you have not entered a number, please try again.")
            continue

        if 1 <= number_of_people <= 4:
            break
        elif number_of_people < 1:
            print("It seems you have entered a number too low, please try again")
        else:
            print("Apologies, we are only able to accomodate a maximum of 4 people in a reservation.")

# Prompting the customer to enter contact information and ensuring the number formating is accurate  
    while True:
        contact_number = input("Enter your phone number (without hyphens): ")
        if not all(c.isdigit() for c in contact_number):
            print("Invalid contact number format, please try again.")
            continue
        if len(contact_number) > 11:
            print("Oops it seems like you have entered too many numbers, please try again.")
            continue
        if len(contact_number) < 10:
            print("Oops it seems like you have entered too little numbers, please try again.")
            continue
        
        break

# Obtaining the email address from the customer ensuring the format of the email address given is valid ad formatted appropriately    
    while True:
        email_address = input("Enter email address: ")
        if "@" not in email_address or "." not in email_address:
            print("Invalid email address format, please try again.")
            continue
        break
                
# Writing reservation details obtained within the reservation text file 
    with open(RESERVATION_FILE, "a") as file:
                    reservation = f"{date_of_reservation}|{reservation_session}|{customer_name}|{email_address}|{contact_number}|{number_of_people}\n"
                    file.write(reservation)
                
    print("Reservation added successfully!")
    input("Press Enter to continue: ")

# Clearing the screen
    clear_screen()

# Defining a function to cancel a reservation
def cancel_reservation():
    # Prompting the user to enter the reservation details
    customer_name = input("Enter customer name: ")
    date_of_reservation = input("Enter reservation date (YYYY-MM-DD): ")
    reservation_session = input("Enter reservation session: ")
    
    # Reading the reservation details from the text file
    with open(RESERVATION_FILE, "r") as file:
        reservations = file.readlines()
    
    # Checking and erasing the reservation if present within the text file and rewriting the updated reservations unto the updated file
    updated_reservations = []
    found = False
    for reservation in reservations:
        if (
            customer_name.lower() in reservation.lower()
            and reservation_session.lower() in reservation.lower()
            and date_of_reservation.lower() in reservation.lower()
        ):
            found = True
        else:
            updated_reservations.append(reservation)

    # Rewriting back the updated reservations unto the original reservation file and informing if there are no associated reservations present within the file
    if found:
        with open(RESERVATION_FILE, "w") as file:
            file.writelines(updated_reservations)
        
        print("Your reservation has been canceled successfully.")
    else:
        print("Apologies, it seems your reservation is not present within our system")

# Function to update/edit reservation(s)
def update_reservation():
    
  while True:
      currentList = []  # to store the current reservations uphold
      currentIndex = 0  # get the reservation index number.
      exitProg = 0
  
      try:
          with open(RESERVATION_FILE, 'r') as f:  # Opens the text file as a list
              content = f.readlines()
              f.close()
  
      except IOError as e:  # error if file is not read
          print(e)
          print("File was not read!")
  
      # User inputs email to find reservations
      while True:
          enteredEmail = input("Please enter email to change reservations: ")
  
          if "@" not in enteredEmail or "." not in enteredEmail:  # if the email format is incorrect
              print("Wrong format!")
              continue
          else:
              print("Finding reservations....")
  
          for firstLoop in content:
              if enteredEmail in firstLoop:
                  print("Reservation found!")
                  currentList = firstLoop.split("|")
                  currentIndex = content.index(firstLoop)  # saves the index number for the reservations
                  exitProg += 1
                  break
  
          if exitProg != 0:  # based on the changes above
              break
          else:
              print("Reservation not found!")
              continue  # else the program will continue running below
  
      # Prints out the account details
      print("Date: ", currentList[0])
      print("Slot: ", currentList[1])
      print("Name: ", currentList[2])
  
      # prompts the user to choose changes made
      print("Which would you like to change?")
      print("1. Date & Slot")
      print("2. Name")
  
      selection = int(input("Enter selection: "))
  
      # if user chose to change date and slot
      if selection == 1:
          while True:
              newReservation = input("Please enter new reservation date: (YYYY-MM-DD)")  # user will input desired date
              try:  # the program will convert the string input into datetime format.
                  newReservation = datetime.strptime(newReservation, "%Y-%m-%d")
              except ValueError:  # if the format is wrong it requests the user to input again.
                  print("It seems you have an incorrect date format, please try again")
                  continue
              if newReservation >= (datetime.now() + timedelta(days=5)):  # If the reservation is made 5 days advance
                  print()
                  while True:
  
                      # user will be given the choice to re-choose the slot
                      newSlot = input("Please input new slot: [1, 2, 3, 4]")
                      try:
                          # check if the slot entered is in numbered format or not
                          newSlot = int(newSlot)
  
                      except ValueError:
                          print("Wrong Format!")
                          continue  # re-loop the program
  
                      # check if user enters a slot that does not exist
                      if (newSlot <= 0) or (newSlot > 4):
                          print("Invalid slot")
                          continue
  
                      else:
                          counter = 0
                          newReservation = newReservation.strftime("%Y-%m-%d")
                          # counts how many users has booked the slot on the same date.
                          for x in content:
                              counter = 0
                              if x != content[currentIndex]:  # anything except the current one
                                  if str(newSlot) and str(newReservation) in x:  # if the slot and the reservation repeats,
                                      counter += 1  # the counter increases
                          # if counter exceeds 8 or is 8, it will prompt the user to choose another slot.
  
                          if counter >= 8:
                              print("The current slot selected is FULL. Please select a new one.")
                              continue
  
                          # prompts if the user confirms to make the changes above as desired.
                          print("Existing Date: " + currentList[0])
                          print("New Date: " + newReservation)
                          print("Existing Slot: " + currentList[1])
                          print("New Slot: Slot " + str(newSlot))
                          while True:
                              # additional confirmation
                              confirmation = input("Are you sure you are about to make these changes? (Y/N): ")
  
                              # user declines to change
                              if confirmation.upper() == "N":
                                  print("Update cancelled.")
                                  break
  
                              # user agrees to change
                              elif confirmation.upper() == "Y":
  
                                  # update reservations code
                                  g = open(RESERVATION_FILE, 'w')
                                  # begins to replace every content except the updated one
                                  for x in content:
                                      # if the content is the about to be updated one, skip
                                      if content.index(x) == currentIndex:
                                          print()
                                      else:
                                          g.write(x)  # rewrite the existing content
  
                                  updateInfo = newReservation + "|" + "Slot " + str(newSlot) + "|" + currentList[2] + "|" + currentList[3] + "|" + currentList[4] + "|" + currentList[5]
                                  g.write(updateInfo)  # rewrite the new changes made
                                  g.close()  # close the textfile
                                  break
                              else:
                                  print("Wrong input.")  # if user inputs otherwise
                                  continue
                          break
                  print("Changes has been made.")  # tells the user that a change has been made
                  break
              else:  # prints out notice which booking must be made 5 days in advance
                  print("Sorry! Your booking must be made 5 DAYS in advance!")
                  print("Today's date is", datetime.now().strftime("%Y-%m-%d"))
  
  
      if selection == 2:
          customerName = ""  # null
          while True:
              customerName = input("Enter customer name : ")
              if not all(c.isalpha() or c.isspace() for c in customerName):  # check if the customer name only contains a-z
                  print("Please enter a valid name")
                  continue
  
              print("Existing Name: " + currentList[2])
              print("New Name: " + customerName)
              while True:
                  confirmation = input("Are you sure you are about to make these changes? (Y/N): ")  # additional confirmation
  
                  # user declines
                  if confirmation.upper() == "N":
                      print("Update cancelled.")
                      break
  
                  # User agrees and proceeds
                  elif confirmation.upper() == "Y":
  
                      # update reservations
                      g = open(RESERVATION_FILE, 'w')
                      # begins to replace every content except the updated one
                      for x in content:
                          # if the content is the about to be updated one, skip
                          if content.index(x) == currentIndex:
                              print()
                          else:
                              g.write(x)  # rewrite the existing content
  
                      updateInfo = currentList[0] + "|" + currentList[1] + "|" + customerName.upper() + "|" + currentList[
                          3] + "|" + currentList[4] + "|" + currentList[5]
                      g.write(updateInfo)  # updates the new data
                      g.close()
                      print("changes saved.")  # notifies the user that a change has been made.
                      break
                  break
              break
      repeatSelection = input("Would you like to edit another reservation? (Y/N):")  # prompts user
      # user agrees to edit another
      if repeatSelection.upper() == "Y":
          continue
      # user rejects to edit another
      elif repeatSelection.upper() == "N":
          break
      # invalid input
      else:
          print("Enter a valid input!")
# Function to display all reservations
def display_reservations():
    # Read reservations from  the textfile
    with open(RESERVATION_FILE, "r") as file:
        reservations = file.readlines()
    
    # Display reservations
    if reservations:  # if the reservation contains contents and not null:
        print("All Reservations:")
        print("Date\t\tSlot\tName\t\t\te-mail\t\t\tPhone\t\t\tNumber of pax")  # prints out each reservations
        print("----------------------------------------------------------")
        for singleReservation in reservations:
            parts = singleReservation.split("|")
            print(f"{parts[0]}\t{parts[1]}\t\t{parts[2]}\t\t{parts[3]}\t{parts[4]}\t{parts[5]}")
    else: # if the text file has zero data inside.
        print("No reservations found.")

# Function to generate meal recommendation
def generate_recommendation():
    # Read menu items from file
    with open(MENU_FILE, "r") as file:
        menuItems = file.readlines()
    
    # Select random recommendation
    rec = random.choice(menuItems)  # pick one of the food choice randomly.
    
    print("Meal Recommendation:")
    print(rec)  # displays the food choice

# Main menu loop
while True :
    print("Charming Thyme Trattoria Restaurant Management System")
    print("Welcome! How may we help you today")
    print(datetime.now().strftime("%A, %Y-%m-%d [%H:%M:%S]"))
    print("------Main menu------")
    print("1. Add Reservation(s)")
    print("2. Cancel Reservation(s)")
    print("3. Update/Edit Reservation(s)")
    print("4. Display Reservations")
    print("5. Generate Meal Recommendation")
    print("6. Exit the menu")
    
    action = input("What is your desired action (1-6): ")
    
    if action == "1":
        add_reservation()
    elif action == "2":
        cancel_reservation()
    elif action == "3":
        update_reservation()
    elif action == "4":
        display_reservations()
    elif action == "5":
        generate_recommendation()
    elif action == "6":
        print("Exiting.")
        break
    else:
        print("Apologies, we are unable to fulfill that request. Please try again.")
        
    input("Press Enter to continue: ")
    clear_screen()
