import os
import random
import bcrypt
import data_manager
import string


def mark_search_word(search_word, string):
    marked_string = string.replace(search_word, f'<mark>{search_word}</mark>')
    return marked_string


def delete_image(image_file):
    os.remove(os.path.join(os.environ.get('IMAGE_PATH'), image_file['image']))


def generate_random_secret_key():
    secret_key = random.choices(string.ascii_lowercase, k=4)
    secret_key.extend(random.choices(string.ascii_uppercase, k=4))
    secret_key.extend(random.choices(string.digits, k=4))
    secret_key.extend(random.choices(string.punctuation, k=4))
    random.shuffle(secret_key)
    return secret_key


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))


def verify_registration_details(user_details):
    username, email, email_check, password, password_check = user_details.values()
    user = data_manager.get_user_by_detail((username, email))
    if email == email_check and password == password_check:
        if user is None:
            password = hash_password(password)
            return True, (username, email, password), 'Signed up successfully!'
        elif username == user['username'] or email == user['email']:
            return False, None, 'Email or username already in use. Please, try again!'
    else:
        return False, None, 'Email or password do not match. PLease, try again!'


def verify_log_in_details(log_in_form):
    username, email, password = log_in_form.values()
    user = data_manager.get_user_by_detail((username, email))
    if user is not None and verify_password(password, user['password']):
        return True, user['username'], 'Logged in successfully!'
    else:
        return False, None, 'Email or password do not match!'
