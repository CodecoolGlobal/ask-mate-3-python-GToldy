import database_common
import datetime
import util


@database_common.connection_handler
def add_new_question(cursor, question_details, user_id, image_file=''):
    submission_time = datetime.datetime.now()

    add = """
        INSERT INTO question
        VALUES(DEFAULT, %(time)s, %(view_n)s, %(vote_n)s, %(title)s, %(message)s, %(image)s, %(user_id)s )
        """
    cursor.execute(add, {'time': submission_time, 'view_n': 0, 'vote_n': 0, 'title': question_details['title'],
                         'message': question_details['message'], 'image': image_file, 'user_id': user_id})


@database_common.connection_handler
def get_questions(cursor, order_by=None, order_direction=True, question_id=None):
    if question_id is not None:
        query = """
            SELECT *
            FROM question
            WHERE id = %(question_id)s
            """
        cursor.execute(query, {'question_id': question_id})
    else:
        query = """
            SELECT *
            FROM question
            """
        cursor.execute(query)

    data = cursor.fetchall()

    if order_by is not None:
        order_direction = True if order_direction == 'True' else False
        data = sorted(data, key=lambda x: x[order_by], reverse=order_direction)

    return data


@database_common.connection_handler
def get_answers(cursor, question_id=None):
    if question_id is not None:
        query = """
            SELECT *
            FROM answer
            WHERE question_id = %(question_id)s
            """
        cursor.execute(query, {'question_id': question_id})
    else:
        query = """
            SELECT *
            FROM answer
            """
        cursor.execute(query)

    data = cursor.fetchall()

    return data


@database_common.connection_handler
def update_question_by_id(cursor, question_details, question_id, image_file=''):
    update = """
        UPDATE question
        SET title = %(title)s, message = %(message)s, image = %(image)s 
        WHERE id = %(id_code)s
        """
    cursor.execute(update,
                   {'id_code': question_id, 'title': question_details['title'], 'message': question_details['message'],
                    'image': image_file})


@database_common.connection_handler
def delete_answer_by_question_id(cursor, question_id):
    answer = get_answer_id_by_question_id(question_id)
    print(answer)
    for ans in answer:
        for i in ans.values():
            delete_comment_by_answer_id(i)

    delete = """
        DELETE FROM answer
        WHERE question_id = %(id_code)s
        """
    cursor.execute(delete, {'id_code': question_id})


@database_common.connection_handler
def delete_comment_by_answer_id(cursor, question_id):
    delete = """
        DELETE FROM comment
        WHERE answer_id = %(id_code)s
        """
    cursor.execute(delete, {'id_code': question_id})


@database_common.connection_handler
def delete_comment_by_id(cursor, comment_id):
    delete = """
        DELETE FROM comment
        WHERE id = %(id_code)s
        """
    cursor.execute(delete, {'id_code': comment_id})


@database_common.connection_handler
def delete_comment_by_question_id(cursor, question_id):
    delete = """
        DELETE FROM comment
        WHERE question_id = %(id_code)s
        """
    cursor.execute(delete, {'id_code': question_id})


@database_common.connection_handler
def delete_image_by_question_id(cursor, question_id):
    get_image = """
            SELECT image
            FROM question
            WHERE id = %(question_id)s
            """
    cursor.execute(get_image, {'question_id': question_id})
    image_file = cursor.fetchone()
    if image_file['image'] != '':
        util.delete_image(image_file)


@database_common.connection_handler
def delete_question_by_id(cursor, question_id):
    delete_comment_by_question_id(question_id)
    delete_answer_by_question_id(question_id)
    delete_image_by_question_id(question_id)

    delete = """
        DELETE FROM question
        WHERE id = %(id_code)s
        """
    cursor.execute(delete, {'id_code': question_id})


@database_common.connection_handler
def add_new_answer(cursor, question_details, question_id, user_id, image_file=''):
    submission_time = datetime.datetime.now()

    add = """
        INSERT INTO answer
        VALUES(DEFAULT, %(time)s, %(vote_n)s, %(question_id)s, %(message)s, %(image)s, %(user_id)s )
        """
    cursor.execute(add, {'time': submission_time, 'vote_n': 0, 'question_id': question_id,
                         'message': question_details['message'], 'image': image_file, 'user_id': user_id})


@database_common.connection_handler
def add_new_comment_to_question(cursor, comment, question_id, user_id):
    submission_time = datetime.datetime.now()

    add = """
        INSERT INTO comment
        VALUES(DEFAULT, %(question_id)s, NULL,  %(message)s, %(time)s, %(edited_c)s, %(user_id)s )
        """
    cursor.execute(add, {'question_id': question_id, 'message': comment['comment'],
                         'time': submission_time, 'edited_c': 0, 'user_id': user_id})


@database_common.connection_handler
def add_new_comment_to_answer(cursor, comment, answer_id, user_id):
    submission_time = datetime.datetime.now()

    add = """
        INSERT INTO comment
        VALUES(DEFAULT, NULL, %(answer_id)s,  %(message)s, %(time)s, %(edited_c)s, %(user_id)s )
        """
    cursor.execute(add, {'answer_id': answer_id, 'message': comment['comment'],
                         'time': submission_time, 'edited_c': 0, 'user_id': user_id})


@database_common.connection_handler
def get_answer_id_by_question_id(cursor, question_id):
    query = """
        SELECT id
        FROM answer
        WHERE question_id = %(id_code)s
        """
    cursor.execute(query, {'id_code': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_id_by_comment_id(cursor, comment_id):
    query = """
        SELECT answer_id
        FROM comment
        WHERE id = %(id_code)s
        """
    cursor.execute(query, {'id_code': comment_id})
    answer = cursor.fetchall()

    a_id = 0
    for ans in answer:
        for i in ans.values():
            a_id = i

    return a_id


@database_common.connection_handler
def get_question_id_by_comment_id(cursor, comment_id):
    query = """
        SELECT question_id
        FROM comment
        WHERE id = %(id_code)s
        """
    cursor.execute(query, {'id_code': comment_id})
    answer = cursor.fetchall()

    q_id = 0
    for ans in answer:
        for i in ans.values():
            q_id = i

    return q_id


@database_common.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    query = """
        SELECT question_id
        FROM answer
        WHERE id = %(id_code)s
        """
    cursor.execute(query, {'id_code': answer_id})
    answer = cursor.fetchall()

    q_id = 0
    for ans in answer:
        for i in ans.values():
            q_id = i

    return q_id


@database_common.connection_handler
def get_comments(cursor):
    query = """
        SELECT *
        FROM comment
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_by_id(cursor, comment_id):
    query = """
        SELECT *
        FROM comment
        WHERE id = %(id_code)s
        """
    cursor.execute(query, {'id_code': comment_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_comments_by_question_id(cursor, question_id):
    query = """
        SELECT *
        FROM comment
        WHERE question_id = %(id_code)s
        """
    cursor.execute(query, {'id_code': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_by_id(cursor, answer_id):
    query = ''' SELECT *
            FROM answer
            WHERE id = %(answer_id)s '''
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@database_common.connection_handler
def update_answers_by_id(cursor, answer_detail, answer_id, image_file):
    update = """
            UPDATE answer
            SET  message = %(message)s, image = %(image)s 
            WHERE id = %(answer_id)s
            """
    cursor.execute(update, {'answer_id': answer_id, 'message': answer_detail['message'], 'image': image_file})


@database_common.connection_handler
def get_comment_edited_count_by_id(cursor, comment_id):
    query = """
        SELECT edited_count
        FROM comment
        WHERE id = %(id_code)s
        """
    cursor.execute(query, {'id_code': comment_id})
    num = cursor.fetchall()
    num = num[0]
    number = num['edited_count']

    if number == None:
        number = 0

    return number


@database_common.connection_handler
def update_comment(cursor, comment, comment_id):
    number = get_comment_edited_count_by_id(comment_id) + 1
    submission_time = datetime.datetime.now()

    update = """
        UPDATE comment
        SET message = %(message)s, submission_time = %(time)s, edited_count = %(edited_c)s
        WHERE id = %(c_id)s
        """
    cursor.execute(update, {'message': comment['comment'],
                            'time': submission_time, 'edited_c': number, 'c_id': comment_id})


@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    query = ''' SELECT *
                FROM question
                WHERE id = %(question_id)s '''
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchone()


@database_common.connection_handler
def search_in_questions(cursor, search_word):
    query = ''' SELECT *
                FROM question
                WHERE message LIKE %(search_word)s or title LIKE %(search_word)s'''
    cursor.execute(query, {'search_word': search_word})
    return cursor.fetchall()


@database_common.connection_handler
def search_in_answers(cursor, search_word):
    query = ''' SELECT *
                FROM answer
                WHERE message LIKE %(search_word)s '''
    cursor.execute(query, {'search_word': search_word})
    return cursor.fetchall()


@database_common.connection_handler
def add_new_tag(cursor, tag_name):
    query = '''INSERT
            INTO tag
            VALUES (DEFAULT, %(tag_name)s)'''
    cursor.execute(query, {'tag_name': tag_name})

    result = ''' SELECT id
                FROM tag
                WHERE name=%(tag_name)s'''
    cursor.execute(result, {'tag_name': tag_name})
    return cursor.fetchone()


@database_common.connection_handler
def new_question_tag(cursor, tag_id, question_id):
    query = '''INSERT
            INTO question_tag
            VALUES (%(question_id)s, %(tag_id)s)'''
    cursor.execute(query, {'question_id': question_id, 'tag_id': tag_id})


@database_common.connection_handler
def get_all_tags(cursor):
    query = '''SELECT *
            FROM tag'''
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_all_tags_with_num(cursor):
    query = '''SELECT tag.name, COUNT(question_id) AS q_num
                FROM tag
            LEFT JOIN question_tag qt on tag.id = qt.tag_id
            GROUP BY tag.id
            ORDER BY tag.name'''
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_tag_by_question_id(cursor, question_id):
    query = '''SELECT name, question_id
            FROM tag
            INNER JOIN question_tag on tag.id = question_tag.tag_id
            WHERE question_id=%(question_id)s'''
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def delete_tag_from_question_tags(cursor, question_id, tag_id):
    query = '''DELETE
        FROM question_tag
        WHERE question_tag.question_id=%(question_id)s AND tag_id=%(tag_id)s'''
    cursor.execute(query, {'question_id': question_id, 'tag_id': tag_id})


@database_common.connection_handler
def add_new_user(cursor, username, email, password):
    registration_time = datetime.datetime.now()
    query = "INSERT INTO users " \
            "VALUES (DEFAULT, %(username)s, %(email)s, %(password)s, %(registration_time)s)"
    cursor.execute(query, {'username': username, 'email': email, 'password': password, 'registration_time': registration_time})


@database_common.connection_handler
def get_user_by_detail(cursor, user_login):
    username, email = user_login
    query = "SELECT * FROM users WHERE email = %(email)s OR username = %(username)s"
    cursor.execute(query, {'username': username, 'email': email})
    return cursor.fetchone()

  
@database_common.connection_handler  
def get_user_id_by_user_name(cursor, user_name):
    query = """
        SELECT user_id
        FROM users
        WHERE username = %(user_name)s
        """
    cursor.execute(query, {'user_name': user_name})
    return cursor.fetchall()


@database_common.connection_handler
def get_question_vote_num(cursor, question_id):
    query = '''SELECT vote_number
                FROM question
                WHERE id=%(question_id)s'''
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchone()


@database_common.connection_handler
def get_answer_vote_num(cursor, answer_id):
    query = '''SELECT vote_number
                FROM answer
                WHERE id=%(answer_id)s'''
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@database_common.connection_handler
def update_question_vote_num(cursor, question_id, vote_number):
    query = '''UPDATE question
                SET vote_number=%(vote_number)s
                WHERE id=%(question_id)s'''
    cursor.execute(query, {'vote_number': vote_number, 'question_id': question_id})


@database_common.connection_handler
def update_answer_vote_num(cursor, answer_id, vote_number):
    query = '''UPDATE answer
                SET vote_number=%(vote_number)s
                WHERE id=%(answer_id)s'''
    cursor.execute(query, {'vote_number': vote_number, 'answer_id': answer_id})


@database_common.connection_handler
def get_users_rep_num_for_A(cursor, answer_id):
    query = '''SELECT reputation_number, users.user_id
                FROM users
                LEFT JOIN answer a on users.user_id = a.user_id
                WHERE a.id=%(answer_id)s'''
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@database_common.connection_handler
def get_users_rep_num_for_Q(cursor, question_id):
    query = '''SELECT reputation_number, users.user_id
                FROM users
                LEFT JOIN question q on users.user_id = q.user_id
                WHERE q.id=%(question_id)s'''
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchone()


@database_common.connection_handler
def update_users_rep_num(cursor, reputation_number, user_id):
    query = '''UPDATE users
                SET reputation_number=%(reputation_number)s
                WHERE user_id=%(user_id)s'''
    cursor.execute(query, {'reputation_number': reputation_number, 'user_id': user_id})

