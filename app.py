# app.py
from flask import Flask, render_template
import os
app = Flask(__name__)
 
poll_data = {
   'question' : 'Сонголтоо хийнэ үү?',
   'fields'   : ['С.Баяр', 'Х.Номтойбаяр', 'Н.Энхбаяр', 'Б.Эрдэнэбаяр', 'сонголт алга']
}
 
@app.route('/')
def root():
    return render_template('poll.html', data=poll_data)
 
if __name__ == "__main__":
    app.run(debug=True)
