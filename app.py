from flask import Flask, render_template, request
import random
import string
import time
import re
import math

with open('common-words.txt', 'r') as file:
        common_words = [line.strip() for line in file]

def contains_common_word(password):
        with open('common-words.txt', 'r') as file:
            common_words = [line.strip() for line in file]

        for word in common_words:
            if word.lower() in password.lower():
                return True

        return False

def contains_date_pattern(password):
    date_patterns = [
        r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
        r'\d{2}-\d{2}-\d{4}',  # MM-DD-YYYY
        r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
        r'\d{4}/\d{2}/\d{2}',  # YYYY/MM/DD
        r'\d{2}-\d{2}-\d{2}',  # MM-DD-YY
        r'\d{2}/\d{2}/\d{2}',  # MM/DD/YY
    ]

    for pattern in date_patterns:
        if re.search(pattern, password):
            return True

    return False

def calculate_unique_characters(password):
    char_frequency = {}
    for char in password:
        char_frequency[char] = char_frequency.get(char, 0) + 1

    unique_characters = 0
    password_length = len(password)
    for char, frequency in char_frequency.items():
        probability = frequency / password_length
        unique_characters -= probability * math.log2(probability)

    return unique_characters

def contains_leet_speak(password):
    leet_dict = {
        'a': ['4', '@'],
        'b': ['8'],
        'c': ['(', '<', '{', '['],
        'e': ['3'],
        'g': ['9', '6'],
        'h': ['#'],
        'i': ['1', '!', '|'],
        'l': ['1', '|', '7'],
        'o': ['0'],
        's': ['5', '$'],
        't': ['+', '7'],
        'z': ['2']
    }

    modified_password = password.lower()

    for char, substitutions in leet_dict.items():
        for substitution in substitutions:
            modified_password = modified_password.replace(substitution, char)

    return modified_password != password.lower() and contains_common_word(modified_password)

app = Flask(__name__, static_url_path='/gui', static_folder='gui')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate')
def generate_home():
    return render_template('generate.html')

@app.route('/test')
def test_home():
    return render_template('test.html')

@app.route('/crack_home')
def crack_home():
    return render_template('crack.html')

@app.route('/generate/pressed', methods=['POST'])
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

    if not characters:
        return render_template('generate.html', error="Choose at least one option to generate.")

    password = generate_password(length, characters)
    return render_template('generate.html', password=password)

def generate_password(length, characters):
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

@app.route('/test/pressed', methods=['POST'])
def test():
    password = request.form['password']

    criteria = [
        (len(password) >= 12, "At least 12 characters", 1),
        (any(c.isupper() for c in password), "Contains an uppercase letter", 1),
        (any(c.islower() for c in password), "Contains a lowercase letter", 1),
        (any(c.isdigit() for c in password), "Contains a digit", 1),
        (any(c in string.punctuation for c in password), "Contains a special character", 1),
        (not contains_common_word(password), "Contains a common word", 1),
        (not contains_date_pattern(password), "Avoids date patterns", 1),
        (calculate_unique_characters(password) > 2.5, "Mix of unique characters", 1),
        (not contains_leet_speak(password), "Avoids leet speak", 1)
    ]

    analysis = []
    total_points = 0

    for condition, description, points in criteria:
        if condition:
            total_points += points
            analysis.append(f'✅ {description} (+{points} point)')
        else:
            analysis.append(f'❌ {description}')

    if total_points >= 7:
        strength = "Strong"
    elif total_points >= 4:
        strength = "Medium"
    else:
        strength = "Weak"

    return render_template('test.html', strength=strength, password=password, analysis=analysis, total=total_points)

@app.route('/crack/pressed', methods=['POST'])
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