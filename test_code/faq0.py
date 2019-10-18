#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################################################
## ##
""" """
################################################################################
import json
import jsonref
import jsonschema

# https://python-jsonschema.readthedocs.io/en/stable/faq/#why-doesn-t-my-schema-s-default-property-set-the-default-on-my-instance
def extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])

        for error in validate_properties(validator, properties, instance, schema):
            yield error

    return jsonschema.validators.extend(validator_class, {"properties": set_defaults})


DefaultValidatingDraft7Validator = extend_with_default(jsonschema.Draft7Validator)

# Recursively walk through a JSON Schema initializing it with blank defaults.
# TODO: rename function and check if there are issues with how this is
# modifying the datastructure it is iterating through.
def iterdict(schema):
    for k, v in schema.items():
        if isinstance(v, dict):
            if v.get("type") == "object":
                v.setdefault("default", {})
            elif v.get("type") == "string":
                v.setdefault("default", "")
            elif v.get("type") == "array":
                v.setdefault("default", [])
            iterdict(v)


def main():
    # Load JSON Schema from the repository by using URL or local file using absolute path and 'file:' prefix
    schema_uri = "file:/Users/hadley/GitHub/bco-schema/biocomputeobject.json"
    schema = jsonref.loads(f'{{ "$ref": "{schema_uri}" }}', jsonschema=True)
    # Walk through the definitions ensuring they all *a* default
    iterdict(schema)

    data = {}
    # Use the extended validator to fill in `data` with default values from the schema
    for err in DefaultValidatingDraft7Validator(schema).iter_errors(data):
        # print validation errors with a schema path to make them easier to read/trace
        print(
            f'{err.message} in the schema path {err.schema.get("$id") }#{"/".join(err.schema_path)}'
        )

    # Pretty print `data` showing the assigned default values.
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
