import os

def mark_search_word(search_word, string):
    marked_string = string.replace(search_word, f'<mark>{search_word}</mark>')
    return marked_string


def delete_image(image_file):
    os.remove(os.path.join(os.environ.get('IMAGE_PATH'), image_file['image']))
