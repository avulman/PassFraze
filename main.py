import eel
import random
import string
import time

eel.init('gui')

@eel.expose
def App(): # app main function
    print("Application Running")
App()

eel.start('index.html', size=(500, 600))

#TODO long-term: allow users the option to save passwords and add them from CLI to google docs or dropbox .txt file
#TODO long-term: encrypt passwords using a library such as hashlib
#TODO long-term: implement brute force protection by limiting login attempts CAPTCHA challenges to prevent bots
#TODO long-term: add support for MFA
#TODO construct password manager and have it work with this program to import generated passwords there

def crack_password(password=None):
    if not password:
        password = input("Enter the password you would like me to crack: ")
    start_time = time.time()
    attempts = 0
    while True:
        attempt = generate_random_characters(len(password), string.ascii_letters + string.digits + string.punctuation)
        attempts += 1
        if attempt == password:
            end_time = time.time()
            time_taken = end_time - start_time
            print(f"Attempt {attempts:,}: {attempt}")
            print(f"\nYour password was: {attempt}")
            print(f"It took {attempts:,} attempts and {time_taken:.2f} seconds to crack your password.")
            break
        else:
            print(f"Attempt {attempts:,}: {attempt}")

def generate_random_characters(length, characters):
    return ''.join(random.choice(characters) for _ in range(length))

def generate_weak_password(length):
    with open('common-words.txt', 'r') as file:
        common_words = [line.strip() for line in file]

    chosen_word = random.choice(common_words)

    while len(chosen_word) > length:
        chosen_word = chosen_word[:-1]

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
        #time.sleep(2)
        print("It's time to decide how long you want your password to be.")
        #time.sleep(2)
        print("The perk of having passwords that are at least 12 characters long, is that they typically aren't considered weak by default.")
        #time.sleep(2)
        print("Typically passwords also can't exceed 128 characters, so your max character count is 128.")
        #time.sleep(2)
        length = int(input("Enter the desired length of your password: "))
        if length < 2:
            print("Sorry, your password length should be at least 2 characters.")
            return
        elif length >= 129:
            print("Your password is too long. Typical password length shouldn't exceed 128 characters. ")
            return
        
        print("Now it's time to choose the strength of your password!")
        #time.sleep(1)
        strength = input("Choose password strength weak (enter '1'), medium (enter '2'), or strong (enter '3'): ").lower()
        
        if strength not in ["1", "2", "3"]:
            print("Invalid strength level. Please choose from weak (enter '1'), medium (enter '2'), or strong (enter '3').")
            return
        
        if strength == "1":
            print("Generating a weak password...")
            password = generate_weak_password(length)
        elif strength == "2":
            print("Generating a medium strength password...")
            password = generate_medium_password(length)
        elif strength == "3":
            print("Generating a strong password...")
            password = generate_strong_password(length)
        else:
            raise ValueError("Invalid strength level. Please choose from weak (enter '1'), medium (enter '2'), or strong (enter '3').")
        
        print("Generated Password:", password)

        crack_option = input("Would you like me to attempt cracking this password? If yes (enter '1') if no (enter '2'): ")
        if crack_option == "1":
            crack_password(password)
        elif crack_option == "2":
            print("No problem! Terminating program...")
        else:
            print("Invalid entry.")

    except ValueError:
        print("Please enter a valid integer for the password length.")

def contains_common_word(password):
    with open('common-words.txt', 'r') as file:
        common_words = [line.strip() for line in file]

    for word in common_words:
        if word.lower() in password.lower():
            return True

    return False

def test_own_password():
    print("Let's test that password!")

    while True:
        user_password = input("Enter the password that you would like to test: ")

        if contains_common_word(user_password):
            print("Your password contains a common word, and will therefore be considered weaker.")
            action = input("Would you like to: proceed (enter '1'), choose a different password (enter '2'), or exit (enter) '3'): ").lower()

            if action == "1":
                break
            elif action == "2":
                continue
            elif action == "3":
                print("Terminating program...")
                return
            else:
                print("Invalid entry.")
        else:
            print("Analyzing password...")
            break

    test_password_strength(user_password)

    while True:
        crack_option = input("Would you like me to attempt cracking this password? If yes (enter '1') if no (enter '2'): ")
        if crack_option == "1":
            crack_password(user_password)
            break
        elif crack_option == "2":
            print("No problem! Terminating program...")
            break
        else:
            print("Invalid entry.")

def main():
    try:
        print("Welcome to PassFraze! This tool allows you to generate passwords, test the strength of your own passwords, and even cracks passwords!")
        #time.sleep(2)
        action = input("Would you like to generate a password (enter '1'), test the strength of your own password (enter '2'), or watch me crack a ('enter 3') a password?\n").lower()

        if action == "1":
            generate_password()
        elif action == "2":
            test_own_password()
        elif action == "3":
            crack_password()
        else:
            print("Invalid entry. Please type '1' to generate or '2' to test.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
