# app.py
from flask import Flask, render_template, request
import os
app = Flask(__name__)
 
poll_data = {
   'question' : 'Та сонголтоо хийнэ үү?',
   'fields'   : ['С.Баяр', 'Х.Номтойбаяр', 'Н.Энхбаяр', 'Б.Эрдэнэбаяр', 'үгүй']
}
filename = 'data.txt'

@app.route('/')
def root():
    return render_template('poll.html', data=poll_data)

@app.route('/poll')
def poll():
    vote = request.args.get('field')

    out = open(filename, 'a')
    out.write( vote + '\n' )
    out.close()

    return render_template('thankyou.html', data=poll_data)

if __name__ == "__main__":
    app.run(debug=True)
