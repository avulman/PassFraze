def valid_password(password):
    if ' ' in password:
        print("Password may not contain a space.")
        return 
    if len(password) <= 7:
        print("The password you have entered is to short and doesn't meet the criteria.")
        return False
    if sum(1 for c in password if c.isupper()) < 2:
        print("The password you have entered doesn't contain at least 2 capital letters.")
        return False
    if sum(1 for c in password if c.islower()) < 2:
        print("The password you have entered doesn't contain at least 2 lowercase letters.")
        return False
    if sum(1 for c in password if c.isdigit()) < 2:
        print("The password you have entered doesn't contain at least 2 digits.")
        return False
    
    return True

password = input("Welcome to password guesser!\nChoose a password, and I'll try to guess it!\nYour password must contain:\n- No spaces\n- At least 2 capital letters\n- At least 2 lowercase letters\n- At least 2 numbers\n- At least 2 unique characters\nEnter a password: ")

if valid_password(password):
    print("Password is valid.\nInitializing password guesser...")
else:
    print("Come back when you're ready to type in a valid password!")