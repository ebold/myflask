# app.py
# python 3.8

from flask import Flask, render_template, request
import os, json
app = Flask(__name__)
 
poll_data = {
   'title' : '"Сонгууль 2020" санал асуулга',
   'question' : 'Та сонголтоо хийнэ үү?',
   'fields'   : ['С.Баяр', 'Х.Номтойбаяр', 'Н.Энхбаяр', 'Б.Эрдэнэбаяр', 'үгүй']
}

result_filename = 'result.json'
list_filename = 'list.json'
all_candidates = {}

'''
    list.json
    {
        'number' :
                'province' : 'A',
                'mandates' : '3',
                'candidates' : [ {'idx' : 'i', 'name' : 'B', 'party': 'C'}, {...}, ...],
        ...
                
    }
'''

'''
    result.json
    {
        'number' :
                'idx' : votes,
                'idx' : votes,
        ...
                
    }
'''

with open(result_filename, 'w') as f:
    f.write(json.dumps(all_candidates))

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

    # evaluate request
    your_votes = {}
    for k in request.args.keys():
        if 'field' in k:
            your_votes[request.args[k]] = 1

    mandates = request.args.get('mandates')
    '''if request.args.get('mandates') != len(your_votes)
        return render_template('revote.html')'''

    # get previous result
    result = {}    
    with open(result_filename, 'r') as f:
        result = json.load(f)

    total_votes = {}
    constituency = request.args.get('constituency')
    if constituency in result:
        total_votes = result[constituency]
        for c in your_votes:
            if c in total_votes:
                total_votes[c] = total_votes[c] + your_votes[c]
            else:
                total_votes[c] = your_votes[c]
    else:
        for c in your_votes:
            total_votes[c] = your_votes[c]

    # update result
    result[constituency] = total_votes

    with open(result_filename, 'w') as f:
        f.write(json.dumps(result))

    # show result
    result_data = {}
    result_data['votes'] = []

    candidates = all_candidates[constituency]['candidates']
    for c in candidates:
        if c['idx'] in your_votes:
            result_data['votes'].append({'idx': c['idx'], 'name': c['name'], 'party': c['party']})

    result_data['title'] = poll_data['title']
    result_data['constituency'] = constituency
    result_data['province'] = all_candidates[constituency]['province']

    return render_template('thankyou.html', data=result_data)

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
