Galaxy-To-BCO Mapping
=============
In this directory are two csv mapping files, the first of which was used to develop the code for [the initial release](https://github.com/biocompute-objects/Galaxy-To-BCO/tree/0.1.0)

1) workflow2BCO.csv -> has four columns. 
    first column is the BCO field 
    second indicates if that field had to be populated manually 
    third indicates if that field could be populated automatically by our [BCO_editor](https://github.com/biocompute-objects/bco_editor/tree/openbox-bio-master/cgi-bin) tool
    fourth indicates if that field could be populated by the [Galaxy Workflow BCO tool](https://github.com/biocompute-objects/Galaxy-To-BCO/tree/0.1.0).

2) history2BCO.csv -> four columns. 
    First: BCO field, 
    Second: file name packaged in Galaxy history zip to obtain the corresponding field
    Third: the specific field in the JSON objects present in history generated file
    Fourth: notes about that field.
