#!/usr/bin/env python 
# -*- coding: utf-8 -*-

################################################################################
                        ##JSON Parse##
"""Parses Galaxy Workflow file for BCO creation"""
################################################################################


import json, sys

with open(sys.argv[1]) as file:
    data = json.load(file)
tool = {}
for i in range(len(data['steps'].keys())):
    tool[i] = {}
    if data['steps'][str(i)]['tool_id'] == None: continue
    print data['steps'][str(i)]['id']
    tool[i]['step_number'] = data['steps'][str(i)]['id']
    print data['steps'][str(i)]['name']
    tool[i]['name'] = data['steps'][str(i)]['name']
    print data['steps'][str(i)]['tool_version']
    tool[i]['tool_version'] = data['steps'][str(i)]['tool_version']
    print data['steps'][str(i)]['tool_id']
    tool[i]['tool_id'] = data['steps'][str(i)]['tool_id']
    tool[i]['input_list'] = []
    for step in data['steps'][str(i)]['inputs']:
        print step['name'], step['description']
        a = {'name': step['name'], 'description': step['description']}
        tool[i]['input_list'].append(a)
    print ''
    tool[i]['output_list'] = []
    for step in data['steps'][str(i)]['outputs']:
        print step['name'], step['type']
        a = {'name': str(step['name']+'.'+step['type']), 'type': step['type']}
#        tool[i]['output_list']['address'] = 
        tool[i]['output_list'].append(a)
    print '\n'
json_data = json.dumps(tool)

for i in tool: 
    print json.dumps(tool[i])

print type(tool.keys())

with open(sys.argv[2], 'w') as file:
    file.write('[')
    for i in tool.keys(): 
        file.write(json.dumps(tool[i], sort_keys=True, indent=4))
        if i == tool.keys()[-1]: continue
        else: file.write(',')
    file.write(']')

