import requests
import json
import pandas as pd
import random
import os
from flask import Flask, request,render_template
app = Flask(__name__)

#The Jeopardy JSON file at my personal website
#Where you will find other codes and languages
url = "https://richard-perreault.com/Documents/JEOPARDY_QUESTIONS1.json"

response = requests.get(url)
data = json.loads(response.text)

global count
count = len(data)
quiz = pd.DataFrame(data)

# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])

def index():
  errors = []
  results = {}
  if request.method == "POST":
    #if request.form.get("Submit"):
      try:
          wager = request.form['wager']
          quizchoice(wager)
      except:
          errors.append(
              "Unable to get URL. Please make sure it's valid and try again."
          )
  question = Question()
  return render_template('index.html', number=question[0],category=question[1],air_date=question[2],question=question[3],value=question[4],round=question[5],show_number=question[6],answer=question[7])

def Question():
  """Retruns Jeopardy Question and Question to index.html"""
  number = str(rand)
  category=quiz['category'][rand]
  air_date =quiz['air_date'][rand]
  question=quiz['question'][rand]
  value=quiz['value'][rand]
  round=quiz['round'][rand]
  show_number=quiz['show_number'][rand]
  answer=quiz['answer'][rand]
  return number,category,question,air_date,value,round,show_number,answer

    
def quizchoice(wager):
  """Enter in a wager and get a Jeopardy question"""
  
  go=True

  while go:
    global rand
    rand = random.randrange(1,count) 
    value = quiz['value'][rand]
    #removedollar = ''.join([value for i in range(len(value)) if i != 0])
    try:
     removedollar = value
     removedollar = removedollar.replace('$', '')
     removecomma = removedollar.replace(',', '')
    except:
       removecomma=0
    
    try:
      #This will check to see if the number is
      #an increment of 100
      wager1 = int(wager)/10
      if str(wager1).find('.0') ==-1:
        quizchoice()
        if go:
         return  
      #Make sure it is between 100 and 10000   
      if int(wager) < 100.0 or int(wager) > 10000.0:
        return render_template('index.html')
        if go:
         return 
      if int(wager) == int(removecomma):
        go=False
      else:
        continue
    except:
      #Make sure there is no ValueError so it is just
      #numbers, and if not ask again
      return render_template('index.html')
      if go:
       return

if __name__ == "__main__":
    app.run(host='0.0.0.0')

Question()