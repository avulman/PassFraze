import random
import string
import time

def generate_random_characters(length, characters):
    return ''.join(random.choice(characters) for _ in range(length))

def generate_weak_password(length):
    with open('common-words.txt', 'r') as file:
        common_words = [line.strip() for line in file]

    chosen_word = random.choice(common_words)
    remaining_length = length - len(chosen_word)

    if remaining_length <= 0:
        return chosen_word

    password = chosen_word + generate_random_characters(remaining_length, string.digits)
    return password

def generate_medium_password(length):
    characters = string.ascii_letters + string.digits
    return generate_random_characters(length, characters)
        
def generate_strong_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return generate_random_characters(length, characters)

def test_password_strength(password):
    with open('common-words.txt', 'r') as file:
        common_words = [line.strip() for line in file]

    criteria = [
        (len(password) >= 12, 3),
        (any(c.isupper() for c in password), 1),
        (any(c.islower() for c in password), 1),
        (any(c.isdigit() for c in password), 1),
        (any(c in string.punctuation for c in password), 1),
        (any(c in string.punctuation for c in password), 1),
        (any(word in password for word in common_words), -3)
    ]

    total_points = sum(points for condition, points in criteria if condition)

    if total_points >= 5:
        print("Your password is strong.")
    elif total_points >= 3:
        print("Your password is medium in strength. Consider adding more unique characters to make it stronger!")
    else:
        print("Your password is weak. Add more characters or consider using a mix of uppercase, lowercase, digits, and special characters.")

def generate_password():
    try:
        print("Sweet! Let's generate your very own password!")
        time.sleep(2)
        print("It's time to decide how long you want your password to be.")
        time.sleep(2)
        print("The perk of having passwords that are at least 12 characters long, is that they aren't weak by default.")
        time.sleep(2)
        print("Typically passwords also can't exceed 128 characters, so your max character count is 128.")
        length = int(input("Enter your desired length of the password: "))
        if length < 2:
            print("Sorry, your password length should be at least 2 characters.")
            return
        elif length >= 129:
            print("Your password is too long. Typical password length shouldn't exceed 128 characters. ")
            return
        
        print("Now it's time to choose the strength of your password!")
        time.sleep(1)
        strength = input("Choose password strength (weak, medium, strong): ").lower()
        
        if strength not in ["weak", "medium", "strong"]:
            print("Invalid strength level. Please choose from 'weak', 'medium', or 'strong'.")
            return
        
        if strength == "weak":
            password = generate_weak_password(length)
        elif strength == "medium":
            password = generate_medium_password(length)
        elif strength == "strong":
            password = generate_strong_password(length)
        else:
            raise ValueError("Invalid strength level. Please choose from 'weak', 'medium', or 'strong'.")
        
        print("Generated Password: ", password)

    except ValueError:
        print("Please enter a valid integer for the password length.")

def test_own_password():
    print("Let's test that password!")
    time.sleep(1)
    user_password = input("Enter the password that you would like to test: ")
    test_password_strength(user_password)

def main():
    try:
        print("Welcome to PassFraze! This tool allows you to generate passwords and test the strength of your own!")
        time.sleep(2)
        action = input("Would you like to generate a password (enter '1') or test the strength of your own password (enter '2')?\n").lower()

        if action == "1":
            generate_password()
        elif action == "2":
            test_own_password()
        else:
            print("Invalid entry. Please type '1' to generate or '2' to test.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
