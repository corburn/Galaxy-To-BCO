#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################################################
                        ##JSON Parse Galaxy History##
"""Parses Galaxy History file for BCO creation
"""
################################################################################

import json
import jsonref
import jsonschema
import sys 
import argparse
import os
import glob

bco = {    "bco_id": "-1",    "checksum": "",    "bco_spec_version": "1.3.0",    "provenance_domain": {      "name": "",      "version": "",      "created": "",      "modified": "",      "contributors": [],      "license": ""    },    "usability_domain": [],    "extension_domain": {      "fhir_extension": [],      "scm_extension": {        "scm_repository": "",        "scm_type": "git",        "scm_commit": "",        "scm_path": ""      }    },    "description_domain": {      "keywords": [],      "pipeline_steps": []    },    "execution_domain": {      "script": [],      "script_driver": "",      "software_prerequisites": [],      "external_data_endpoints": [],      "environment_variables": {}    },    "parametric_domain": [      {        "param": "",        "value": "",        "step": ""      }    ],    "io_domain": {      "input_subdomain": [],      "output_subdomain": []    },    "error_domain": {      "empirical_error": {},      "algorithmic_error": {}    }  }
#______________________________________________________________________________#
def extend_with_default(validator_class):
    """Taken from: https://python-jsonschema.readthedocs.io/en/stable/faq/#why-doesn-t-my-schema-s-default-property-set-the-default-on-my-instance
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
    """Recursively walk through a JSON Schema initializing it with blank defaults.
TODO: rename function and check if there are issues with how this is
modifying the datastructure it is iterating through.
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

    parser.add_argument('-s', '--schema', default='file:/Users/hadley/GitHub/bco-schema/biocomputeobject.json',
                    help='The URL that contains the BCO schema.')

    return parser
#______________________________________________________________________________#
def read_galaxy_history( path ):
    """takes an abosolute path argument
    opens files contained in the Galaxy-History *.zip
    returns a JSON of each of the coorisponding files
    """
    
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
    print(json.dumps(data, indent=4))

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
    """Reads the Prov dom feilds for a GalaxyBCO
    """

    prov = dic['provenance_domain']
    prov['name'] = history['name']
    contributor = {  "orcid": "",  "affiliation": "",  "contribution": [],  "name": "", "email": "" }


    dic['provenance_domain'] = prov

    return dic
#______________________________________________________________________________#
def parse_usability( dic, history ):
    """Uses the Galaxy History annotation feild to populate the useablity domain
    """

    dic['usability_domain'] = history['annotation']
    # print dic['usability_domain']
    return dic
#______________________________________________________________________________#
def parse_extension( dic ):
    """
    """

#______________________________________________________________________________#
def parse_description( dic ):
    """
    """

    des = dic
#______________________________________________________________________________#
def parse_execution( dic ):
    """
    """

    exe = dic
#______________________________________________________________________________#
def parse_param( dic1, dic2 ):
    """
    """
#______________________________________________________________________________#
def parse_io( dic ):
    """
    """

    io = dic
#______________________________________________________________________________#
def parse_err( dic ):
    """
    """

    err = dic

#______________________________________________________________________________#
def main( bco ):
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])
    history,jobs, data_attrs, data_provenance = read_galaxy_history(parsed_args.inputDirectory)
    bco = load_schema(parsed_args.schema)
    bco = parse_top(bco, history)
    bco = parse_usability(bco, history)
    bco = parse_prov(bco, history)
    print(json.dumps(bco))

    print(parsed_args.schema)

#______________________________________________________________________________#
if __name__ == "__main__":
    main(bco)