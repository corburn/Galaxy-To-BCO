#!/usr/bin/env python 
# -*- coding: utf-8 -*-

################################################################################
                        ##JSON Parse Galaxy History##
"""Parses Galaxy History file for BCO creation"""
################################################################################

import json, sys, argparse, os, glob
bco = {    "bco_id": "-1",    "checksum": "",    "bco_spec_version": "1.3.0",    "provenance_domain": {      "name": "",      "version": "",      "created": "",      "modified": "",      "contributors": [],      "license": ""    },    "usability_domain": [],    "extension_domain": {      "fhir_extension": [],      "scm_extension": {        "scm_repository": "",        "scm_type": "git",        "scm_commit": "",        "scm_path": ""      }    },    "description_domain": {      "keywords": [],      "pipeline_steps": []    },    "execution_domain": {      "script": [],      "script_driver": "",      "software_prerequisites": [],      "external_data_endpoints": [],      "environment_variables": {}    },    "parametric_domain": [      {        "param": "",        "value": "",        "step": ""      }    ],    "io_domain": {      "input_subdomain": [],      "output_subdomain": []    },    "error_domain": {      "empirical_error": {},      "algorithmic_error": {}    }  }
#______________________________________________________________________________#
def create_arg_parser():
    """"Creates and returns the ArgumentParser object."""

    parser = argparse.ArgumentParser(description='Parses Galaxy History file for BCO creation.')

    parser.add_argument('inputDirectory',
                    help='Path to the input Galaxy-History.')

    parser.add_argument('-o', '--output',
                    help='The output that contains the BCO.')

    return parser
#______________________________________________________________________________#
def read_galaxy_history( path ):
    """"""
    
    with open (os.path.join(path, 'history_attrs.txt')) as file:
        history = json.load(file)

    with open (os.path.join(path, 'jobs_attrs.txt')) as file:
        jobs = json.load(file)

    with open (os.path.join(path, 'datasets_attrs.txt')) as file:
        data_attrs = json.load(file)

    with open (os.path.join(path, 'datasets_attrs.txt.provenance')) as file:
        data_provenance = json.load(file)

    return history,jobs, data_attrs, data_provenance

#______________________________________________________________________________#
def parse_top( dic ):
    """Pulls the top level fields from the BCO"""

    top = dic
    
    top['bco_id'] = 'hello foo'
    top['checksum'] = ''
    top['bco_spec_version'] = ''#data['bco_spec_version']
    dic = top

    return dic
#______________________________________________________________________________#
def parse_prov( dic, history ):
    """Reads the Prov dom feilds for a GalaxyBCO"""

    prov = dic['provenance_domain']
    prov['name'] = history['name']
    contributor = {  "orcid": "",  "affiliation": "",  "contribution": [],  "name": "", "email": "" }
    print prov.keys()

    dic['provenance_domain'] = prov

    return dic
#______________________________________________________________________________#
def parse_usability( dic, history ):
    """Uses the Galaxy History annotation feild to populate the useablity domain"""

    dic['usability_domain'] = history['annotation']
    # print dic['usability_domain']
    return dic
#______________________________________________________________________________#
def parse_extension( dic ):
    """"""

#______________________________________________________________________________#
def parse_description( dic ):
    """"""

    des = dic
#______________________________________________________________________________#
def parse_execution( dic ):
    """"""

    exe = dic
#______________________________________________________________________________#
def parse_param( dic1, dic2 ):
    """"""
#______________________________________________________________________________#
def parse_io( dic ):
    """"""

    io = dic
#______________________________________________________________________________#
def parse_err( dic ):
    """"""

    err = dic

#______________________________________________________________________________#
def main( bco ):
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])
    history,jobs, data_attrs, data_provenance = read_galaxy_history(parsed_args.inputDirectory)
    bco = parse_top(bco)
    bco = parse_usability(bco, history)
    bco = parse_prov(bco, history)
    print json.dumps(bco)
# tool = {}
# for i in range(len(data['steps'].keys())):
#     tool[i] = {}
#
#     print data['steps'][str(i)]['id']
#     tool[i]['step_number'] = data['steps'][str(i)]['id']
#     print data['steps'][str(i)]['name']
#     tool[i]['name'] = data['steps'][str(i)]['name']
#     print data['steps'][str(i)]['tool_version']
#     tool[i]['tool_version'] = data['steps'][str(i)]['tool_version']
#     print data['steps'][str(i)]['tool_id']
#     tool[i]['tool_id'] = data['steps'][str(i)]['tool_id']
#     tool[i]['input_list'] = []
#     for step in data['steps'][str(i)]['inputs']:
#         print step['name'], step['description']
#         a = {'name': step['name'], 'description': step['description']}
#         tool[i]['input_list'].append(a)
#     print ''
#     tool[i]['output_list'] = []
#     for step in data['steps'][str(i)]['outputs']:
#         print step['name'], step['type']
#         a = {'name': str(step['name']+'.'+step['type']), 'type': step['type']}
# #        tool[i]['output_list']['address'] =
#         tool[i]['output_list'].append(a)
#     print '\n'
# json_data = json.dumps(tool)
#
# for i in tool:
#     print json.dumps(tool[i])
#
# print type(tool.keys())
#
# with open(sys.argv[2], 'w') as file:
#     file.write('[')
#     for i in tool.keys():
#         file.write(json.dumps(tool[i], sort_keys=True, indent=4))
#         if i == tool.keys()[-1]: continue
#         else: file.write(',')
#     file.write(']')
#
#
#
#______________________________________________________________________________#
if __name__ == "__main__":
    main(bco)