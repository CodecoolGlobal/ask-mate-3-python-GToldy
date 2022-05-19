from flask import Flask, redirect, render_template, request, url_for, flash, session, escape, request

import data_manager
import os
import time
from datetime import datetime

import util
from util import mark_search_word

app = Flask(__name__)
app.secret_key = util.generate_random_secret_key()


@app.route('/')
def latest_5_questions():

    question = data_manager.get_questions('submission_time', 'True')
    question = question[:5]

    return render_template('top-5-questions.html', questions=question)


@app.route('/list')
def list_questions():
    if request.args:
        question = data_manager.get_questions(request.args['order_by'], request.args['order_direction'])
        return render_template('list.html', questions=question, order=request.args)
    question = data_manager.get_questions('submission_time', True)
    return render_template('list.html', questions=question, order=None)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def get_question_page(question_id):
    question_tags = data_manager.get_tag_by_question_id(question_id)
    comments = data_manager.get_comments()
    questions = data_manager.get_questions(question_id=question_id)[0]
    answers = data_manager.get_answers(question_id=question_id)

    answer_owner = False

    if 'username' in session and questions['user_id'] is not None:

        user_name = data_manager.get_user_name_by_user_id(questions['user_id'])

        if user_name is not None and escape(session['username']) == user_name['username']:

            answer_owner = True

    if request.method == 'POST':
        data_manager.delete_question_by_id(question_id)
        return redirect(url_for('list_questions'))

    return render_template('question.html', question=questions, answers=answers, comments=comments,
            tag_list=question_tags, answer_owner=answer_owner)


@app.route('/add-question', methods=['GET', 'POST'])
def add_new_question():
    user_id = None

    if 'username' in session:
        user_id = data_manager.get_user_id_by_user_name(session['username'])


    if request.method == 'POST':
        image = request.files['image']
        image_file = f'{time.time()}_{image.filename}'
        if image.filename != '':
            image.save(os.path.join(os.environ.get('IMAGE_PATH'), image_file))
            data_manager.add_new_question(request.form, user_id['user_id'], image_file)
        else:
            data_manager.add_new_question(request.form, user_id['user_id'])
        return redirect('list')
    return render_template('add-question.html', question=None)


@app.route('/question/<question_id>/add-answer', methods=['GET', 'POST'])
def add_new_answer(question_id):
    user_id = None

    if 'username' in session:
        user_id = data_manager.get_user_id_by_user_name(escape(session['username']))

    question = data_manager.get_question_by_id(question_id)
    if request.method == 'POST':
        image = request.files['image']
        image_file = f'{time.time()}_{image.filename}'
        if image.filename != '':
            image.save(os.path.join(os.environ.get('IMAGE_PATH'), image_file))
            data_manager.add_new_answer(request.form, question_id, user_id, image_file)
        else:
            data_manager.add_new_answer(request.form, question_id, user_id)
        return redirect(url_for('get_question_page', question_id=question_id))
    return render_template('add-answer.html', question=question, answer=None)


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def update_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    if request.method == 'POST':
        image = request.files['image']
        image_file = f'{time.time()}_{image.filename}'
        if image.filename != '':
            image.save(os.path.join(os.environ.get('IMAGE_PATH'), image_file))
            data_manager.update_question_by_id(request.form, question_id, image_file)
        else:
            data_manager.update_question_by_id(request.form, question_id)
        return redirect(url_for('list_questions'))
    return render_template('add-question.html', question=question)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer = data_manager.get_answers_by_id(answer_id)
    question_id = answer['question_id']

    if request.method == 'POST':
        if 'accepted_state' in request.form:
            data_manager.update_answer_acception_by_id(answer_id, request.form['accepted_state'])
            if request.form['accepted_state'] == 'True':
                user_data = data_manager.get_users_rep_num_for_a(answer_id, )
                rep_num = user_data['reputation_number']
                user_id = user_data['user_id']
                rep_num += 15
                data_manager.update_users_rep_num(rep_num, user_id)
            else:
                user_data = data_manager.get_users_rep_num_for_a(answer_id, )
                rep_num = user_data['reputation_number']
                user_id = user_data['user_id']
                rep_num -= 15
                data_manager.update_users_rep_num(rep_num, user_id)

            return redirect(url_for('get_question_page', question_id=question_id))
        image = request.files['image']
        image_file = f'{time.time()}_{image.filename}'
        if image.filename != '':
            image.save(os.path.join(os.environ.get('IMAGE_PATH'), image_file))
            data_manager.update_answers_by_id(request.form, answer_id, image_file)
        else:
            data_manager.update_answers_by_id(request.form, answer_id)
        return redirect(url_for('get_question_page', question_id=question_id))
    return render_template('add-answer.html', answer=answer)


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id):
    question_id = data_manager.get_question_id_by_answer_id(answer_id)
    data_manager.delete_answer(answer_id)
    return redirect(url_for('get_question_page', question_id=question_id))


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def new_comment_to_question(question_id):
    where = "question"

    user_id = None

    if 'username' in session:
        user_id = data_manager.get_user_id_by_user_name(escape(session['username']))

    if request.method == 'POST':
        data_manager.add_new_comment_to_question(request.form, question_id, user_id)
        return redirect(url_for('get_question_page', question_id=question_id))

    return render_template('new-comment.html', question_id=question_id, where=where)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def new_comment_to_answer(answer_id):
    where = "answer"

    user_id = None

    if 'username' in session:
        user_id = data_manager.get_user_id_by_user_name(escape(session['username']))

    q_id = data_manager.get_question_id_by_answer_id(answer_id)
    if request.method == 'POST':
        data_manager.add_new_comment_to_answer(request.form, answer_id, user_id)

        return redirect(url_for('get_question_page', question_id=q_id))

    return render_template('new-comment.html', comment=None, answer_id=answer_id, where=where)


@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    where = "comment"

    answer_id = data_manager.get_answer_id_by_comment_id(comment_id)
    if answer_id is None:
        question_id = data_manager.get_question_id_by_comment_id(comment_id)
    else:
        question_id = data_manager.get_question_id_by_answer_id(answer_id)

    comment = data_manager.get_comment_by_id(comment_id)
    comment = comment[0]

    if request.method == 'POST':
        data_manager.update_comment(request.form, comment_id)

        return redirect(url_for('get_question_page', question_id=question_id))

    return render_template('new-comment.html', comment_id=comment_id, comment=comment, where=where)


@app.route('/search')
def search():
    search_word = request.args.get('q')
    question_results = data_manager.search_in_questions(f'%{search_word}%')
    marked_titles = []
    for questions in question_results:
        marked_title = mark_search_word(search_word, questions['title'])
        marked_titles.append([questions['id'], marked_title])
    answer_results = data_manager.search_in_answers(f'%{search_word}%')
    marked_answer_questions = []
    for answer in answer_results:
        marked_message = mark_search_word(search_word, answer['message'])
        question = data_manager.get_question_by_id(answer['question_id'])
        marked_answer_questions.append([question['id'], question['title'], marked_message])
    return render_template('search.html', questions=marked_titles, answers_match=marked_answer_questions)


@app.route('/comments/<comment_id>/delete', methods=['GET', 'POST'])
def delete_comment(comment_id):

    answer_id = data_manager.get_answer_id_by_comment_id(comment_id)
    if answer_id is None:
        question_id = data_manager.get_question_id_by_comment_id(comment_id)
    else:
        question_id = data_manager.get_question_id_by_answer_id(answer_id)

    if request.method == 'POST':
        if "yes-choice" in request.form:
            data_manager.delete_comment_by_id(comment_id)
            return redirect(url_for('get_question_page', question_id=question_id))
        elif "no-choice" in request.form:
            return redirect(url_for('get_question_page', question_id=question_id))

    return render_template('delete.html', comment_id=comment_id)


@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def add_new_tag(question_id):
    all_tag = data_manager.get_all_tags()
    if request.method == 'POST':
        tag = request.form['choose-tag']
        new_tag = request.form['new-tag']
        if tag != "":
            data_manager.new_question_tag(tag, question_id)
        elif new_tag:
            tag_id = data_manager.add_new_tag(new_tag)
            data_manager.new_question_tag(tag_id['id'], question_id)
        return redirect(url_for('get_question_page', question_id=question_id))
    return render_template('new-tag.html', tag_list=all_tag, question_id=question_id)


@app.route('/question/<question_id>/tag/<tag_id>/delete')
def delete_tag(question_id, tag_id):
    data_manager.delete_tag_from_question_tags(question_id, tag_id)
    return redirect(url_for('get_question_page', question_id=question_id))


@app.route('/users')
def users_list():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def user_page(user_id):
    user_data = data_manager.get_user_relations(user_id)
    questions = data_manager.get_questions_for_user_id(user_id)
    answers = data_manager.get_answers_for_user_id(user_id)
    comments = data_manager.get_comments_for_user_id(user_id)

    return render_template('user.html', user_data=user_data, questions=questions, answers=answers,
                           comments=comments)


@app.route('/registration', methods=['GET', 'POST'])
def user_registration():
    if request.method == 'POST':
        is_verified, user, flash_massage = util.verify_registration_details(request.form)
        if is_verified:
            username, email, password = user
            data_manager.add_new_user(username, email, password)
            flash(flash_massage, 'info')
            return redirect(url_for('list_questions'))
        else:
            flash(flash_massage, 'error')
            return redirect(url_for('user_registration'))
    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def user_log_in():
    if request.method == 'POST':
        is_verified, username, flash_message = util.verify_log_in_details(request.form)
        if is_verified:
            session['username'] = username
            flash(flash_message, 'info')
            return redirect(url_for('list_questions'))
        else:
            flash(flash_message, 'error')
            return redirect(url_for('user_log_in'))
    return render_template('login.html')


@app.route('/logout')
def user_log_out():
    session.pop('username', None)
    return redirect(url_for('list_questions'))


@app.route('/tags', methods=['GET', 'POST'])
def tags_page():
    tags = data_manager.get_all_tags_with_num()
    return render_template('tags.html', tags=tags)

  
@app.route('/question/<question_id>/vote-up')
def question_vote_up(question_id):
    vote_num = data_manager.get_question_vote_num(question_id)['vote_number']
    vote_num += 1
    data_manager.update_question_vote_num(question_id, vote_num)
    user_data = data_manager.get_users_rep_num_for_q(question_id, )
    rep_num = user_data['reputation_number']
    user_id = user_data['user_id']
    rep_num += 5
    data_manager.update_users_rep_num(rep_num, user_id)
    return redirect(url_for('get_question_page', question_id=question_id))


@app.route('/question/<question_id>/vote-down')
def question_vote_down(question_id):
    vote_num = data_manager.get_question_vote_num(question_id)['vote_number']
    vote_num -= 1
    data_manager.update_question_vote_num(question_id, vote_num)
    user_data = data_manager.get_users_rep_num_for_q(question_id, )
    rep_num = user_data['reputation_number']
    user_id = user_data['user_id']
    rep_num -= 2
    data_manager.update_users_rep_num(rep_num, user_id)
    return redirect(url_for('get_question_page', question_id=question_id))


@app.route('/answer/<answer_id>/vote-up')
def answer_vote_up(answer_id):
    vote_num = data_manager.get_answer_vote_num(answer_id)['vote_number']
    vote_num += 1
    data_manager.update_answer_vote_num(answer_id, vote_num)
    question_id = data_manager.get_question_id_by_answer_id(answer_id)
    user_data = data_manager.get_users_rep_num_for_a(answer_id, )
    rep_num = user_data['reputation_number']
    user_id = user_data['user_id']
    rep_num += 10
    data_manager.update_users_rep_num(rep_num, user_id)
    return redirect(url_for('get_question_page', question_id=question_id))


@app.route('/answer/<answer_id>/vote-down')
def answer_vote_down(answer_id):
    vote_num = data_manager.get_answer_vote_num(answer_id)['vote_number']
    vote_num -= 1
    data_manager.update_answer_vote_num(answer_id, vote_num)
    question_id = data_manager.get_question_id_by_answer_id(answer_id)
    user_data = data_manager.get_users_rep_num_for_a(answer_id, )
    rep_num = user_data['reputation_number']
    user_id = user_data['user_id']
    rep_num -= 2
    data_manager.update_users_rep_num(rep_num, user_id)
    return redirect(url_for('get_question_page', question_id=question_id))


if __name__ == "__main__":
    app.run(
        port=5000,
        debug=True
    )
