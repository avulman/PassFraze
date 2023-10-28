from flask import Flask, render_template, request
import random
import string
import time

app = Flask(__name__, static_url_path='/gui', static_folder='gui')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    length = int(request.form['length'])
    include_uppercase = 'uppercase' in request.form
    include_lowercase = 'lowercase' in request.form
    include_digits = 'digits' in request.form
    include_special = 'special' in request.form

    characters = ''

    if include_uppercase:
        characters += string.ascii_uppercase
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_digits:
        characters += string.digits
    if include_special:
        characters += '!@#$%^&*()_+[]{}|;:,.<>?'

    password = generate_password(length, characters)
    return render_template('generate.html', password=password)

def generate_password(length, characters):
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/crack')
def crack():
    return render_template('crack.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/passfraze')
def passfraze():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

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

def contains_common_word(password):
    with open('common-words.txt', 'r') as file:
        common_words = [line.strip() for line in file]

    for word in common_words:
        if word.lower() in password.lower():
            return True

    return False