# app.py
# python 3.8

# http://kaffeine.herokuapp.com/ - gives my app a caffeine shot every 30 minutes
# https://medium.com/@morgannewman/how-to-keep-your-free-heroku-app-online-forever-4093ef69d7f5

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
                'candidates' : 
                    'idx' : {'name' : 'B', 'party': 'C'},
                    'idx' : {'name' : 'B', 'party': 'C'},
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

with open(list_filename, 'r') as f:
    all_candidates = json.load(f)

'''with open(result_filename, 'w') as f:
    results = {}
    for constituency in all_candidates:
        results[constituency] = {}
        candidates = all_candidates[constituency]['candidates']
        for c in candidates:
            results[constituency][c] = 0
    f.write(json.dumps(results))'''

@app.route('/')
def redirect():
    return render_template('redirect.html', data=poll_data)

@app.route('/huuchin')
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
    if int(mandates) != len(your_votes):
        error_data = {}
        error_data['title'] = poll_data['title']
        error_data['mandates'] = mandates
        return render_template('error.html', data=error_data)

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
    result_data['title'] = poll_data['title']
    result_data['constituency'] = constituency
    result_data['province'] = all_candidates[constituency]['province']
    result_data['votes'] = your_votes

    return render_template('thankyou.html', data=result_data, candidates=all_candidates[constituency]['candidates'])

@app.route('/results')
def show_results():
    # get results
    results = {}    
    with open(result_filename, 'r') as f:
        results = json.load(f)

    # show results
    results_data = {}
    results_data['title'] = poll_data['title']
    results_data['votes'] = results

    return render_template('results.html', data=results_data, candidates=all_candidates)

@app.route('/results_constit')
def show_constituency_results():
    # get a constituency from HTTP request
    constituency = request.args['constituency']
    
    # get all results
    results = {}    
    with open(result_filename, 'r') as f:
        results = json.load(f)

    # get poll results of a given constituency
    results_data = {}
    results_data['title'] = poll_data['title']
    results_data['votes'] = {}
    results_data['votes'][constituency] = results[constituency]

    # get candidates of a given constituency
    constit_data = {}
    constit_data[constituency] = {}
    constit_data[constituency]['province'] = all_candidates[constituency]['province']
    constit_data[constituency]['mandates'] = all_candidates[constituency]['mandates']
    constit_data[constituency]['candidates'] = all_candidates[constituency]['candidates']

    return render_template('results.html', data=results_data, candidates=constit_data)

if __name__ == "__main__":
    app.run(debug=True)
