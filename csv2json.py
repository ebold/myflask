#!/usr/bin/env python
# python 3.8

import json, re

'''
    all_candidates
    {
        'number' :
                'province' : 'A',
                'mandates' : '3',
                'candidates' : [ {'idx' : i, 'name' : 'B', 'party': 'C'}, {...}, ...],
        ...
                
    }
'''

csv_file = 'list.csv'
out_file = 'list.json'
all_candidates = {}

# read a file with candidate list line by line
with open(csv_file, 'r') as f:
    lines = f.readlines()

    cand_idx = 0    # candidate index
    const_idx = ''  # constituency index
    province = ''   # province name
    mandates = ''   # number of mandates in a constituency

    # parse each line
    for line in lines[1:]:

        line_elements = line.split(',')

        cand_name = line_elements[-2]
        cand_party = line_elements[-1].rstrip('\n')

        # a line contains constituency, province, mandates and also candidate name and party
        if line_elements[0] != '':

            # 2 types of province name: simple and complex within double quotes
            elements = []
            if line_elements[0].startswith('"'):

                province = re.match("(\".+\")", line).group(1)
                elements = line[len(province):].split(',')
            else:
                province = line_elements[0].strip()
                elements = line_elements

            const_idx = elements[1].split('-')[0].strip() # 26-р тойрог
            mandates = elements[2].split(' ')[0].strip() # 3 мандат
            
            print (const_idx, province, mandates)
            cand_idx += 1
            candidates = []
            candidates.append({'idx': cand_idx, 'name': cand_name, 'party': cand_party})

            all_candidates[const_idx] = {}
            all_candidates[const_idx]['province'] = province
            all_candidates[const_idx]['mandates'] = mandates
            all_candidates[const_idx]['candidates'] = candidates

        # a line contains only candidate name and party
        else:
            cand_idx += 1
            all_candidates[const_idx]['candidates'].append({'idx': cand_idx, 'name': cand_name, 'party': cand_party})


    print(all_candidates)

with open(out_file,'w') as f:    
    f.write(json.dumps(all_candidates, sort_keys=True, indent=4))
