# ------------------------------------------------------------------------------------------ 
# Title: Assignment05
# Desc: This assignment demonstrates using dictionaries, files (JSON), and exception handling
#       to manage course registrations.
# Change Log: (Who, When, What)
# Mohiuddin Khan,11/12/2025,Completed Assignment05 with dictionaries, JSON, and exceptions
# ------------------------------------------------------------------------------------------ 

# -----------------------------
# Import Modules
# -----------------------------
# json is used to read/write the list of dictionaries to a JSON file.
# io (imported as _io) is used so we can type the file variable as _io.TextIOWrapper.
import json
import io as _io

# -----------------------------
# Define the Data Constants
# -----------------------------
# MENU: This constant holds the menu text shown to the user.
# It does NOT change while the program runs.
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course
    2. Show current data  
    3. Save data to a file
    4. Exit the program
----------------------------------------- 
'''

# FILE_NAME: This constant holds the name of the JSON file we use for storage.
# It does NOT change while the program runs.
FILE_NAME: str = "Enrollments.json"

# -----------------------------
# Define the Data Variables
# -----------------------------
# These variables will store the data the user enters while the program runs.

student_first_name: str = ''      # Holds the first name of a student entered by the user.
student_last_name: str = ''       # Holds the last name of a student entered by the user.
course_name: str = ''             # Holds the course name entered by the user.
student_data: dict = {}           # Holds one row of student data as a dictionary.
students: list = []               # Holds multiple rows of student data (list of dictionaries).
file = _io.TextIOWrapper          # Will hold a reference to an opened file.
menu_choice: str = ''             # Holds the user's menu selection.

# ------------------------------------------------------------------------------------------ 
# Startup Processing: Load existing data from the JSON file into the students list
# ------------------------------------------------------------------------------------------ 
# When the program starts, we try to open "Enrollments.json" and load its data
# into the students list. We use structured error handling (try/except/finally)
# so the program does not crash if the file is missing or invalid.

try:
    file = open(FILE_NAME, "r")
    students = json.load(file)          # Expecting a list of dictionaries.
    file.close()
except FileNotFoundError as e:
    print("The enrollment file must exist before running this script!\n")
    print("-- Technical Error Message --")
    print(e, e.__doc__, type(e), sep="\n")
except json.JSONDecodeError as e:
    print("The enrollment file contains invalid JSON data.\n")
    print("-- Technical Error Message --")
    print(e, e.__doc__, type(e), sep="\n")
except Exception as e:
    print("There was a non-specific error while reading the file!\n")
    print("-- Technical Error Message --")
    print(e, e.__doc__, type(e), sep="\n")
finally:
    # Make sure the file is closed if it was successfully opened.
    try:
        if file.closed is False:
            file.close()
    except Exception:
        # If file was never opened correctly, we simply ignore this.
        pass

# ------------------------------------------------------------------------------------------ 
# Main Program Loop
# ------------------------------------------------------------------------------------------ 
# This while loop repeatedly:
#   1) Shows the menu
#   2) Asks the user for a menu choice
#   3) Runs the correct block of code for that menu choice

while True:

    # -----------------------------
    # Show the Menu (Output)
    # -----------------------------
    print(MENU)
    menu_choice = input("What would you like to do: ").strip()
    print()  # Add a blank line for nicer spacing.

    # ------------------------------------------------------------------ 
    # Menu Choice 1: Register a Student for a Course (Input + Processing)
    # ------------------------------------------------------------------ 
    # This section:
    #   - Prompts the user for first name, last name, and course name.
    #   - Uses structured error handling to validate names (no numbers).
    #   - Stores the data in a dictionary and adds it to the students list.
    if menu_choice == "1":
        try:
            # Get and validate first name
            student_first_name = input("Enter the student's first name: ").strip()
            if not student_first_name.isalpha():
                raise ValueError("First name must contain only letters (no numbers or symbols).")

            # Get and validate last name
            student_last_name = input("Enter the student's last name: ").strip()
            if not student_last_name.isalpha():
                raise ValueError("Last name must contain only letters (no numbers or symbols).")

            # Get course name (no special rules given, so we just strip spaces)
            course_name = input("Please enter the name of the course: ").strip()

            # Create a dictionary for this student's data
            student_data = {
                "FirstName": student_first_name,
                "LastName": student_last_name,
                "CourseName": course_name
            }

            # Add the dictionary to the list of students
            students.append(student_data.copy())

            # Confirm to the user that the registration was captured
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.\n")

        except ValueError as e:
            # These are our custom validation errors for the names
            print(e)
            print("-- Technical Error Message --")
            print(e.__doc__)
            print(e.__str__())
        except Exception as e:
            # Catch any other unexpected errors
            print("There was a non-specific error while entering student data!\n")
            print("-- Technical Error Message --")
            print(e, e.__doc__, type(e), sep="\n")

        continue  # Go back to the menu

    # ------------------------------------------------------------------ 
    # Menu Choice 2: Show current data (Output)
    # ------------------------------------------------------------------ 
    # This section:
    #   - Loops through the students list.
    #   - Displays a sentence about each student's registration.
    #   - Also shows the same data as a comma-separated string.
    elif menu_choice == "2":
        if not students:
            print("No registrations to display yet.\n")
        else:
            print("-" * 50)
            for student_data in students:
                first = student_data.get("FirstName", "")
                last = student_data.get("LastName", "")
                course = student_data.get("CourseName", "")

                # Descriptive message
                print(f"Student {first} {last} is enrolled in {course}")

                # Comma-separated values (CSV-style) for each row
                print(f"{first},{last},{course}")
            print("-" * 50)
            print()
        continue  # Go back to the menu

    # ------------------------------------------------------------------ 
    # Menu Choice 3: Save data to a file (Processing + Output)
    # ------------------------------------------------------------------ 
    # This section:
    #   - Opens "Enrollments.json" in write mode.
    #   - Writes the students list (list of dictionaries) as JSON.
    #   - Uses structured error handling to catch file/JSON errors.
    #   - Shows the user what was saved.
    elif menu_choice == "3":
        try:
            file = open(FILE_NAME, "w")
            # Write the list of dictionaries to the JSON file
            json.dump(students, file, indent=2)
            file.close()

            print("The following data was saved to file!\n")
            if not students:
                print("(There were no registrations to save.)\n")
            else:
                for student_data in students:
                    first = student_data.get("FirstName", "")
                    last = student_data.get("LastName", "")
                    course = student_data.get("CourseName", "")
                    print(f"{first},{last},{course}")
                print()
        except TypeError as e:
            print("Please check that the data can be converted into valid JSON.\n")
            print("-- Technical Error Message --")
            print(e, e.__doc__, type(e), sep="\n")
        except Exception as e:
            print("There was an error while trying to save the data!\n")
            print("-- Technical Error Message --")
            print(e, e.__doc__, type(e), sep="\n")
        finally:
            # Make sure the file is closed if it was successfully opened.
            try:
                if file.closed is False:
                    file.close()
            except Exception:
                pass

        continue  # Go back to the menu

    # ------------------------------------------------------------------ 
    # Menu Choice 4: Exit the program
    # ------------------------------------------------------------------ 
    elif menu_choice == "4":
        print("Program Ended.Thank you for your input. Have a Great Day!")
        break  # Exit the while loop and end the program

    # ------------------------------------------------------------------ 
    # Handle invalid menu choice (Error)
    # ------------------------------------------------------------------ 
    else:
        print("Please only choose option 1, 2, 3, or 4.\n")
        continue
