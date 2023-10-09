import random
import string

def generate_password(length):
    characters= string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    try:
        length = int(input("Enter the desired length of the password: "))
        if length < 2:
            print("Password length should be at least 2 characters.")
            return
        password = generate_password(length)
        print("Generated Password: ", password)
    except ValueError:
        print("Please enter a valid integer fot the password length.")

if __name__ == "__main__":
    main()