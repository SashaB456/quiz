import socket
import sqlite3
from flask import Flask, redirect, url_for, request, render_template
from random import randint
import db
app=Flask(__name__, template_folder='templates')
db_name = "quiz.sqlite"
conn = None
cursor = None
score = 0
def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
def close():
    cursor.close()
    conn.close()
#def show_table(table):
#    open()
#    cursor.execute("SELECT * FROM " + table)
#    data = cursor.fetchall()
#    close()
#    return data
#def build_links():
#    open()
#    sql = "INSERT INTO quiz_content(quiz_id, question_id) VALUES (?, ?)"
#    answer = input("(y/n)")
#    while answer != "n":
#        quiz_id = int(input(""))
#        question_id = int(input(""))
#        cursor.execute(sql, [quiz_id, question_id])
#        conn.commit()
#       answer = input("(y/n)")
#    close()
#if __name__ == "__main__":
#    print(show_table("quiz"))
#    print(show_table("question"))
#    build_links()
quiz_id = 0
question_id = 0
def get_questions(quiz_id):
    open()
    SQL = ''' 
    SELECT question.question, 
    question.answer, 
    question.wrong1, 
    question.wrong2, 
    question.wrong3, 
    quiz.name 
    FROM question, quiz, quiz_content 
    WHERE question.id == quiz_content.question_id 
    AND quiz.id == quiz_content.quiz_id 
    AND quiz_content.quiz_id == ?;
    '''
    cursor.execute(SQL, [quiz_id])
    data = cursor.fetchall()
    close()
    return data
def get_quizes():
    open()
    sql = '''
    SELECT * FROM quiz ORDER BY id
    '''
    cursor.execute(sql)
    data = cursor.fetchall()
    close()
    return data


def index():
    global quiz_id, question_id, score
    #quiz_id = randint(1, 3)
    #print(quiz_id)
    if request.method == "GET":
        question_id = 0
        score = 0
        return render_template("index.html", questions=get_quizes())
    elif request.method == "POST":
        quiz_id = request.form.get("quiz")
        return redirect(url_for("test"))
def test():
    global question_id, score
    try:
        questions = db.get_questions(quiz_id)[question_id]
    except IndexError:
        return redirect(url_for("result"))




    if request.method == "GET":
        return render_template("test.html", question=questions)



    if request.method == "POST":
        question_id += 1
        user_answer = request.form.get("answer")
        if user_answer == questions[1]:
            score += 1
            text="Yes"
        else:
            score -= 1
            text="No"
        return render_template("test.html", text_result=text)
def result():
    global score
    return render_template("result.html", test_score=score)
app.add_url_rule("/", "index", index, methods=["GET", "POST"])
app.add_url_rule("/test", "test", test, methods=["GET", "POST"])
app.add_url_rule("/result", "result", result)
#app.run(debug=True, host="192.168.0.49", port=5000)
local_ip = socket.gethostbyname(socket.gethostname())
app.run(debug=True, host=local_ip, port=5000)