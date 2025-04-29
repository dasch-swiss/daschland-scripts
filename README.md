# daschland-scripts

This repository contains all data for the creation of the example project Alice in DaSCHland.\
To upload the project, please follow the instructions in the upload protocol down below.


### Project structure:

-  `daschland_data.xml` The XML file containing the data for the project.
-  `daschland_ontology` The ontology folder containing the ontology files used to create the JSON ontology file.
-  `daschland.json` The JSON file containing the data for the project.
-  `data` The folder containing the project data.
   -  `Multimedia_Data` The folder containing the multimedia data (video, audio, ...) for the project, in subfolders according to the project classes.
   -  `Spreadsheet_Data` The folder containing the spreadsheet data for the project. Each project class has a separate spreadsheet file.
   -  `XML` The folder containing the XML data for the project.
-  `nodegoat` The folder containing all data to create the mirror project on Nodegoat.
-  `pyproject.toml` The Python project file containing all dependencies for the project.
-  `src` The folder containing the Python scripts for the project. 
   - `Helper_Scripts` The helper scripts containing custom functions.
   - `Scripts_excel2xml` The scripts to convert the spreadsheet data to XML, using the old module "dsp-tools excel2xml".
   - `Scripts_Nodegoat` The scripts to create the mirror project data on Nodegoat.
   - `Scripts_xmllib` The scripts to convert the XML data to JSON, using the current library "dsp-tools xmllib".
- `uv.lock` The lock file for the project, which is used to create a virtual environment for the project.


### Upload protocol:

To upload data to a DSP-API server, use the `dsp-tools` command line tool.
Please use the project admin account to upload data to the DSP-API server.

## Uploading Data locally:

dsp-tools create daschland.json
dsp-tools xmlupload -u cheshire.cat@dasch.swiss -p 'xxxx' daschland_data.xml


## Uploading Data to rdu-08 test server:

dsp-tools create -s https://app.rdu-08.dasch.swiss -u root@example.com -p 'xxxx' daschland.json
dsp-tools xmlupload -s https://app.rdu-08.dasch.swiss -u cheshire.cat@dasch.swiss -p 'xxxx' daschland_data.xml

