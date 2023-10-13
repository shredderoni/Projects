import random, string

def generate_password(min_length, numbers=False, special_characters=False):
    letters = string.ascii_letters
    digits = string.digits
    special = string.punctuation

    characters = letters
    if numbers:
        characters += digits
    if special_characters:
        characters += special

    pwd = ""
    meets_criteria = False
    has_number = False
    has_special = False

    while not meets_criteria or len(pwd) < min_length:
        new_char = random.choice(characters)
        pwd += new_char

        if new_char in digits:
            has_number = True
        elif new_char in special:
            has_special = True

        meets_criteria = True
        if numbers:
            meets_criteria = has_number
        if special_characters:
            meets_criteria = meets_criteria and has_special
        
    return pwd

while True:
    try:
        min_length = int(input('\nEnter minimum length: '))
        break
    except ValueError:
        print("\nEnter a number!")
while True:
    has_number = input('\nDo you want to have numbers? (y/n): ')
    match has_number.upper():
        case "Y" | "YES":
            has_number = True
            break
        case "N" | "NO":
            has_number = False
            break
        case _:
            print("Enter a valid option!")
while True:
    has_special = input('\nDo you want to have special characters? (y/n): ')
    match has_special.upper():
        case "Y" | "YES":
            has_special = True
            break
        case "N" | "NO":
            has_special = False
            break
        case _:
            print("Enter a valid option!")

print(generate_password(min_length, has_number, has_special))