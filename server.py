from flask import Flask, redirect, render_template, request, url_for
import data_manager
import os
import time

from util import mark_search_word

app = Flask(__name__)


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
    question_tag = data_manager.get_tag_by_question_id(question_id)
    comments = data_manager.get_comments()
    questions = data_manager.get_questions(question_id=question_id)[0]
    answers = data_manager.get_answers(question_id=question_id)

    if request.method == 'POST':
        data_manager.delete_question_by_id(question_id)  # Törlésre át kell adni a képet majd.
        return redirect(url_for('list_questions'))

    return render_template('question.html', question=questions, answers=answers, comments=comments, tag_list=question_tag)


@app.route('/add-question', methods=['GET', 'POST'])
def add_new_question():
    if request.method == 'POST':
        image = request.files['image']
        image_file = f'{time.time()}_{image.filename}'
        if image.filename != '':
            image.save(os.path.join(os.environ.get('IMAGE_PATH'), image_file))
            data_manager.add_new_question(request.form, image_file)
        else:
            data_manager.add_new_question(request.form)
        return redirect('list')
    return render_template('add-question.html', question=None)


@app.route('/question/<question_id>/add-answer', methods=['GET', 'POST'])
def add_new_answer(question_id):
    question = data_manager.get_question_by_id(question_id)
    if request.method == 'POST':
        image = request.files['image']
        image_file = f'{time.time()}_{image.filename}'
        if image.filename != '':
            image.save(os.path.join(os.environ.get('IMAGE_PATH'), image_file))
            data_manager.add_new_answer(request.form, question_id, image_file)
        else:
            data_manager.add_new_answer(request.form, question_id)
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
        image = request.files['image']
        image_file = f'{time.time()}_{image.filename}'
        if image.filename != '':
            image.save(os.path.join(os.environ.get('IMAGE_PATH'), image_file))
            data_manager.update_answers_by_id(request.form, answer_id, image_file)
        else:
            data_manager.update_answers_by_id(request.form, answer_id)
        return redirect(url_for('get_question_page', question_id=question_id))
    return render_template('add-answer.html', answer=answer)


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def new_comment_to_question(question_id):
    where = "question"

    if request.method == 'POST':
        data_manager.add_new_comment_to_question(request.form, question_id)
        return redirect(url_for('get_question_page', question_id=question_id))

    return render_template('new-comment.html', question_id=question_id, where=where)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def new_comment_to_answer(answer_id):
    where = "answer"
    q_id = data_manager.get_question_id_by_answer_id(answer_id)
    if request.method == 'POST':
        data_manager.add_new_comment_to_answer(request.form, answer_id)

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


@app.route('/registration', methods=['GET', 'POST'])
def user_registration():
    return render_template('registration.html')


if __name__ == "__main__":
    app.run(
        port=5000,
        debug=True
    )