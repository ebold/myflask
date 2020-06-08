# app.py
# python 3.8

from flask import Flask, render_template, request
import os, json
app = Flask(__name__)
 
poll_data = {
   'greeting' : '"Сонгууль 2020" санал асуулга',
   'question' : 'Та сонголтоо хийнэ үү?',
   'fields'   : ['С.Баяр', 'Х.Номтойбаяр', 'Н.Энхбаяр', 'Б.Эрдэнэбаяр', 'үгүй']
}

result_filename = 'result.txt'
list_filename = 'list.json'
all_candidates = {}

with open(list_filename, 'r') as f:
    all_candidates = json.load(f)

@app.route('/')
def root():
        
    constituencies = []
    for i in all_candidates:
        c = {'number': i, 'province': all_candidates[i]['province']}
        constituencies.append(c)

    poll_data['constituencies'] = constituencies

    return render_template('hello.html', data=poll_data)

@app.route('/hello')
def hello():
    constituency = request.args.get('constituency')

    poll_data['candidates'] = all_candidates[constituency]['candidates']
    poll_data['mandates'] = all_candidates[constituency]['mandates']
    poll_data['province'] = all_candidates[constituency]['province']
    poll_data['constituency'] = constituency

    return render_template('poll.html', data=poll_data)

@app.route('/poll')
def poll():
    vote = request.args.get('field')

    out = open(result_filename, 'a')
    out.write( vote + '\n' )
    out.close()

    return render_template('thankyou.html', data=poll_data)

@app.route('/results')
def show_results():
    votes = {}
    for f in poll_data['fields']:
        votes[f] = 0

    f  = open(result_filename, 'r')
    for line in f:
        vote = line.rstrip("\n")
        votes[vote] += 1

    return render_template('results.html', data=poll_data, votes=votes)

if __name__ == "__main__":
    app.run(debug=True)
