#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################################################
                        ##JSON Parse Galaxy History##
"""
                    Parses Galaxy History files for BCO creation
    For a test use https://github.com/biocompute-objects/Galaxy-To-BCO/tree/dev
    as the test file
"""
################################################################################

import json
import jsonref
import jsonschema
import sys 
import argparse
import os
import glob

#bco = {    "bco_id": "-1",    "checksum": "",    "bco_spec_version": "1.3.0",    "provenance_domain": {      "name": "",      "version": "",      "created": "",      "modified": "",      "contributors": [],      "license": ""    },    "usability_domain": [],    "extension_domain": {      "fhir_extension": [],      "scm_extension": {        "scm_repository": "",        "scm_type": "git",        "scm_commit": "",        "scm_path": ""      }    },    "description_domain": {      "keywords": [],      "pipeline_steps": []    },    "execution_domain": {      "script": [],      "script_driver": "",      "software_prerequisites": [],      "external_data_endpoints": [],      "environment_variables": {}    },    "parametric_domain": [      {        "param": "",        "value": "",        "step": ""      }    ],    "io_domain": {      "input_subdomain": [],      "output_subdomain": []    },    "error_domain": {      "empirical_error": {},      "algorithmic_error": {}    }  }
#______________________________________________________________________________#
def extend_with_default(validator_class):
    """
    Taken from: https://python-jsonschema.readthedocs.io/en/stable/faq/#why-doesn-t-my-schema-s-default-property-set-the-default-on-my-instance
    """

    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])

        for error in validate_properties(
            validator, properties, instance, schema,
        ):
            yield error

    return jsonschema.validators.extend(
        validator_class, {"properties" : set_defaults},
    )
DefaultValidatingDraft7Validator = extend_with_default(jsonschema.Draft7Validator)

#______________________________________________________________________________#
def iterdict(schema):
    """
    Recursively walk through a JSON Schema initializing it with blank defaults.
    TODO: rename function and check if there are issues with how this is modifying the datastructure it is iterating through.
    """

    for k,v in schema.items():
        if isinstance(v, dict):
            if v.get('type') == 'object':
                v.setdefault('default', {})
            elif v.get('type') == 'string':
                v.setdefault('default', '')
            elif v.get('type') == 'array':
                v.setdefault('default', [])
            iterdict(v)

#______________________________________________________________________________#
def create_arg_parser():
    """"Creates and returns the ArgumentParser object. An absolute path for the 
    input directory is required. 
    TODO: The output is path is optional now, and does not work yet
    """

    parser = argparse.ArgumentParser(description='Parses Galaxy History file for BCO creation.')

    parser.add_argument('inputDirectory',
                    help='Path to the input Galaxy-History.')

    parser.add_argument('-o', '--output',
                    help='The output that contains the BCO.')

    parser.add_argument('-s', '--schema', default='file:/Users/hadley/GitHub/BCO_Specification/schemas/biocomputeobject.json',
                    help='The URL that contains the BCO schema.')

    return parser
#______________________________________________________________________________#
def read_galaxy_history( path ):
    """takes an abosolute path argument
    opens files contained in the Galaxy-History *.zip
    returns a JSON of each of the coorisponding files
    """
    
    try: 
        with open (os.path.join(path, 'history_attrs.txt')) as file:
            history = json.load(file)
    except: history = []

    try: 
        with open (os.path.join(path, 'datasets_attrs.txt')) as file:
            data_attrs = json.load(file)
    except: data_attrs = []

    try: 
        with open (os.path.join(path, 'jobs_attrs.txt')) as file:
            jobs = json.load(file)
    except: jobs = []

    try: 
        with open (os.path.join(path, 'implicit_collection_jobs_attrs.txt')) as file:
            implicit = json.load(file)
    except: implicit = []

    try: 
        with open (os.path.join(path, 'collections_attrs.txt')) as file:
            collections = json.load(file)
    except: collections = []

    try: 
        with open (os.path.join(path, 'export_attrs.txt')) as file:
            export_attrs = json.load(file)
    except: export_attrs = []

    try: 
        with open (os.path.join(path, 'libraries_attrs.txt')) as file:
            libraries = json.load(file)
    except: libraries = []

    try: 
        with open (os.path.join(path, 'datasets_attrs.txt.provenance')) as file:
            data_provenance = json.load(file)
    except: data_provenance = []

    workflow = []
    for name in glob.glob(os.path.join(path,'datasets/Galaxy-Workflow-Workflow_constructed_from_history__*')): 
        with open (name) as file:
            workflow = json.load(file)

    return history, data_attrs, jobs, implicit, collections, export_attrs, libraries, data_provenance, workflow

#______________________________________________________________________________#
def load_schema( url ):
    """Load JSON Schema from the repository by using URL or local file using
    absolute path and 'file:' prefix
    Walk through the definitions ensuring they all *a* default
    Use the extended validator to fill in `data` with default values from the 
    schema
    print validation errors with a schema path to make them easier to read/trace
    """

    schema_uri = url

    schema = jsonref.loads(f'{{ "$ref": "{schema_uri}" }}', jsonschema=True)

    iterdict(schema)

    data = {}

    for err in DefaultValidatingDraft7Validator(schema).iter_errors(data): continue
        #print(f'{err.message} in the schema path {err.schema.get("$id") }#{"/".join(err.schema_path)}')
    data['bco_spec_version'] = schema_uri
    # Pretty print `data` showing the assigned default values.
    #print(json.dumps(data, indent=4))

    return data

#______________________________________________________________________________#
def parse_top( dic1, dic2 ):
    """Pulls the top level fields from the BCO
    """

    his = dic2
    top = dic1
    
    top['bco_id'] = his['name']
    top['checksum'] = ''
    #top['bco_spec_version'] = ''#data['bco_spec_version']
    dic = top

    return dic
#______________________________________________________________________________#
def parse_prov( dic, history ):
    """
    Reads the Prov dom feilds for a GalaxyBCO
    """

    prov = dic['provenance_domain']
    prov['name'] = history['name']
    contributor = {  "orcid": "",  "affiliation": "",  "contribution": [],  "name": "", "email": "" }
    #prov['review'] = 
    prov['created'] = history['create_time']
    prov['modified'] = history['update_time']
    prov['created'] = history['create_time']
    dic['provenance_domain'] = prov

    return dic
#______________________________________________________________________________#
def parse_usability( bco, history ):
    """Uses the Galaxy History annotation feild to populate the useablity domain
    """

    bco['usability_domain'] = history['annotation']
    # print dic['usability_domain']
    return bco
#______________________________________________________________________________#
def parse_extension( dic ):
    """
    """

#______________________________________________________________________________#
def parse_description( bco, workflow,  ):
    """ 
    description based on workflow

    """
    
    description_domain = {
            'keywords': [],
            'xref': [],
            'platform': ['Galaxy'],
            'pipeline_steps': []
        }
        
    for i in range(len(workflow['steps'])): 
        if workflow['steps'][str(i)]['tool_id'] == None: 
            pass
        else:
            
            description_domain['pipeline_steps'].append(
                {
                    'step_number': i, 
                    'name': workflow['steps'][str(i)]['name'], 
                    'description': '', 
                    'version': workflow['steps'][str(i)]['tool_version']
                }
            )
                #     'prerequisite': [
                #         {
                #             'name': '',
                #             'uri':{
                #                 'uri':'',
                #                 'access_time':''
                #             }
                #         }
                #     ],
                #     'output_list':[
                #         {
                #             'name': '',
                #             'uri':{
                #                 'uri':'',
                #                 'access_time':''
                #             }
                #         }
                #     ]
                # }
            # )

    bco['description_domain'] = description_domain

    return bco
#______________________________________________________________________________#
def parse_execution( dic ):
    """
    """

    exe = dic
#______________________________________________________________________________#
def parse_param( bco, jobs ):
    """
    """

    parametric_domain =[]
    for i in jobs:
        if 'files' in i['params'].keys(): pass
        else:
            for p in i['params'].keys():
                parametric_domain.append({
                    'param': p,
                    'value': i['params'][p],
                    'step': i['tool_id']
                })

    bco['parametric_domain'] = parametric_domain

    return bco
#______________________________________________________________________________#
def parse_io( bco, data_attrs ):
    """
uses jobs to oparse 
    """

    data = data_attrs
    input_subdomain = []
    for i in data:
        if i['designation'] == None:
            try: 
                uri = {'access_time': i['update_time'],'uri': i['uuid'],'filename': i['name']}
                input_subdomain.append(uri)
            except: 
                uri = {'access_time': i['update_time'],'uri': i['dataset_uuid'],'filename': i['name']}
                input_subdomain.append(uri)
    bco['io_domain']['input_subdomain'] = input_subdomain
    
    output_subdomain = []
    for i in data:
        if i['designation'] == 'output':
            try: output_subdomain.append({
                'mediatype': i['file_name'].split('.')[-1],
                'uri': {'access_time': i['update_time'],'uri': i['uuid'],'filename': i['name']}
            })
            except: output_subdomain.append({
                'mediatype': i['file_name'].split('.')[-1],
                'uri': {'access_time': i['update_time'],'uri': i['dataset_uuid'],'filename': i['name']}
            })
    bco['io_domain']['output_subdomain'] = output_subdomain
    
    return bco
#______________________________________________________________________________#
def parse_err( dic ):
    """
    """

    err = dic

#______________________________________________________________________________#
def main( ):
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])
    history, data_attrs, jobs, implicit, collections, export_attrs, libraries, data_provenance, workflow = read_galaxy_history(parsed_args.inputDirectory)
    bco = load_schema(parsed_args.schema)
    bco = parse_usability(bco, history)
    bco = parse_prov(bco, history)
    bco = parse_io(bco, data_attrs)
#    bco = parse_param(bco, jobs)
    parse_description(bco, workflow)

    bco = parse_top(bco, history)
    print(json.dumps(bco, indent=4))

    #print(parsed_args.schema)

#______________________________________________________________________________#
if __name__ == "__main__":
    main()