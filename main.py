import requests
import json
import random
import pandas as pd
from flask import Flask, request, render_template
from flask import escape

app = Flask('app')

#The Jeopardy JSON file at my personal website
#Where you will find other codes and languages
url = "https://richard-perreault.com/Documents/JEOPARDY_QUESTIONS1.json"

response = requests.get(url)
data = json.loads(response.text)

global count
global rand
count = len(data)
rand = random.randrange(0, count)
quiz = pd.DataFrame(data)


# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods=["GET", "POST"])
def index():
    errors = []
    if request.method == "POST":
        #if request.form.get("Submit"):
        try:
            wager = request.form['wager']
            quizchoice(wager)
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
    question_and_answer = Question_And_Answer()
    #question = str(escape(question_and_answer[3]))
    question = str(question_and_answer[3])
    return render_template('index.html',
                           number=question_and_answer[0],
                           category=question_and_answer[1],
                           air_date=question_and_answer[2],
                           question=question,
                           value=question_and_answer[4],
                           round=question_and_answer[5],
                           show_number=question_and_answer[6],
                           answer=question_and_answer[7])
    #return render_template('index.html')


def Question_And_Answer():
    """Returns Jeopardy Question and Answer to index.html"""
    number = str(rand)
    category = quiz['category'][rand]
    air_date = quiz['air_date'][rand]
    question = quiz['question'][rand]
    value = quiz['value'][rand]
    round = quiz['round'][rand]
    show_number = quiz['show_number'][rand]
    answer = quiz['answer'][rand]
    return number, category, air_date, question, value, round, show_number, answer


def quizchoice(wager):
    """Enter in a wager and get a Jeopardy question"""

    go = True

    while go:
        global rand
        rand = random.randrange(0, count)
        value = quiz['value'][rand]
        #removedollar = ''.join([value for i in range(len(value)) if i != 0])
        try:
            removedollar = value
            removedollar = removedollar.replace('$', '')
            removecomma = removedollar.replace(',', '')
        except:
            removecomma = 0

        try:
            #This will check to see if the number is
            #an increment of 100
            while int(wager) % 100 > 0:
                num = int(wager) + 1
                wager = str(num)
            #Make sure it is between 100 and 10000
            if int(wager) < 100.0 or int(wager) > 10000.0:
                return render_template('index.html')
                if go:
                    return
            if int(wager) == int(removecomma):
                go = False
            else:
                continue
        except:
            #Make sure there is no ValueError so it is just
            #numbers, and if not ask again
            return render_template('index.html')
            if go:
                return


app.run(host='0.0.0.0')
