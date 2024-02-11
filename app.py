# app.py
# python 3.8

# Commands used to test this app on the devel host:
# $ cd ~/venv/
# $ . .venv/bin/activate
# $ flask --app app run

from flask import Flask, render_template, request
import os, json
app = Flask(__name__)
 
poll_data = {
   'title' : '"Сонгууль 2020" санал асуулга',
   'question' : 'Та сонголтоо хийнэ үү?',
   'fields'   : ['С.Баяр', 'Х.Номтойбаяр', 'Н.Энхбаяр', 'Б.Эрдэнэбаяр', 'үгүй'],
   'select_constit': 'Энд заасан тойргийн дүнг сонирхох: ',
   'select_all': 'Эсвэл нийт тойргийн дүнг сонирхох -> ',
   'home': 'Үндсэн хуудас уруу буцах'
}

# election 2020
result_filename = 'result.json'
list_filename = 'list.json'
result_2020_filename = 'result_2020.json'
all_candidates = {}

# tsagaan sar
tsagaan_sar_filename = 'tsagaan_sar.json'
wheel_filename = 'wheel.json'

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
def home():
    return render_template('index.html')

@app.route('/election2020')
def election2020():
        
    constituencies = []
    for i in all_candidates:
        c = {'number': i, 'province': all_candidates[i]['province']}
        constituencies.append(c)

    poll_data['constituencies'] = constituencies

    return render_template('election2020.html', data=poll_data)

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
    result_data['votes'] = []

    candidates = all_candidates[constituency]['candidates']
    for c in candidates:
        if c in your_votes:
            result_data['votes'].append({'idx': c, 'name': candidates[c]['name'], 'party': candidates[c]['party']})

    result_data['title'] = poll_data['title']
    result_data['constituency'] = constituency
    result_data['province'] = all_candidates[constituency]['province']

    return render_template('thankyou.html', data=result_data)

@app.route('/poll_result')
def show_poll_result():
    # get results
    results = {}    
    with open(result_filename, 'r') as f:
        results = json.load(f)

    # show results
    results_data = {}
    results_data['title'] = poll_data['title']
    results_data['votes'] = results

    return render_template('results.html', data=results_data, candidates=all_candidates)

@app.route('/poll_result_by_constit')
def show_poll_result_by_constituency():
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

@app.route('/result_2020')
def show_result_2020():
    # read votes from an external file
    results = {}
    with open(result_2020_filename, 'r') as f:
       results = json.load(f)

    # prepare data
    results_data = {}
    results_data['title'] = '2020 results'
    results_data['votes'] = results

    # render HTML
    return render_template('result_2020.html', data=results_data, candidates=all_candidates)

@app.route('/result_2020_by_constit')
def show_result_2020_by_constituency():
    # get a constituency from HTTP request
    constituency = request.args['constituency']

    # get all results
    results = {}
    with open(result_2020_filename, 'r') as f:
        results = json.load(f)

    # get election result of a chosen constituency
    results_data = {}
    results_data['title'] = poll_data['title']
    results_data['votes'] = {}
    results_data['votes'][constituency] = results[constituency]

    # get candidates of a chosen constituency
    constit_data = {}
    constit_data[constituency] = {}
    constit_data[constituency]['province'] = all_candidates[constituency]['province']
    constit_data[constituency]['mandates'] = all_candidates[constituency]['mandates']
    constit_data[constituency]['candidates'] = all_candidates[constituency]['candidates']

    return render_template('result_2020.html', data=results_data, candidates=constit_data)

@app.route('/tsagaan_sar')
def tsagaan_sar():

    with open(tsagaan_sar_filename, 'r') as f:
        data = json.load(f)

    route = {}
    route["overview_text"] = data["overview_text"]

    return render_template('tsagaan_sar.html', data=data, route=route)

@app.route('/find_seat')
def find_seat():

    # age (must be non-zero) - hii nasiig tootsno
    # gender - eregtei bol 'gal' -s ehlen nar zov toiruulan toolno,
    #        - emegtei bol 'us' -s ehlen nar buruu toiruulan toolj suudliig olno

    age = int(request.args['age'])
    gender = request.args['gender']

    # get all seats
    with open(wheel_filename, 'r') as f:
        seats = json.load(f)
        n_seats = seats["n_seats"]
        idx_water = n_seats / 2

    # calculate seat index
    idx = (age - 1) % n_seats

    # handling for female
    if (gender == "female"):
        idx = (idx + idx_water) % n_seats - idx
        idx = int(idx)

    seat = seats["seats"][str(idx)]    # user's seat info
    directions = seats["directions"]

    # TODO: consider 'black_dog_mouth' for the route
    seat["outgoing"] = seat["way"]["0"]

    # get text for HTML
    with open(tsagaan_sar_filename, 'r') as f:
        data = json.load(f)

    # workaround to display user info and route procedure separetely in HTML (as paragraphs)
    paragraphs =  "Суудал: " + seat["desc"] + ", нас: " + str(age) + ", хүйс: " + data[gender] # user info
    paragraphs += '\n'
    paragraphs += make_route(seat, directions) # route procedure

    paragraphs = paragraphs.split('\n')  # make array by splitting

    # build a final route text
    route = {}
    route["paragraphs"] = paragraphs

    return render_template('tsagaan_sar.html', data=data, route=route)

def make_route(seat, directions):
    # compose a route

    route_text = "Мөр гаргах: Шинийн нэгний өглөө " + directions[seat["outgoing"]] + " зүгт гарч, "
    route_text += "хөллийн засал болгон сууж буй хөллийн махбодын дайсан болох " + seat["opposite"] + "-д "
    route_text += "'" + seat["mantra"] + "' тарнийг уриж, " + directions[seat["way"]["4"]] + " зүгт цацаж, "
    route_text += directions[seat["way"]["1"]] + " зүгээс ирнэ."

    return route_text

if __name__ == "__main__":
    app.run(debug=True)
